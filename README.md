# Disappearing Text App


## Description

The Disappearing App is a Python application with a graphical user interface (GUI) built using the Tkinter module. It is designed to help content writers maintain their productivity by setting a timer (3 or 5 minutes) and motivating them to keep writing. The app keeps track of the user's keyboard input and saves the highest word count achieved during the specified time duration.

## Features

- Choose between a 3-minute or 5-minute timer.
- Displays the highest word count achieved during the selected time duration.
- Autosave functionality to save the written content in a text file.
- Automatic content deletion if no typing is detected within 3 seconds to encourage continuous writing.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)

## Usage:

- Run the `main.py` script on your IDE.

- Select the desired time duration (3 minutes or 5 minutes) and start writing.

- If you stop typing for 3 seconds, the app will automatically delete your content.

- Your highest word count is displayed, and the written content is saved to a text file.


## Working of App:

### 3 mins interface:
![3 mins](readmepics/3_minutes.png)
### 5 mins interface:
![5 mins](readmepics/5_minutes.png)
### Time Over:
![timeup](readmepics/timeover.png)
### 3 sec timer:
![timer](readmepics/timer.png)