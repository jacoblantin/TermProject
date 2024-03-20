# TermProject

Jacob Lantin, Devon Lau, Filippo Maresca Denini

ME 405-04

Term Project: Learn by Dueling

Introduction:

Learn by Dueling is a project where students are tasked with making a Nerf launcher into an autonomously tracking and shooting launcher. A thermal camera and two electric motors were provided and must be included in our design. An emergency stop device also must be implemented in the design. During lab on week 10, teams will duel with their robots and demonstrate their proficiency with designing hardware and organized software that can work with each other and using mechatronics skills to implement controls.

Hardware:

The construction of our hardware design including the 11 main components is shown below in Figure 1.  The design includes many 3D printed parts and many repurposed parts from the Cal Poly Mechatronics lab. All parts, excluding the Nerf gun were either provided to us or 3D printed. Motor #1 and the spur gear sits in the 3D printed base. This base is meant to be a compact housing that secures our power transmission that controls the gun’s yaw angle. The shaft of the spur gear fits snugly into the Nerf sleeve, which holds the Nerf gun, thermal camera, and trigger actuation mechanism. The picture in Figure 2 shows some of the 3D printed parts on the print bed.

![image](https://github.com/jacoblantin/TermProject/assets/145752175/7601ea8e-956f-4a89-8b67-bd75bfe7c3d8)

Figure 1. Overall Hardware Design

![image](https://github.com/jacoblantin/TermProject/assets/145752175/ac57fd7c-cbbf-4ea1-8bc6-5f944770d900)

Figure 2. 3D Printed Parts on Print Bed

The trigger actuation mechanism is driven by motor #2 and works with the pinion bevel gear, bevel gear, and trigger ring. The pinion bevel gear is press fit to the shaft of motor #2, which then meshes with the bevel gear. Figure 3 below displays a top-down view of the robot to more clearly show the trigger mechanism. There is a hole in the bevel gear which connects with the trigger ring through a shaft. The other side of the trigger ring is attached to the trigger itself. When motor #2 is actuated, the trigger ring is pulled on by the bevel gear and the trigger is pulled.

![image](https://github.com/jacoblantin/TermProject/assets/145752175/d06fb266-fc2b-423c-ad70-b0e4f1ec569d)

Figure 3. Top-Down View of Hardware

Software:

There are a total of seven .py files for this program. The program main.py is run on the computer while the other 6 .py files are uploaded to the microcontroller. The main file is a modified scheduler that runs in a round-robin form once that iterates through Task 0 – Init, Task 1 – Scan for Targets, and Task 2 – Fire. There is also an additional task implemented in main to terminate the program after one scheduled loop. The software is gone into more detail below.

Results:

To test the system, our robot was set up at the dueling table and a team member stood at the far end of the table as a target. The code was executed, and the gun responded accordingly: it turned 180°, tracked the target for 5 seconds, and then shot. Most of the time, the gun would turn around then stick onto the target at the end of the table, but sometimes, the infrared camera would sense heat to the left or right and slowly start tracking something that it was not supposed to. This problem would become elevated if the target were moving. To combat this, we tried implementing 3 seconds of waiting time before trying to track the target so the gun would hopefully not lose its target. This solution proved to be effective since we were more consistently able to hit our target. In our solo testing, we reached a point where the robot could hit its target 8/10 times.

Conclusion:

For this project, we ran into many issues involving our trigger mechanism. We had to make many iterations to our mechanical design for it to perform consistently and efficiently. The first iterations of our design did not involve any bevel gears and we learned that we did not have enough torque in the motor to pull the trigger this way. We needed a gear ratio to increase our torque and to more effectively pull on the trigger by pulling in a different direction. After many attempts of this new design, the shaft of the bevel gear kept snapping, so we decided to just drill a hole into our Nerf sleeve and have the screw be the shaft to the bevel gear. This solution was successful since it pulled our trigger very consistently without breaking.
For future teams attempting this project, it is important to try and specify the most efficient parts early in the design process. If our team had chosen a stepper motor to pull the trigger and had good placement with it, we could have eliminated the need for any bevel gears in our design. Another improvement is to have the infrared camera be placed stationary and closer to the targets. This requires some calibration before it can shoot but could have been a solution to our tracking sticking to incorrect targets. If the camera is closer, there is less noise from interferences and the fixed frame that the camera sees will make the aiming more precise.
In conclusion, our design worked well if it was given a very controlled environment, but with so much noise that our camera picked up, having the camera mounted on the gun might not have been the best direction. Issues of not enough torque for our trigger mechanism and breaking the bevel gear shaft were what the team spent most of the time fixing, but these issues eventually solved themselves. To avoid these issues altogether, we recommend that teams use a stepper motor, placed in a mechanically efficient lo
A brief discussion of what you've learned about the project and recommendations for anyone who would like to build upon your work. This does not mean a discussion of what you learned about mechatronics in general; that belongs in other places.  It is a discussion of what worked well and what didn't for this device.


"Doxygen Main Page"

I was unsure as to how to edit the Doxygen main page, so the software details will go here. The software is split into three main tasks, as detailed in the State diagram below:
 
 ![image](https://github.com/jacoblantin/TermProject/assets/145752175/ee4e2eaf-a906-4c94-a083-bbad83497b92)

Figure 4. State Diagram

Each state is written as a task .py file in the code, namely task0.py, task1.py, and task2.py.

The file task0.py, Init, rotates the panning motor 180 degrees. There is a period of waiting 3 seconds before and waiting 2 seconds after the motor spin for timing purposes for the duel. This is so that the turret can be activated starting at a countdown of 3 seconds, then fire after the 5 seconds of waiting has passed. The motor driver and encoder files are used.

The file task1.py, Scan for Targets, is a modified mlx_cam file that runs a camera scan and rotates the motor accordingly in a loop for a set number of times, this being 4. After four loops have passed, the task moves to the next state. The mlx_cam.py file that Dr. Ridgely has provided to us is modified so that the camera takes an image, and that image is processed so that an average of the “hottest” pixels' position is calculated. That position is given to the microcontroller to adjust the panning motor towards that position. The control loop is used in this task to push the motor incrementally in said direction. This happens four times so that the turret is pointing towards the target by the end of the four loops.

The file task2.py, Fire, sends a signal to the trigger motor with a set Kp of 50 and around 5000 encoder ticks, a tested number that pushes the bevel gears enough to activate the trigger.

A Voltage of 25V and an Current of 1.0A is set for the whole system.

The control, encoder, and motor driver files are all essentially the same to the files from the previous lab. These supporting files are used in the three states to operate the motors.

There is also an extra small task in the main.py file to end the scheduler loop after one run-through of the three main tasks.


