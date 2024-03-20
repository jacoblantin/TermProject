"""!
@file task1.py
This file is modified from the mlx_cam.py file provided to
us by Dr. Ridgely. This chat is modified by our Lab05 lab group
in conjunction with some code from ChatGPT for task1 of the
ME 405 term project, "Scan for Targets." The code contains a class
implementation to intiialize the I2C MLX cam provided to us,
an algorithm function (assisted by ChatGPT) to find the
hottest pixel to center on, and a function to turn the panning
motor/camera in conjunction with where the hottest pixel is.

@author Jacob Lantin, Devon Lau, Filippo Maresca Denini
@date 19-Mar-2024

"""

# module/provided imports
import pyb
import utime as time
from machine import Pin, I2C
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern

# imported custom classes from control.py and otherwise
from control import CLPControl
from task0 import task0_fxn
from task2 import task2_fxn


class MLX_Cam:
    """!
    (Provided by Dr. Ridgely) Class which wraps an MLX90640 thermal infrared camera
    driver to make it easier to grab and use an image. This image is in "raw" mode,
    meaning it has not been calibrated (which takes lots of time and memory) and only
    gives relative IR emission seen by pixels, not estimates of the temperatures.
    """
    
    def __init__(self, i2c, address=0x33, pattern=ChessPattern,
                 width=NUM_COLS, height=NUM_ROWS):
        """!
        Constructor to set up an MLX90640 camera.
        @param i2c - An I2C bus which has been set up to talk to the camera;
                     this must be a bus object which has already been set up
        @param address - The address of the camera on the I2C bus (default 0x33)
        @param pattern - The way frames are interleaved, as we read only half
                         the pixels at a time (default ChessPattern)
        @param width - The width of the image in pixels; leave it at default
        @param height - The height of the image in pixels; leave it at default
        """

        ## The I2C bus to which the camera is attached
        self._i2c = i2c
        ## The address of the camera on the I2C bus
        self._addr = address
        ## The pattern for reading the camera, usually ChessPattern
        self._pattern = pattern
        ## The width of the image in pixels, which should be 32
        self._width = width
        ## The height of the image in pixels, which should be 24
        self._height = height
        ## Tracks whether an image is currently being retrieved
        self._getting_image = False
        ## Which subpage (checkerboard half) of the image is being retrieved
        self._subpage = 0

        # The MLX90640 object that does the work
        self._camera = MLX90640(i2c, address)
        self._camera.set_pattern(pattern)
        self._camera.setup()

        ## A local reference to the image object within the camera driver
        self._image = self._camera.raw

    
    def get_image_nonblocking(self):
        """!
        This method gets an image from an MLX90640 camera in a non-blocking way.
        The code and functionality for this is provided by Dr. Ridgely.
        """
        
        # If this is the first recent call, begin the process
        if not self._getting_image:
            self._subpage = 0
            self._getting_image = True
        
        # Read whichever subpage needs to be read, or wait until data is ready
        if not self._camera.has_data:
            return None
        
        image = self._camera.read_image(self._subpage)
        
        # If we just got subpage zero, we need to come back and get subpage 1;
        # if we just got subpage 1, we're done
        if self._subpage == 0:
            self._subpage = 1
            return None
        else:
            self._getting_image = False
            return image


def center_camera_on_hottest_pixel_x(camera, CLP):
    """!
    This function is a custom algorithm to capture an image using
    the camera class above, find the maximum "temperature" or heat
    signature in the image, and turn the motor in the direction of
    that heat signature. The heat signature is averaged from the
    highest heat signatures throughout the image.
    
    This function was created using the help of ChatGPT, inserting
    pseudo-code into the chat box and asking for an algorithm.
    @param camera - I2C MLX camera class
    @param CLP - control loop class to run motor
    """
    
    # Capture an image
    image = None
    while not image:
        image = camera.get_image_nonblocking()
        time.sleep_ms(5) # was 50

    # Find the maximum temperature in the image
    max_temp = max(image)

    # Find all the pixels with the maximum temperature
    max_temp_pixels = [(row, col) for row in range(camera._height) for col in range(camera._width) if image[row * camera._width + col] == max_temp]

    # Calculate the average position of the pixels with the highest temperature
    if max_temp_pixels:
        avg_row = sum(row for row, _ in max_temp_pixels) // len(max_temp_pixels)
        avg_col = sum(col for _, col in max_temp_pixels) // len(max_temp_pixels)

        # Calculate adjustment to center the camera on the averaged position
        center_col = camera._width // 2
        col_adjustment = center_col - avg_col

        # Move the motor to center the camera in the x-direction
        CLP.set_Kp(20)
        CLP.set_setpoint(-col_adjustment*150)
        CLP.run()

        # Display information if needed
        print(f"Averaged hottest pixel coordinates: (row, {avg_col})")
        print(f"Adjustment in x-direction: {col_adjustment}")


def task1_fxn():
    """!
    This function was originally named "test_MLX_cam_with_motor()."
    
    This function contains code which initializes the I2C bus for the camera,
    initializes the control loop for the motor, and runs the camera-centering
    function above to function as Task 1
    
    This function is modified from the code that Dr. Ridgely provided for us and
    is assisted by ChatGPT to run with the camera-centering function above.
    """
    
    while True: # generator
        
        import gc

        # The following import is only used to check if we have an STM32 board such
        # as a Pyboard or Nucleo; if not, use a different library
        try:
            from pyb import info

        # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
        except ImportError:
            # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
            i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

        # OK, we do have an STM32, so just use the default pin assignments for I2C1
        else:
            i2c_bus = I2C(1)

        print("MXL90640 Easy(ish) Driver Test")

        # Select MLX90640 camera I2C address, normally 0x33, and check the bus
        i2c_address = 0x33
        scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
        print(f"I2C Scan: {scanhex}")

        # Create the camera object and set it up in default mode
        camera = MLX_Cam(i2c_bus)
        print(f"Current refresh rate: {camera._camera.refresh_rate}")
        camera._camera.refresh_rate = 100.0
        print(f"Refresh rate is now:  {camera._camera.refresh_rate}")

        print("MXL90640 Easy(ish) Driver Test with Motor")
        
        # panning motor driver pins - (motor B) C1, A0, A1, timer 5    
        pinE = pyb.Pin.board.PC1
        pinA = pyb.Pin.board.PA0
        pinB = pyb.Pin.board.PA1
        timer1 = 5
        
        # panning motor encoder pins - (encoder C) C6, C7, timer 8
        pin1 = pyb.Pin.board.PC6
        pin2 = pyb.Pin.board.PC7
        timer2 = 8   
        
        # 4 loops = ~2 seconds
        for n in range(4):
            try:
                CLP = CLPControl(pinE, pinA, pinB, timer1, pin1, pin2, timer2)
                
                center_camera_on_hottest_pixel_x(camera, CLP)
            
            except KeyboardInterrupt:
                # Stop the motor if the script is interrupted
                CLP.disable_motor()
         
        # disable motor 
        CLP.disable_motor()
        
        # generator yield
        yield 0



# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program.
if __name__ == "__main__":
    
    pass


