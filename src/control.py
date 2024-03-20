"""!
@file control.py
This file contains a class implementation that represents a proportional gain
closed control loop for use in the term project. The file is used in conjunction
with motor_driver.py and encoder_reader.py to drive the motor in a closed
control loop.

@author Jacob Lantin, Devon Lau, Filippo Maresca Denini
@date 19-Mar-2024

"""

# module imports
import utime
import pyb

# imported classes from lab01 (motor driver) and lab02 (encoder)
from motor_driver import MotorDriver
from encoder_reader import encoder


class CLPControl:
    """!
    This class contains the constructor and methods that initialize the control loop variables
    and allow for the control algorithm to be run with a given Kp, the proportional gain constant.
    """
    
    def __init__(self, pinE, pinA, pinB, timer1, pin1, pin2, timer2):
        """!
        This constructor initializes the motor driver, encoder, Kp, and setpoints. It also
        zeros the encoder.
        @param pinE - pinENA for motor driver
        @param pinA - pin A for motor driver
        @param pinB - pin B for motor driver
        @param timer1 - timer for motor driver
        @param pin1 - pin 1 for encoder
        @param pin2 - pin 2 for encoder
        @param timer2 - timer for encoder
        """
        
        # initialize motor driver class
        self.moe = MotorDriver(pinE, pinA, pinB, timer1)        

        # intialize encoder class
        self.pin1 = pyb.Pin(pin1, pyb.Pin.IN)
        self.pin2 = pyb.Pin(pin2, pyb.Pin.IN)
        self.timer = timer2
        self.enc = encoder(self.pin1, self.pin2, self.timer)
        
        # zero encoder
        self.enc.zero()
        
        # initialize Kp, the proportional gain (default to 0)
        self.Kp = 0
                
        # initialize setpoint, the inital/current position/setpoint (default to 0)
        self.setpoint = 0
        
        # initialize setpoint_desired, the desired position/setpoint (default to 0)
        self.setpoint_desired = 0
     
    
    def set_setpoint(self, setpoint):
        """!
        This method sets the DESIRED setpoint.
        @param setpoint - input, the desired setpoint
        """                
        self.setpoint_desired = setpoint
    
    
    def set_Kp(self, Kp):
        """!
        This method sets Kp, the proportional gain constant.
        @param Kp - input, the set proportional gain constant
        """
        self.Kp = Kp

    
    def run(self):
        """!
        This method is called repeatedly to run the control algorithm.
        The method runs the control loop a set amount of times every 10 ms.
        The time and position is tracked over a range of 2000 ms, or 2 seconds, and stored in a list of tuples.
        """        
        # time in ms
        self.time = 0
        
        # list with time and position
        self.listy = []
        
        # run control loop 100 times (1 second)
        for x in range(10):
            
            # read encoder current position
            current = self.enc.read()
            
            # append list with current time and position
            self.listy.append((self.time,current))
            
            # calculate error
            error = self.setpoint_desired - current
            
            # multiply error by Kp (/1000 for scaling)
            PWM = (self.Kp / 1000) * error        
            
            # send PWM (actuation) to motor driver
            self.moe.set_duty_cycle(PWM)
            
            # run every 10 ms
            utime.sleep_ms(10)
            self.time += 10
            
    
    def disable_motor(self):
        """!
        This method disables the motor by using the motor class.
        """
        self.moe.disable_motor()
    
    
    def print_results(self):
        """!
        This method prints the results, the list of tuples, formatted for use in the interface.
        """
        for x in self.listy:
            print(', '.join(map(str, x)))



# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program.
if __name__ == "__main__":
        
    pass
    



