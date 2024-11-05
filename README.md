# picoArducam

This is a repository with the files I am using to run the Arducam 2560 board with MicroPython.  I wanted to drive the waveshare ST7789 display directly from the Pico; however, the output from the camera is a jpg (even when a bmp file is requested.  I have to take the image onto my computer, convert it using Pillow to pixels, and save the file in rgb565 format.  I can then load the file and display it on the screen (it's very slow).  This repo has the files that I am using to make it work.  Still working on a better solution.
