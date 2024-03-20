"""!
@file task0.py
This file contains a function implementation for task0 of
the ME405 term project, "Init."

@author Jacob Lantin, Devon Lau, Filippo Maresca Denini
@date 19-Mar-2024

"""

# module imports
import pyb
import utime

# imported classes from motor_driver.py and encoder_reader.py
from motor_driver import MotorDriver
from encoder_reader import encoder


def task0_fxn():
    """!
    Task 0 of the term project is for
    the turret to wait three seconds, rotate 180 degrees clockwise,
    then wait two seconds. From which the scheduler will
    jump to task 1. The panning motor is used with the motor
    and encoder classes for this. The motor is driven
    until it hits 180 degrees/19000 encoder ticks.
    """
    
    while True: # generator
        
        # panning motor driver pins - (motor B) C1, A0, A1, timer 5    
        pinE = pyb.Pin.board.PC1
        pinA = pyb.Pin.board.PA0
        pinB = pyb.Pin.board.PA1
        timer1 = 5
        
        # panning motor encoder pins - (encoder C) C6, C7, timer 8
        pin1 = pyb.Pin.board.PC6
        pin2 = pyb.Pin.board.PC7
        timer2 = 8
        
        # initialize motor
        moe = MotorDriver(pinE, pinA, pinB, timer1)        
        moe.set_duty_cycle(-25)
        
        # initialize encoder
        enc = encoder(pin1, pin2, timer2)
        enc.zero()
        
        # sleep for 3 seconds
        utime.sleep(3)
        
        # spin turret 180 degrees:
        # initalize "prev" value
        prev = enc.read()
        
        # stop motor if encoder reads 19000
        while True:
            # only print encoder value if value changes
            new = enc.read()
            
            if new != prev:
                print(f"\nEncoder value: {new}")
            
            # 1900 (25V 1A) is apparently 180 degrees for the rotating motor
            if new <= -19000:
                moe.disable_motor()
                break
            
            # calculate encoder value every 10 ms
            utime.sleep_ms(10)
            
        # sleep for 2 seconds
        utime.sleep(2)
        
        # generator yield
        yield 0

        
# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program.
if __name__ == "__main__":

    # run task0 function
    task0_fxn()
