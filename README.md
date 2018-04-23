RAILCAR COUNTER
Developed by Yilin Yang
Last Updated Feb. 1st 2018

OBJECTIVE:
1. Counts the number of cars in a supplied video that 
exit the frame differentiating between left and right

2. Displays the current count on the video frame which
updates as the video plays

3. Bonus: Identify the cars by unique number and output
a CSV file stating which way each car went

INSTALLATION AND EXECUTION:
1. Program is designed in Windows 10 64-bit using Python 3.6

2. Program is currently contained entirely within "main.py"

3. Video input must be specified in global variable "input_path"
in the format 'filename.type' including single quotations

4. Two external libraries must by installed and imported:
numpy and opencv. Both may be downloaded at the website:
	https://www.lfd.uci.edu/~gohlke/pythonlibs/
NOTE: the version required will depend on your system specifications
EXAMPLE: Python 3.6 requires filename containing "cp36"

5. Numpy and opencv libraries must be installed using pip install
in the same directory the version file is downloaded
EXAMPLE: pip install numpy-1.12.0+mk1-cp36-cp36m-win32.whl

6. Confirm successful installation. The terminal you are using should
display a message verifying if the installation succeeded or not.

7. Done! You should be able to run main.py without issue.

IMPLEMENTATION NOTES:
-Program uses background subtraction techniques to identify railcar contours

-Contour centers are calculated and tracked. If the coordinates of the center
pass center thresholds, the program classifies the car as having exited in a 
certain direction

-The accuracy of tracking is not perfect and can always be improved. In particular
the program has difficulty identifying flatcars

-Objective 3 is not fully complete. Time is monitored correctly but specific car
IDs have not been assigned yet. The plan is to use a queue system to push an ID
when a new car appears and pop it when the car exits.

ACKNOWLEDGMENTS:
The following website was invaluable in guiding a first time user (myself) on
how to install and work with OpenCV. This was my first experience with image processing
and I would not have been able to figure out what to do without this guide's assistance.
https://www.solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/
