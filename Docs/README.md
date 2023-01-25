# GoPro-App
<img align="left" src=https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/film-roll.png width=200>
A wireless control app for a GoPro Hero10. The purpose of this app is to allow researchers to control a GoPro worn by a surgeon in the operating room from a distance
so that the non-sterile research staff minimize contact with the sterile OR team.

The app allows the researcher to connect to the GoPro, start and stop video, take a photo, adjust GoPro settings, check the battery and SD card status, and save out
new videos and images taken into user defined directories. For a detailed breakdown of the App refer to [the app breakdown](#app-breakdown)

This project uses the [Open GoPro SDK](https://gopro.github.io/OpenGoPro/python_sdk/) for all communication with and from the GoPro.

> **Note**
>
> This product and/or service is not affiliated with, endorsed by or in any way associated with GoPro Inc. or its products and services. GoPro, HERO, and their 
> respective logos are trademarks or registered trademarks of GoPro, Inc.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/iSensTeam/GoPro-App/blob/main/LICENSE)
[![GitHub followers](https://img.shields.io/github/followers/Nabizzle?style=social)](https://github.com/Nabizzle)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/open-gopro)](https://www.python.org/downloads/release/python-3109/)

# App Description
The app is available in both a dark and light mode version shown below. The app will default to your system theme, but there is also a theme switcher in the upper
right of the app. This app was designed in dark mode so it is preferred aesthetically, but there is no functional difference between the themes.

![Dark Mode App](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/App%20Darkmode.png)
![Light Mode App](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/App%20Lightmode.png)

## App Breakdown
![Labeled App](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/GUI%20Labeled.png)

1. **Resolution Selector**: Allows the user to select between the available resolutions for the GoPro.
   - Note that not all frame rates are possible at a given resolution
2. **Frame Rate Selector**: Allows the user to select between the available frame rates for a given resolution on the GoPro
3. **Field of View Selector**: Allows the user to select between the field of view options on the GoPro
4. **Theme Selector**: Allows the user to select between the system default theme, a dark theme, and a light theme for the app
5. **Video Recording Switch**: A switch to start and stop a video recording on the GoPro
6. **Photo Button**: Switches to photo mode, takes a photo, and returns to video mode
7. **Directory Name**: The name of a user defined subdirectory in the Data folder of the repository
   - If you don't have a Data folder, the app generates one when it is opened
8. **Refresh Battery Indicator Button**: Polls the GoPro for an updated estimate of battery life and SD card recording room
9. **Battery and SD Card Status Indicators**: Shows the battery life and room left on the SD card
   - These values will change based on the selected resolution and frame rate
   - Battery life is shown as a time and as a colored bar for high, medium and low battery
   
   ![High Battery](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/Battery%20High.png)
   ![Medium Battery](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/Battery%20Medium.png)
   ![Low Battery](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/Battery%20Low.png)
10. **Digital Zoom Slider**: Allows you to give the GoPro a digital zoom.
    > **Note**
    >
    > The motion of zooming with the slider is choppy due to the frequency of sending the commands at a low rate

11. **GoPro selector**: Dropdown menu for selecting which GoPro to connect to
    - If your GoPro is not listed, you can select the ability to connect to the first available GoPro
12. **Connection Button**: Button to start the connection to the GoPro
13. **File Transfer Button**: When clicked, all new files are saved into the user defined subdirectory from GUI element 7
14. **Timestamp Checkbox**: When checked, a timestamp for when the files were saved is added to the beginning of all transferred files in the format of 
YYYYMMDD_HHMMSS_"GoPro file name"

> **Note**
>
> Not all resolutions and frame rates for every GoPro have been added to the app. For example, at this time, the Hero11 has more features in the Open GoPro SDK That
> would need to be added if you are going to use a new GoPro. Alternatively, there could be a future GoPro version selector.

# Connecting to a GoPro
When connecting to a GoPro, open the GoPro to its page for pairing to the Quik app.
> **Warning**
> **Make sure you do not select connecting to a remote.**

In order to get to this option, swipe down from the top on the rear screen of the GoPro, then swipe right to left and click on the **Connections** option. On this 
screen select connect device and select the GoPro Quik App. When this is done you should see this screen.

![Quik App Pairing Screen](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/Quik%20App%20Pairing%20Screen.png)

If you have not already done so, open the app.
> **Note**
>
> In this state, one the theme switcher, GoPro selector, and connection button should be functional. This is to prevent you from sending commands before the GoPro
> is connected to.

Press the "Open Connection" button. When you have done this, the following prompt will appear.

![Connection Prompt](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/Connection%20Question.png)

If you forgot to start pairing, you can start it now or press cancel. If you press ok, the code will connect to the GoPro
> **Warning**
>
> The GoPro will say it is connected before the code has finished connecting. Make sure the code confirms the connection has occurred when the following message
> appears.

![Connection Confirmation](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/Connection%20Confirmation.png)

Once the connection is confirmed, press ok and the GoPro is default to the lowest resolution and frame rate values and the indicators will refresh for you. You will
have to manually refresh them after this, but they will auto refresh when resolution and frame rate change.

## Troubleshooting the Connection
The GoPro will not always connect correctly when the connection is opened in the app even if the GoPro says the connection occurred. This is because the GoPro will
confirm early in the connection process, but the full connection requires a bluetooth and wifi connection to the GoPro. If the connection confirmation appears, then
you know the connection occurred correctly. If not, then try the following:

1. Retry pairing form the beginning
2. Restart the app and then pairing
3. Turn the GoPro on and off
4. Reset the connections in the connections menu
5. Make sure you are using a python version at or above 3.10, but before 3.11

# Using the App
After the app is connected to a GoPro, all of the settings widgets will become active and allow you to change the settings. When you change the resolution, the list of
frame rate options will change based on what that resolution can do. If the frame rate you want is not available at that resolution, you will likely need to change the
resolution. Refer to the [battery life table](#battery-life-table) below for a list of all possible resolution and frame rate combinations. The FOV values should have
no effect on the resolution or frame rate options so they should all be available at any time.

> **Note**
>
> The battery and SD card indicators will refresh when the app originally connects and when you change resolution and frame rate parameters, but if you stay at one
setting, you will need to poll the GoPro for they values your self with the "Refresh Battery Indicator" button. This is a manual process to save battery.

## Battery Life Table
<table>
    <thead>
        <tr>
            <th bgcolor="black"></th>
            <th colspan=5>Battery Life in Minutes:</th>
        </tr>
        <tr style="text-align: center">
            <th style="padding: 0 10px">Resolution</th>
            <th style="padding: 0 10px">24 fps</th>
            <th style="padding: 0 10px">30 fps</th>
            <th style="padding: 0 10px">60 fps</th>
            <th style="padding: 0 10px">120 fps</th>
            <th style="padding: 0 10px">240 fps</th>
        </tr>
    </thead>
    <tbody>
        <tr style="text-align: center">
            <td>1080p</td>
            <td>-</td>
            <td>120</td>
            <td>90</td>
            <td>64</td>
            <td>48</td>
        </tr>
        <tr style="text-align: center">
            <td>2.7K</td>
            <td>-</td>
            <td>-</td>
            <td>75</td>
            <td>60</td>
            <td>44</td>
        </tr>
        <tr style="text-align: center">
            <td>2.7 (4x3)</td>
            <td>-</td>
            <td>-</td>
            <td>75</td>
            <td>59</td>
            <td>-</td>
        </tr>
        <tr style="text-align: center">
            <td>4K</td>
            <td>76</td>
            <td>76</td>
            <td>72</td>
            <td>36</td>
            <td>-</td>
        </tr>
        <tr style="text-align: center">
            <td>4K (4x3)</td>
            <td>-</td>
            <td>-</td>
            <td>51</td>
            <td>-</td>
            <td>-</td>
        </tr>
        <tr style="text-align: center">
            <td>5K (4x3)</td>
            <td>-</td>
            <td>64</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
        </tr>
        <tr style="text-align: center">
            <td>5.3K</td>
            <td>-</td>
            <td>74</td>
            <td>47</td>
            <td>-</td>
            <td>-</td>
        </tr>
    </tbody>
</table>

# Converting the App to an Executable
If you would like to use the app on another computer that does not have python, you can convert the app into an executable. This is done by using the pyinstaller package. Unfortunately,
pyinstaller has difficulty finding all of the files for customtkinter, the package used to make the GUI, when using the --onefile option so you need to add the data directly using the
--add-data option. Follow these steps to make the executable
1. Find the location of customtkinter on your computer. You can do this by entering
   `pip show customtkinter` in the terminal.
   - It will likely be in the form of `C:/Users/<username>/Lib/site-packages`
   - If you are using a virtual environment, make sure it is part of the file path
2. Enter the call to pyinstaller using the following: `pyinstaller --noconfirm --onedir --windowed --add-data "<customtkinter location>/customtkinter;customtkinter/" <recording_app.py location>`
  - If you want to also include the icon, you can add the option `--icon="<repository location>/GoPro-App/Docs/Media/film-roll.ico"`
  - If you want to change the name of the app, add the option `--name <new app name>`
3. This will make a build and dist folder in your current directory.
   - I ran this code when in the Code folder and committed my current version of the dist folder
4. The dist folder contains your new .exe file in the recording app folder. It will 
   have the same name as the python app.
   > **Note**
   >
   > When running the .exe, it will make a Data folder in the directory right above
   > it in the dist folder. If you move the .exe it would likely make it in whatever
   > directory was right above its new location. You should probably not move the 
   > exe as the full directory of packages in the recording_app folder will be
   > needed.
5. If you would like a shortcut you can put anywhere, right click on the .exe and
   select the option to make a shortcut. This will make a shortcut in the current
   folder.
   - If you want to change the icon to the same icon as the app, go to the properties
     of the shortcut and select the change icon button in the shortcut tab. Select 
     your new icon from there

![Shortcut Icon Change](https://github.com/iSensTeam/GoPro-App/blob/main/Docs/Media/Icon%20Change.png)

# Requirements
- [Python 3.10.0](https://www.python.org/downloads/release/python-3109/)
  - Python 3.11 is not supported currently by Open GoPro
- [customtkinter version: 5.0.4](https://pypi.org/project/customtkinter/0.3/) ![dependency check for customtkinter](https://img.shields.io/librariesio/release/PyPi/customtkinter/5.0.4)
- [open-gopro 0.12.0](https://community.gopro.com/s/article/Welcome-To-Open-GoPro?language=en_US) ![dependency check for open-gopro](https://img.shields.io/librariesio/release/PyPi/open-gopro/0.12.0)

## Executable Generation Requirements
- [pyinstaller version 5.7.0](https://pyinstaller.org/en/stable/installation.html) ![dependency check for pyinstaller](https://img.shields.io/librariesio/release/pypi/pyinstaller/5.7.0)

# Important Note on HIPAA Compliance
> **Warning**
>
> For its intended purpose, this app is made to record videos of a participant which is **Protected Data**. In order to be allowed to use this app to record a
> participant either in the operating room or in the lab during experiments, you **must use a VA approved device** to run the app. If this is not possible, you must
> disable the button to save video files on your local device running the app. For all questions relating to HIPAA compliance, refer to the Clinical and Regulatory 
> staff for what is and is not allowed when interacting with participants.

# Author
Code and documentation written by [Nabeel Chowdhury](https://www.nabeelchowdhury.com/)

# Acknowledgements
App icon from: <a href="https://www.flaticon.com/free-icons/analog" title="analog icons">Analog icons created by juicy_fish - Flaticon</a>
