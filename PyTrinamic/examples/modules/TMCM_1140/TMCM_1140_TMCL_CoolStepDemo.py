#!/usr/bin/env python3
'''
Move a motor back and forth using the TMCM1140 module

Created on 13.07.2021

@author: Trinamic Software Team
'''

import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules import TMCM_1140
import time

PyTrinamic.showInfo()
connectionManager = ConnectionManager("--interface serial_tmcl --port COM6 --data-rate 115200")

with connectionManager.connect() as myInterface: 
    module = TMCM_1140(myInterface)
    motor = module.motors[0]

    # The configuration is based on our PD42-1-1140-TMCL
    # If you use a different motor be sure you have the right configuration setup otherwise the script may not working.

    print("Preparing parameters")
    #preparing drive settings 
    motor.DriveSetting.max_current= 2000
    motor.DriveSetting.standby_current = 0
    motor.DriveSetting.boost_current = 0
    motor.DriveSetting.microstep_resolution = motor.ENUMs.microstep_resolution_256_microsteps
    print(motor.DriveSetting)
    #preparing linear ramp settings 
    motor.max_acceleration = 2000
    motor.max_velocity = 2000
    print(motor.LinearRamp)

    #reset actual position 
    motor.actual_position = 0

    #start rotating motor 
    print("Rotating")
    motor.rotate(1500)
    
    #set up StahlGuard2
    print("Initial StallGuard2 values:")
    print(motor.StallGuard2)
    motor.StallGuard2.calibrate_zero()
    print("StallGuard2 after calibration: ")
    print(motor.StallGuard2)

    print("try to stop motor")

    while not(motor.actual_velocity == 0):
        time.sleep(0.2)
    
    time.sleep(3)
    print("Start rotating again")
    motor.rotate(1500)

    print("Initial CoolStep values:")
    print(motor.CoolStep)
    motor.CoolStep.calibrate()
    print("CoolStep after calibration:")
    print(motor.CoolStep)

    time.sleep(10)
    #stop rotating motor
    print("Stopping")
    motor.stop()
    

print("\nReady.")
