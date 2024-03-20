"""!
@file task2.py
This file contains a function implementation for task2 of
the ME405 term project, "Fire."

@author Jacob Lantin, Devon Lau, Filippo Maresca Denini
@date 19-Mar-2024

"""

# module imports
import pyb
import utime

# imported classes from control.py, motor_driver.py, and encoder_reader.py
from control import CLPControl
from motor_driver import MotorDriver
from encoder_reader import encoder


def task2_fxn():
    """!
    Task 2 of the term project is for
    the trigger motor to activate with a sufficiently
    high Kp and encoder rotation to pull the trigger using
    the bevel gears on the turret. For this task,
    with a Voltage set to 25V and an Amperage set to
    1.0 A, the parameters used are Kp = 50 and setpoint
    = 5000.
    """

    while True: # generator
        
        # trigger motor driver pins - (motor A) A10, B4, B5, timer 4    
        pinE = pyb.Pin.board.PA10
        pinA = pyb.Pin.board.PB4
        pinB = pyb.Pin.board.PB5
        timer1 = 3
        
        # trigger motor encoder pins - (encoder B) B6, B7
        pin1 = pyb.Pin.board.PB6
        pin2 = pyb.Pin.board.PB7
        timer2 = 4
        
        # initalize controller class
        CLP = CLPControl(pinE, pinA, pinB, timer1, pin1, pin2, timer2)
        
        # set Kp to 50
        CLP.set_Kp(50)
        
        # pull trigger with -5000 encoder ticks
        CLP.set_setpoint(-5000)
        
        # run
        CLP.run()
        
        # disable motor
        CLP.disable_motor()    
        
        # print "end"
        print("End")
        
        # generator yield
        yield 0

        
# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program.
if __name__ == "__main__":

    # run task2 function
    task2_fxn()