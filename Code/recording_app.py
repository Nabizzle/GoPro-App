import customtkinter as ctk
from tkinter import messagebox
from open_gopro import WirelessGoPro, Params
import os
import datetime as dt

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class GoProApp(ctk.CTk):
    '''
    App to control a GoPro from a distance

    This app allows a user to control how and when a GoPro records video and
    images. The app allows you to timestamp the files from the GoPro based on
    when they wer saved from the computer and organize them in folders when
    downloading them from the GoPro.

    Attributes
    ----------
    PADX: int
        The number of pixels to pad on the left and right sides of the GUI
        elements
    PADY: int
        The number of pixels to pad on the top and bottom sides of the GUI
        elements
    gopro_name: str
        The name of the GoPro to connect to
    gopro: WirelessGoPro
        A wireless GoPro object to connect to
    resolution_dropdown: CTkOptionMenu
        A list of possible resolutions for the GoPro
    frame_rate_dropdown: CTkOptionMenu
        A list of possible frame rates for the GoPro
    fov_dropdown: CTkOptionMenu
        A list of possible fields of view for the GoPro
    recording_variable: StringVar
        Value of the recording switch
    recording_switch: CTkSwitch
        A switch widget to tell the GoPro to start and stop recording
    photo_button: CTkButton
        A button to tell the GoPro to take a photo and go back to video mode
    file_group_entry: CTkEntry
        An entry box to label the group of files being saved
    save_files_button: CTkButton
        A button to pull all of the new files from the GoPro
    stamp_check: StringVar
        Value of the timestamp_check
    timestamp_check: CTkCheckBox
        Checkbox for telling the code if a time stamp should be added to the
        start of the files being saved.
    previously_saved_files: List[str]
        A list of all of the previously saved files in the Data folder
    poll_battery: CTkButton
        A button to get the battery life and SD card recording room values
    battery_indicator: BatteryIndicator
        The GUI elements to display the battery and SD card statuses
    connect: CTkButton
        A button to connect to the selected GoPro
    gopro_list: List[str]
        List of all possible GoPros to connect to. You can also connect to the
        first available.

    Methods
    -------
    __init__()
        Creates all of the base GUI elements
    set_resolution(choice)
        Switches the GoPro to a selected resolution
    set_frame_rate(choice)
        Switches the GoPro to a selected frame rate
    set_fov(choice)
        Switches the GoPro to a field of view
    take_photo()
        Take an image with the current settings
    save_files()
        Save out new files from the GoPro
    select_gopro(choice)
        Select a GoPro to connect to
    connect_callback()
        Connect to the selected GoPro form the select_gopro dropdown
    close_callback()
        Disconnects from the GoPro
    recording_switch_event
        Turns video recording on and off with the current video settings
    poll_battery_callback()
        Update the battery and SD card indicators

    See Also
    --------
    BatteryIndicator

    Notes
    -----
    - The app needs to be restarted if you need to reconnect to the GoPro.
    - The app will check your Data folder to make sure that it does not save
      the same video twice.
    - In order to save different videos into different folders, you need to
      save them after a group of those videos have been recorded as all new
      videos are pulled at once.
    - The newer GoPros can have more resolution, fps and fov  values. These
      values are for the Hero10.

    References
    ----------
    [Open GoPro SDK](https://gopro.github.io/OpenGoPro/python_sdk/)
    '''
    PADX = 10
    PADY = 10

    def __init__(self) -> None:
        '''
        Creates all of the base GUI elements

        Creates the GUI and links the elements to the correct callbacks
        '''
        super().__init__()
        # selected GoPro to connect to
        self.gopro_name = "GoPro 5990"
        self.gopro = WirelessGoPro(target=self.gopro_name)

        # Global App Parameters)
        self.title("GoPro Control App")
        self.config(padx=self.PADX, pady=self.PADY)
        self.resizable(False, False)

        # Resolution Dropdown
        default_resolution = ctk.StringVar(value="1080p")
        self.resolution_dropdown = ctk.CTkOptionMenu(
            self, values=["1080p", "2.7K", "2.7K (4x3)", "4K",
                          "4K (4x3)", "5K (4x3)", "5.3K"],
            command=self.set_resolution, variable=default_resolution,
            state="disabled")
        self.resolution_dropdown.grid(row=0, column=0, padx=self.PADX,
                                      pady=self.PADY, sticky="nsew")

        # Frame Rate Dropdown
        default_frame_rate = ctk.StringVar(value="30 fps")
        self.frame_rate_dropdown = ctk.CTkOptionMenu(
            self, values=["24 fps", "30 fps", "60 fps" "120 fps", "240 fps"],
            command=self.set_frame_rate, variable=default_frame_rate,
            state="disabled")
        self.frame_rate_dropdown.grid(row=0, column=1, padx=self.PADX,
                                      pady=self.PADY, sticky="nsew")

        # Select FOV
        default_fov = ctk.StringVar(value="Wide")
        self.fov_dropdown = ctk.CTkOptionMenu(
            self, values=["Linear", "Horizon Leveling", "Narrow",
                          "Super View", "Wide"], variable=default_fov,
            command=self.set_fov, state="disabled")
        self.fov_dropdown.grid(row=0, column=2, padx=self.PADX, pady=self.PADY,
                               sticky="nsew")

        # Recording Switch
        self.recording_variable = ctk.StringVar(value="off")
        self.recording_switch = ctk.CTkSwitch(
            self, text="Record Video", variable=self.recording_variable,
            onvalue="on", offvalue="off", command=self.recording_switch_event,
            state="disabled", switch_width=50, switch_height=25)
        self.recording_switch.grid(row=1, column=0, padx=self.PADX,
                                   pady=self.PADY, sticky="nsew")

        # Photo Button
        self.photo_button = ctk.CTkButton(self, text="Take a Photo",
                                          command=self.take_photo,
                                          state="disabled")
        self.photo_button.grid(row=1, column=1, padx=self.PADX, pady=self.PADY,
                               sticky="nsew")

        # Save Out Files
        self.file_group_entry = ctk.CTkEntry(
            self, placeholder_text="Enter File Group Name")
        self.file_group_entry.grid(row=1, column=2, columnspan=2,
                                   padx=self.PADX, pady=self.PADY,
                                   sticky="nsew")
        self.save_files_button = ctk.CTkButton(self, text="Save Out Files",
                                               command=self.save_files,
                                               state="enabled")
        self.save_files_button.grid(row=3, column=2, padx=self.PADX,
                                    pady=self.PADY, sticky="nsew")
        self.stamp_check = ctk.StringVar(value="off")
        self.timestamp_check = ctk.CTkCheckBox(self, text="Timestamp Save?",
                                               variable=self.stamp_check,
                                               onvalue="on", offvalue="off")
        self.timestamp_check.grid(row=3, column=3, padx=self.PADX,
                                  pady=self.PADY)
        if not os.path.exists("../Data"):
            os.makedirs("../Data")
        self.previously_saved_files = []
        for (_, _, filenames) in os.walk("../Data"):
            files = [parts.split("_")[-1] for parts in filenames]
            self.previously_saved_files.extend(files)

        # Battery Indicator
        self.poll_battery = ctk.CTkButton(
            self, text="Refresh Battery Indicator",
            command=self.poll_battery_callback, state="disabled")
        self.poll_battery.grid(row=2, column=0, padx=self.PADX, pady=self.PADY,
                               sticky="nsew")
        self.battery_indicator = BatteryIndicator(self)
        self.battery_indicator.grid(row=2, column=1, columnspan=3,
                                    padx=self.PADX, pady=self.PADY,
                                    sticky="nsew")

        # Connecting to the GoPro
        self.connect = ctk.CTkButton(self, text="Open Connection",
                                     command=self.connect_callback)
        self.connect.grid(row=3, column=1, padx=self.PADX, pady=self.PADY,
                          sticky="nsew")
        default_gopro_name = ctk.StringVar(value="GoPro 5990")
        self.gopro_list = ctk.CTkOptionMenu(
            self, values=["GoPro 5990", "Connect to First Available"],
            command=self.select_gopro, variable=default_gopro_name)
        self.gopro_list.grid(row=3, column=0, padx=self.PADX, pady=self.PADY,
                             sticky="nsew")

    def set_resolution(self, choice: str) -> None:
        '''
        Switches the GoPro to a selected resolution

        Switches the resolution of the GoPro and restricts the frame rate
        dropdown so that only the frame rates for that resolution are possible.
        Once a new resolution has been selected, the battery indicator updates.

        Parameters
        ----------
        choice: str
            The selected resolution from the resolution_dropdown widget.

        Raises
        ------
        KeyError
            If there is a resolution selected that was not implemented

        See Also
        --------
        self.set_frame_rate
        BatteryIndicator

        Notes
        -----
        Newer and older GoPros have different possible resolution and frame
        rate possibilities. This code was written for a Hero10, but different
        options should be easy to add.
        '''
        # Restrict the frame rates based on the selected resolution
        match choice:
            case "1080p":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_1080)
                self.frame_rate_dropdown.configure(values=[
                    "30 fps",
                    "60 fps",
                    "120 fps",
                    "240 fps"
                ], variable=ctk.StringVar(value="30 fps"))
                self.set_frame_rate(self.frame_rate_dropdown.get())
            case "2.7K":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_2_7K)
                self.frame_rate_dropdown.configure(values=[
                    "60 fps",
                    "120 fps",
                    "240 fps"
                ], variable=ctk.StringVar(value="60 fps"))
                self.set_frame_rate(self.frame_rate_dropdown.get())
            case "2.7K (4x3)":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_2_7K_4_3)
                self.frame_rate_dropdown.configure(values=[
                    "60 fps",
                    "120 fps"
                ], variable=ctk.StringVar(value="60 fps"))
                self.set_frame_rate(self.frame_rate_dropdown.get())
            case "4K":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_4K)
                self.frame_rate_dropdown.configure(values=[
                    "24 fps",
                    "30 fps",
                    "60 fps",
                    "120 fps"
                ], variable=ctk.StringVar(value="24 fps"))
                self.set_frame_rate(self.frame_rate_dropdown.get())
            case "4K (4x3)":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_4K_4_3)
                self.frame_rate_dropdown.configure(
                    values=["60 fps"], variable=ctk.StringVar(value="60 fps"))
                self.set_frame_rate(self.frame_rate_dropdown.get())
            case "5K (4x3)":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_5_K_4_3)
                self.frame_rate_dropdown.configure(
                    values=["30 fps"], variable=ctk.StringVar(value="30 fps"))
                self.set_frame_rate(self.frame_rate_dropdown.get())
            case "5.3K":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_5_3_K)
                self.frame_rate_dropdown.configure(values=[
                    "30 fps",
                    "60 fps"
                ], variable=ctk.StringVar(value="30 fps"))
                self.set_frame_rate(self.frame_rate_dropdown.get())
            case _:
                messagebox.showerror(
                    title="Unknown Resolution",
                    message="This is not an available resolution")
                raise KeyError
        # Refresh the battery indicator with the new video parameters
        self.poll_battery_callback()

    def set_frame_rate(self, choice: str) -> None:
        '''
        Switches the GoPro to a selected frame rate

        Switches the frame rate of the GoPro. Once a new resolution has been
        selected, the battery indicator updates.

        Parameters
        ----------
        choice: str
            The selected frame rate from the frame_rate_dropdown widget.

        Raises
        ------
        KeyError
            If there is a frame rate selected that was not implemented

        See Also
        --------
        self.set_resolution
        BatteryIndicator

        Notes
        -----
        Newer and older GoPros have different possible resolution and frame
        rate possibilities. This code was written for a Hero10, but different
        options should be easy to add.
        '''
        match choice:
            case "24 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_24)
            case "25 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_25)
            case "30 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_30)
            case "50 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_50)
            case "60 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_60)
            case "100 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_100)
            case"120 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_120)
            case "200 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_200)
            case "240 fps":
                self.gopro.ble_setting.fps.set(
                    Params.FPS.FPS_240)
            case _:
                messagebox.showerror(
                    title="Unknown Frame Rate",
                    message="This is not an available frame rate")
                raise KeyError
        # Refresh the battery indicator
        self.poll_battery_callback()

    def set_fov(self, choice: str) -> None:
        '''
        Switches the GoPro to a field of view

        Switches the frame rate of the GoPro. Once a new resolution has been
        selected, the battery indicator updates.

        Parameters
        ----------
        choice: str
            The selected frame rate from the frame_rate_dropdown widget.

        Raises
        ------
        KeyError
            If there is a frame rate selected that was not implemented

        Notes
        -----
        Newer and older GoPros have different possible fov possibilities. This
        code was written for a Hero10, but different options should be easy to
        add.
        '''
        match choice:
            case "Linear":
                self.gopro.ble_setting.video_field_of_view.set(
                    Params.VideoFOV.LINEAR)
            case "Horizon Leveling":
                self.gopro.ble_setting.video_field_of_view.set(
                    Params.VideoFOV.LINEAR_HORIZON_LEVELING)
            case "Narrow":
                self.gopro.ble_setting.video_field_of_view.set(
                    Params.VideoFOV.NARROW)
            case "Super View":
                self.gopro.ble_setting.video_field_of_view.set(
                    Params.VideoFOV.SUPERVIEW)
            case "Wide":
                self.gopro.ble_setting.video_field_of_view.set(
                    Params.VideoFOV.WIDE)
            case _:
                messagebox.showerror(title="Unknown FOV",
                                     message="This FOV is not available")
                raise KeyError

    def take_photo(self) -> None:
        '''
        Take an image with the current settings

        Switch to the photo mode in the current settings, take a photo, and
        switch back to video mode.
        '''
        self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.PHOTO)
        self.gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        self.gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)
        self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.VIDEO)

    def save_files(self) -> None:
        '''
        Save out new files from the GoPro

        Saves out any previously unsaved files from the GoPro into a selected
        subdirectory in the Data folder. This is specified by the entry box on
        The GUI. If nothing is entered in that box, they are added to the Data
        folder directly. If the timestamp box is checked, a timestamp of when
        the save button was pressed is added to the front of the file in the
        form of YYYYMMDD_HHMMSS where the first set of M's is month and the
        second is minute.

        Notes
        -----
        If the specified directory does not exist, the code will make it in the
        Data folder.
        '''
        # Make a timestamp
        timestamp = ""
        if self.stamp_check.get() == "on":
            now = dt.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S") + "_"
        # Get the user entered directory name
        directory_name = self.file_group_entry.get()
        # Get all of the files on the GoPro
        gopro_file_list =\
            self.gopro.http_command.get_media_list().data["files"]
        file_names = [file["n"] for file in gopro_file_list]
        # Make a directory for the files to save into
        local_directory = f"../Data/{directory_name}/"
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)
        # Save out any new files
        for file in file_names:
            if file not in self.previously_saved_files:
                local_file = local_directory + timestamp + file
                self.gopro.http_command.download_file(camera_file=file,
                                                      local_file=local_file)
                self.previously_saved_files.append(file)

    def select_gopro(self, choice: str) -> None:
        '''
        Select a GoPro to connect to

        Take in the selected GoPro name and makes a new WirelessGoPro object
        for it. If the name has not been implemented, the first available GoPro
        will be connected to.

        Parameters
        ----------
        choice: str
            The selected GoPro name to connect to

        Notes
        -----
        Default GoPro names are in the form of "GoPro XXXX".
        '''
        match choice:
            case "GoPro 5990":
                self.gopro_name = "GoPro 5990"
            case _:
                self.gopro_name = None

        self.gopro = WirelessGoPro(target=self.gopro_name)

    def connect_callback(self) -> None:
        '''
        Connect to the selected GoPro form the select_gopro dropdown

        Will only connect when the user confirms the GoPro is in pairing mode.
        When the GoPro is connected, the rest of the GUI becomes enabled. This
        is to prevent the user from entering commands before they should be
        able to.

        Warns
        -----
        Error messagebox if the GoPro does not connect to bluetooth

        Warnings
        --------
        You may have to connect to the GoPro at twice if it does not work the
        first time even if the GoPro says it connected. If the App does not
        give confirmation, it did not work. Close the app and pair again.

        Notes
        -----
        - Even if the GoPro says it is connected, wait for a confirmation to
          appear on screen.
        - The pairing mode for the GoPro is when connecting to the Quik App and
          not connecting to a remote.
        '''
        # Ask the user if they are in pairing mode and only continue if True
        answer = messagebox.askokcancel(
            title="Proceed?", message="Is the GoPro in pairing mode?")
        if not answer:
            return

        # Connect to the GoPro if it is not already connected
        if not self.gopro.is_ble_connected:
            self.gopro.open()

        # If the GoPro is not connected, enable the rest of teh GUI
        if self.gopro.is_ble_connected:
            messagebox.showinfo(title="Connection Successful",
                                message="GoPro Connected")
            self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.VIDEO)
            self.connect._state = "disabled"
            self.set_resolution(self.resolution_dropdown.get())
            self.set_frame_rate(self.frame_rate_dropdown.get())
            self.set_fov(self.fov_dropdown.get())
            self.frame_rate_dropdown.configure(state="enabled")
            self.resolution_dropdown.configure(state="enabled")
            self.fov_dropdown.configure(state="enabled")
            self.recording_switch.configure(state="enabled")
            self.photo_button.configure(state="enabled")
            self.poll_battery.configure(state="enabled")
            self.start_cam_button.configure(state="enabled")
            self.poll_battery_callback()
        else:
            messagebox.showerror(title="Failed to Connect",
                                 message="The GoPro did not connect")

    def close_callback(self) -> None:
        '''
        Disconnects from the GoPro

        Warns
        -----
        Error messagebox if the GoPro does not disconnect

        Warnings
        --------
        The closing code needs to run in order to connect again.
        '''
        if self.gopro.is_ble_connected:
            self.gopro.close()

        if self.gopro.is_ble_connected:
            messagebox.showerror(title="Failed to Disconnect",
                                 message="The GoPro did not disconnect.")

    def recording_switch_event(self):
        '''
        Turns video recording on and off with the current video settings
        '''
        # If the switch has turned on, record
        if self.recording_variable.get() == "on":
            # Make sure the GoPro is in video mode
            self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.VIDEO)
            self.recording_switch.configure(text="Recording",
                                            button_color="red")
            self.gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        else:
            self.recording_switch.configure(text="Standby",
                                            button_color="white")
            self.gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)

    def poll_battery_callback(self) -> None:
        '''
        Update the battery and SD card indicators

        Polls the battery percent and SD card's remaining space to update the
        GUI elements for battery percent, life, and SD card recording room.

        See Also
        --------
        BatteryIndicator.update()
        '''
        battery_percent_dict = self.gopro.ble_status.int_batt_per.get_value()
        battery_percent = list(battery_percent_dict.values())[0] / 100
        time_remaining_dict = self.gopro.ble_status.video_rem.get_value().data
        time_remaining = list(time_remaining_dict.values())[0]
        self.battery_indicator.update(battery_percent,
                                      self.resolution_dropdown.get(),
                                      self.frame_rate_dropdown.get(),
                                      time_remaining=time_remaining)


