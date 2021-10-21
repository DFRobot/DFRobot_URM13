# -*- coding: utf-8 -*
'''!
  @file  URM13_work_in_IIC.py
  @brief  This demo shows how URM13 works in IIC interface mode.
  @n      can obtain and change the sensor basic information, configure parameters and get the current distance value and current temperature value
  @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license  The MIT License (MIT)
  @author  [qsjhyy](yihuan.huang@dfrobot.com)
  @version  V1.0.0
  @date  2021-09-24
  @url  https://github.com/DFRobot/DFRobot_URM13
'''
from __future__ import print_function
import sys
sys.path.append('../')
from DFRobot_URM13 import *

'''
  # UART(Modbus-RTU) and I2C/TRIG mode switch
  # URM13 sensor default setting is in UART mode. The sensor can switch between I2C and UART modes simply by short-circuiting different pins before power-on：

  # I2C/TRIG: Short-circuit TRIG and ECHO pins before the sensor is powered on. After the sensor is powered on, that the LED flashes twice indicates the sensor has switched to I2C mode.
  # UART(Modbus-RTU): Short-circuit TRIG and BUSY pins before the sensor is powered on. After the sensor is powered on, that the LED flashes once indicates the sensor has switched to UART(Modbus-RTU) mode.Short-circuit TRIG and BUSY pins before the sensor is powered on. After the sensor is powered on, that the LED flashes once indicates the sensor has switched to UART(Modbus-RTU) mode.

  # After the mode switch succeeds, users can disconnect the corresponding pin short-circuiting, and the switched mode will be recorded by the sensor and take effect permanently.

  # instantiate an object to drive the sensor
'''
sensor = DFRobot_URM13_I2C(i2c_addr = 0x12, bus = 1)


def setup():
  while (sensor.begin() == False):
    print ('Please check that the device is properly connected')
    time.sleep(3)
  print("sensor begin successfully!!!\n")

  '''
    # read module basic information
    # retrieve basic information from the sensor and buffer it into a variable that stores information:
    # addr_IIC, PID_IIC, VID_IIC
  '''
  sensor.read_basic_info()

  # module I2C slave address, the default value is 0x12, module device address(1~127)
  print("baudrate: 0x%x" %sensor.addr_IIC)

  # module PID, the default value is 0x02 the bit is used for product check[can detect the sensor type]
  print("PID: 0x0%x" %sensor.PID_IIC)

  # module VID, firmware revision number：0x10 represents V1.0
  print("VID: 0x%x" %sensor.VID_IIC)

  '''
    # set the module communication address, power off to save the settings, and restart for the settings to take effect
    # addr device address to be set, IIC address range(1~127 is 0x01~0x7F)
  '''
  sensor.set_addr(0x12)

  '''
    # set measure mode
    # mode measure mode to be set, the following patterns constitute mode:
    #   E_INTERNAL_TEMP: use internal temperature compensation function, E_EXTERNAL_TEMP: use external temperature compensation function (users need to write external temperature)
    #   E_TEMP_COMP_MODE_EN: enable temperature compensation function, E_TEMP_COMP_MODE_DIS: disable temperature compensation function
    #   E_AUTO_MEASURE_MODE_EN: automatic ranging, E_AUTO_MEASURE_MODE_DIS: passive ranging
    #   E_MEASURE_RANGE_MODE_LONG: large range measurement(40 - 900cm), E_MEASURE_RANGE_MODE_SHORT: small range measurement(15-150cm)
  '''
  sensor.set_measure_mode(sensor.E_INTERNAL_TEMP | 
                          sensor.E_TEMP_COMP_MODE_EN | 
                          sensor.E_AUTO_MEASURE_MODE_DIS | 
                          sensor.E_MEASURE_RANGE_MODE_LONG)

  '''
    # write ambient temperature data for external temperature compensation, the setting is invalid when out of range
    # temp written ambient temperature data, unit is ℃, resolution is 0.1℃, signed number, range:-10℃～＋70℃
  '''
  sensor.set_external_tempreture_C(30.0)

  '''
    # ranging sensitivity setting, 0x00-0x0A:sensitivity level 0-10
    # measure_sensitivity to set the sensor ranging sensitivity in large range (40-900cm), the smaller the value, and the higher the sensitivity, power off to save the settings, and it takes effect at once
  '''
  sensor.set_measure_sensitivity(0x00)

  print()
  time.sleep(1.5)


def loop():
  '''
    # the function to trigger measuring in passive measurement mode
    # in passive measurement mode, the function is called once, the ranging command is sent once, and the module measures the distance once and saves the measured value into the distance register
  '''
  sensor.passive_measurement_TRIG()

  '''
    # get noise level of power supply, 0x00-0x0A matches noise level of 0-10
    # The parameter indicates the influence of power supply and environment on the sensor. The smaller the noise level, the more accurate the distance value obtained by the sensor
  '''
  noise_level = sensor.get_noise_level()
  print("Current ambient noise level: 0x0%x" %noise_level)

  '''
    # read the current internal temperature
    # the current internal temperature value, unit is ℃, resolution is 0.1℃, signed number
  '''
  internal_tempreture_C = sensor.get_internal_tempreture_C()
  print("The onboard temperature: %d C" %internal_tempreture_C)

  '''
    # read the current distance value, the value of zero indicates it's not measured within the range
    # note: when the object is not in the sensor ranging range, the read measured data will be meaningless
    # the current distance value, unit is cm, large range(40 - 900cm)small range(15-150cm)
  '''
  distance_cm = sensor.get_distance_cm()
  print("Current distance measurement: %d cm" %distance_cm)

  print()
  time.sleep(1)


if __name__ == "__main__":
  setup()
  while True:
    loop()
