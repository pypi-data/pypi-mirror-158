import os
import time
import pyvisa
import logging

RANGE = 'AUTO'

logging.basicConfig(filename='diagnosticLog_dmm.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


class KeySight34465A:

    def __init__(self):
        self.dmm = None
        self.connection_string = None
        self.resource_manager = None

    def open_connection(self):
        """
        Opens a TCP/IP connection to connect to the TDK Lambda PSU
        """
        self.resource_manager = pyvisa.ResourceManager()
        self.connection_string = os.getenv("MUX_CONNECTION_STRING", default='TCPIP0::192.168.123.200::INSTR')
        try:
            logging.info(f": Opening KeysightDMM 34465A Resource at {self.connection_string}")
            self.dmm = self.resource_manager.open_resource(self.connection_string)
            self.dmm.read_termination = '\n'
            self.dmm.write_termination = '\n'
            time.sleep(3)
        except Exception as err:
            raise Exception(f": ERROR {err}: Could not open connection! ")

    def close_connection(self):
        """
        Closes the TCP/IP connection to the TDK Lambda PSU
        """
        self.resource_manager.close()

    def self_test(self):
        """
        Performs the self-test and checks for system errors
        :return: Boolean: True or Error
        """
        sys_err = self.dmm.query(f'SYST:ERR?')
        if sys_err == '+0,"No error"':
            try:
                selftest = self.dmm.query(f'TEST:ALL?')
                if selftest == "+0":
                    logging.info("PASS: SELF-TEST PASSED!")
                    return True
            except Exception as e:
                raise Exception(f": ERROR: {e} One or more self-test has FAILED")
        else:
            logging.error(f": SYSTEM_ERROR: {sys_err}")
            raise

    def system_info(self):
        """
        This function gets all the system info for the Keysight DMM 34465A
        :return: information in logs
        """
        time.sleep(5)
        idn = self.dmm.query(f'*IDN?')
        logging.info(f": IDN: {idn} \n")

        sys_ver = self.dmm.query(f'SYST:VERS?')
        logging.info(f": System Version: {sys_ver}")

        is_dhcp = self.dmm.query(f'SYST:COMM:LAN:DHCP?')
        logging.info(f": DHCP Setting: {is_dhcp} \n")

        ip_address = self.dmm.query(f'SYST:COMM:LAN:IPAD?')
        logging.info(f": IP Address: {ip_address} \n")

        mac_address = self.dmm.query(f'SYST:COMM:LAN:MAC?')
        logging.info(f": MAC Address: {mac_address} \n")

        host_name = self.dmm.query(f'SYST:COMM:LAN:HOST?')
        logging.info(f": DNS Hostname: {host_name} \n")

        subnet_mask = self.dmm.query(f'SYST:COMM:LAN:SMASK?')
        logging.info(f": Subnet Mask: {subnet_mask} \n")

        dns_setting = self.dmm.query(f'SYST:COMM:LAN:DNS?')
        logging.info(f": DNS Setting: {dns_setting} \n")

        gateway = self.dmm.query(f'SYST:COMM:LAN:GAT?')
        logging.info(f": Default Gateway: {gateway} \n")

    def configure_current(self, test_mode, ranges, resolution):
        """
        This function sets all the measurement parameters and trigger parameters to their default values with specified
        range and resolution
        :param test_mode: AC/DC
        :param ranges: {100µA | 1mA | 10mA | 100mA | 1A | 3A | 10A }. Default: AUTO
        :param resolution: AC: optional and ignored, fixed to 6 1/2 digits; DC default 10 PLC
        :return: Success or failure
        """
        conf_curr = self.dmm.query(f'CONF:CURR:{str(test_mode).upper()} {ranges}, {float(resolution)}')
        logging.info(f": {str(test_mode).upper()} Current: {conf_curr} Amps \n")
        return True

    def get_current(self, test_mode):
        """
        This function reads a current measurement
        :param test_mode: AC/DC
        :return: float: Current in Amps
        """
        current = self.dmm.query(f'MEAS:CURR:{test_mode}?')
        logging.info(f": {str(test_mode)} Current: {current} Amps \n")
        return float(current)

    def configure_voltage(self, test_mode, ranges, resolution):
        """
        This function sets all the measurement parameters and trigger parameters to their default values with specified
        range and resolution
        :param test_mode: AC/DC
        :param ranges: {100 mV | 1 V | 10 V | 100 V | 1000 V}. Default: AUTO
        :param resolution: AC: optional and ignored, fixed to 6 1/2 digits; DC default 10 PLC
        :return: Success or failure
        """
        conf_volt = self.dmm.query(f'CONF:VOLT:{str(test_mode).upper()} {ranges}, {float(resolution)}')
        logging.info(f": {str(test_mode).upper()} Voltage: {conf_volt} Volts \n")
        return True

    def get_voltage(self, test_mode):
        """
        This function reads a voltage measurement
        :param test_mode: AC/DC
        :return: float: Current in Amps
        """
        voltage = self.dmm.query(f'MEAS:VOLT:{test_mode}?')
        logging.info(f": {str(test_mode)} Voltage: {voltage} Volts \n")
        return float(voltage)

    def measurements(self):
        """
        This function takes all the necessary measurements from the DMM
        :return: Values in logs
        """
        frequency = self.dmm.query(f'MEAS:FREQ?')
        logging.info(f": Frequency: {frequency} \n")

        period = self.dmm.query(f'MEAS:PER?')
        logging.info(f": Period: {period} \n")

        # If the input signal is greater than can be measured on the specified manual range, the instrument displays
        # the word Overload on front panel and returns "9.9E37" from the remote interface.

        diode = self.dmm.query(f'MEAS:DIOD?')
        if diode > '+9.8E+37':
            logging.info(f": Check Diode value for Overload of measurement!")
        else:
            logging.info(f": Diode value: {diode} \n")

        resistance = self.dmm.query(f'MEAS:RES?')
        if resistance > '+9.80000000E+37':
            logging.info(f": Check Resistance value for Overload of measurement!")
        else:
            logging.info(f": Resistance value: {resistance} \n")

        capacitance = self.dmm.query(f'MEAS:CAP?')
        if capacitance > '+9.80000000E+37':
            logging.info(f": Check Capacitance value for Overload of measurement!")
        else:
            logging.info(f": Capacitance: {capacitance} \n")