class BatteryIndicator(ctk.CTkFrame):
    '''
    Container for all battery and SD card status indicators

    Shows the remaining battery life and SD recording room. The battery life
    is found by showing the GoPro's battery percentage and a battery life time
    based on a table of battery life times during constant recording shown in
    the ReadMe

    Attributes
    ----------
    BATTERY_RECORDING_TIMES: Dict[Dict[int]]
        Battery life times from GoPro's support site
    PADX: int
        Pixel padding to the left and right of the widgets
    battery_percent_text: CTkLabel
        The text for the percent of the battery left
    battery_percent_bar: CTkProgressBar
        A bar to show the remaining battery left
    battery_time_label: CTkLabel
        The title for battery time left
    battery_time_text: CTkLabel
        The time left to record with the current settings
    sd_time_label: CTkLabel
        The title for the SD card recording room left
    sd_time_text
        Shows the amount of time you can record with the current settings

    Methods
    -------
    __init__(*args, **kwargs)
        Setup all of the elements of the battery indicator widget
    update(battery_percent, resolution, fps, time_remaining)
        Updates all of the GUI elements based on polled values

    See Also
    --------
    GoProApp

    References
    ----------
    https://community.gopro.com/s/article/gopro-camera-battery-life
    '''
    BATTERY_RECORDING_TIMES = {
        "1080p": {
            "30 fps": 120,
            "60 fps": 90,
            "120 fps": 64,
            "240 fps": 48,
        },
        "2.7K": {
            "60 fps": 75,
            "120 fps": 60,
            "240 fps": 44,
        },
        "2.7K (4x3)": {
            "60 fps": 75,
            "120 fps": 59,
        },
        "4K": {
            "24 fps": 76,
            "30 fps": 76,
            "60 fps": 72,
            "120 fps": 36,
        },
        "4K (4x3)": {
            "60 fps": 51,
        },
        "5K (4x3)": {
            "30 fps": 64,
        },
        "5.3K": {
            "30 fps": 74,
            "60 fps": 47,
        },
    }

    PADX = 10

    def __init__(self, *args, **kwargs) -> None:
        '''
        Setup all of the elements of the battery indicator widget
        '''
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent")

        # Battery Percentage
        self.battery_percent_text = ctk.CTkLabel(self, text="")
        self.battery_percent_text.grid(row=0, column=0, sticky="nsew")
        self.battery_bar = ctk.CTkProgressBar(self, progress_color="green")
        self.battery_bar.grid(row=1, column=0)

        # Battery Life
        self.battery_time_label = ctk.CTkLabel(self, text="Battery Life")
        self.battery_time_label.grid(row=0, column=1, padx=self.PADX)
        self.battery_time_text = ctk.CTkLabel(self, text="0m")
        self.battery_time_text.grid(row=1, column=1, padx=self.PADX,
                                    sticky="nsew")

        # SD Card Remaining Time
        self.sd_time_label = ctk.CTkLabel(self, text="Time Remaining on Card")
        self.sd_time_label.grid(row=0, column=2, padx=self.PADX)
        self.sd_time_text = ctk.CTkLabel(self, text="0 minutes")
        self.sd_time_text.grid(row=1, column=2, padx=self.PADX, sticky="nsew")
        self.update(0.0, "", "", 0)

    def update(self, battery_percent: float, resolution: str, fps: str,
               time_remaining: int) -> None:
        '''
        Updates all of the GUI elements based on polled values

        Takes in the polled values for the battery percent, video parameters,
        and the amount of recording room left on the SD Card in order to
        update the appearance of the battery indicator. The color of the
        percentage bar is affected by the battery percent as well. The time
        left on the battery is found using the resolution and fps values to
        reference the BATTERY_RECORDING_TIMES dictionary.

        Parameters
        ----------
        battery_percent: float
            The polled battery percentage from the GoPro
        resolution: str
            The selected resolution from the resolution_dropdown menu
        fps: str
            The selected frame rate from the frame_rate_dropdown menu
        time_remaining: int
            The time in seconds left to record with the current resolution and
            fps values. This is polled directly from the GoPro
        '''
        # Change the color of the battery percentage bar based on the
        # percentage. High > 60%, 60% > Medium > 20%, Low < 20%
        if battery_percent > 0.6:
            self.battery_bar.configure(progress_color="green")
        elif battery_percent > 0.2:
            self.battery_bar.configure(progress_color="yellow")
        else:
            self.battery_bar.configure(progress_color="red")

        # Display the battery percentage
        self.battery_percent_text.\
            configure(text=f"{int(battery_percent*100)}%")

        # Find and display the remaining battery time
        try:
            time =\
                self.BATTERY_RECORDING_TIMES[resolution][fps] * battery_percent
        except KeyError:
            self.battery_time_text.configure(text="0 minutes")
        else:
            minutes = int(time // 1)
            seconds = round(time % 1 * 60)
            self.battery_time_text.configure(text=f"{minutes}m {seconds}s")
        self.battery_bar.set(battery_percent)

        # Show the remaining time to record in hours, minutes, and seconds
        hours, minutes, seconds =\
            str(dt.timedelta(seconds=time_remaining)).split(":")
        time_on_card = (f"{hours}h {minutes}m {seconds}s")
        self.sd_time_text.configure(text=time_on_card)


if __name__ == "__main__":
    # Create app and close the GoPro connection safety when the app is closed
    app = GoProApp()
    try:
        app.mainloop()
    finally:
        app.close_callback()
