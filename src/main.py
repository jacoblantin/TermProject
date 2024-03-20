"""!
@file main.py
    This file contains the main file, modified from basic_tasks.py, to run the tasks for the ME405 term project
    sequentially in a real-time scheduler. Each task is modified as a generator file, and the main file in this
    task runs each task after one another. There is also an extra task that prevents the turret from running
    in a continuous loop.

@author Jacob Lantin, Devon Lau, Filippo Maresca Denini
@date   19-Mar-2024

"""

# module imports
import gc
import pyb
import cotask
import task_share

# task imports
from task0 import task0_fxn
from task1 import task1_fxn
from task2 import task2_fxn

# task to end program after one loop
def end_program_task():
    while True:
        print("Ending program.")
        break  # Exit the loop to end the program
        yield  # Yield control back to the scheduler

if __name__ == "__main__":
    
    # Initialize Task
    Task0 = cotask.Task(task0_fxn, name="Task_0", priority=1, period=10, profile=True, trace=False)
    Task1 = cotask.Task(task1_fxn, name="Task_1", priority=1, period=10, profile=True, trace=False)
    Task2 = cotask.Task(task2_fxn, name="Task_2", priority=1, period=10, profile=True, trace=False)
    EndProgramTask = cotask.Task(end_program_task, name="End_Program_Task", priority=2, period=100, profile=True, trace=False)
    
    # Append tasks to list
    cotask.task_list.append(Task0)
    cotask.task_list.append(Task1)
    cotask.task_list.append(Task2)
    cotask.task_list.append(EndProgramTask)
    
    # Run the scheduler with the rr_sched scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.rr_sched()
            
        except StopIteration:
            break        
        
        except KeyboardInterrupt:
            break

