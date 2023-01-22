import customtkinter as ctk
from tkinter import messagebox
from open_gopro import WirelessGoPro, Params
import os
import datetime as dt

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class GoProApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.gopro_name = "GoPro 5990"
        self.gopro = WirelessGoPro(target=self.gopro_name)
        # Global App Parameters)
        self.title("GoPro Control App")
        self.config(padx=10, pady=10)
        self.resizable(False, False)
        # Drop Down Menus
        # Resolution
        default_resolution = ctk.StringVar(value="1080p")
        self.resolution_dropdown = ctk.CTkOptionMenu(
            self, values=["1080p", "2.7K", "2.7K (4x3)", "4K",
                          "4K (4x3)", "5K (4x3)", "5.3K"],
            command=self.set_resolution, variable=default_resolution,
            state="disabled")
        self.resolution_dropdown.grid(row=0, column=0, padx=10, pady=10,
                                      sticky="nsew")
        # Frame Rate
        default_frame_rate = ctk.StringVar(value="30 fps")
        self.frame_rate_dropdown = ctk.CTkOptionMenu(
            self, values=["24 fps", "30 fps", "60 fps" "120 fps", "240 fps"],
            command=self.set_frame_rate, variable=default_frame_rate,
            state="disabled")
        self.frame_rate_dropdown.grid(row=0, column=1, padx=10, pady=10,
                                      sticky="nsew")
        # Select FOV
        default_fov = ctk.StringVar(value="Wide")
        self.fov_selector = ctk.CTkOptionMenu(
            self, values=["Linear", "Horizon Leveling", "Narrow",
                          "Super View", "Wide"], variable=default_fov,
            command=self.set_fov, state="disabled")
        self.fov_selector.grid(row=0, column=2, padx=10, pady=10,
                               sticky="nsew")
        # Recording Switch
        self.recording_variable = ctk.StringVar(value="off")
        self.recording_switch = ctk.CTkSwitch(
            self, text="Record Video", variable=self.recording_variable,
            onvalue="on", offvalue="off", command=self.recording_switch_event,
            state="disabled", switch_width=50, switch_height=25)
        self.recording_switch.grid(row=1, column=0, padx=10, pady=10,
                                   sticky="nsew")
        # Photo Button
        self.photo_button = ctk.CTkButton(self, text="Take a Photo",
                                          command=self.take_photo,
                                          state="disabled")
        self.photo_button.grid(row=1, column=1, padx=10, pady=10,
                               sticky="nsew")
        # Save Files
        self.file_name_entry = ctk.CTkEntry(self,
                                            placeholder_text="Enter File Name")
        self.file_name_entry.grid(row=1, column=2, padx=10, pady=10,
                                  sticky="nsew")
        self.save_files_button = ctk.CTkButton(self, text="Save Out Files",
                                               command=self.save_files,
                                               state="enabled")
        self.save_files_button.grid(row=3, column=2, padx=10, pady=10,
                                    sticky="nsew")
        self.stamp_check = ctk.StringVar(value="off")
        self.timestamp_check = ctk.CTkCheckBox(self, text="Timestamp Save?",
                                               variable=self.stamp_check,
                                               onvalue="on", offvalue="off")
        self.timestamp_check.grid(row=3, column=3, padx=10, pady=10)
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
        self.poll_battery.grid(row=2, column=0, padx=10, pady=10,
                               sticky="nsew")
        self.battery_indicator = BatteryIndicator(self)
        self.battery_indicator.grid(row=2, column=1, columnspan=3,
                                    padx=10, pady=10, sticky="nsew")
        # Connection Button
        self.connect = ctk.CTkButton(self, text="Open Connection",
                                     command=self.connect_callback)
        self.connect.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        default_gopro_name = ctk.StringVar(value="GoPro 5990")
        self.gopro_list = ctk.CTkOptionMenu(
            self, values=["GoPro 5990", "Connect to First Available"],
            command=self.select_gopro, variable=default_gopro_name)
        self.gopro_list.grid(row=3, column=0, padx=10, pady=10,
                             sticky="nsew")

    def set_resolution(self, choice):
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

        self.poll_battery_callback()

    def set_frame_rate(self, choice):
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

        self.poll_battery_callback()

    def set_fov(self, choice):
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

    def take_photo(self):
        self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.PHOTO)
        self.gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        self.gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)
        self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.VIDEO)

    def save_files(self):
        timestamp = ""
        if self.stamp_check.get() == "on":
            now = dt.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S") + "_"
        directory_name = self.file_name_entry.get()
        gopro_file_list =\
            self.gopro.http_command.get_media_list().data["files"]
        file_names = [file["n"] for file in gopro_file_list]
        local_directory = f"../Data/{directory_name}/"
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)
        for file in file_names:
            if file not in self.previously_saved_files:
                local_file = local_directory + timestamp + file
                self.gopro.http_command.download_file(camera_file=file,
                                                      local_file=local_file)
                self.previously_saved_files.append(file)

    def connect_callback(self):
        answer = messagebox.askokcancel(
            title="Proceed?", message="Is the GoPro in pairing mode?")
        if not answer:
            return

        if not self.gopro.is_ble_connected:
            self.gopro.open()

        if self.gopro.is_ble_connected:
            messagebox.showinfo(title="Connection Successful",
                                message="GoPro Connected")
            self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.VIDEO)
            self.connect._state = "disabled"
            self.set_resolution(self.resolution_dropdown.get())
            self.set_frame_rate(self.frame_rate_dropdown.get())
            self.set_fov(self.fov_selector.get())
            self.frame_rate_dropdown.configure(state="enabled")
            self.resolution_dropdown.configure(state="enabled")
            self.fov_selector.configure(state="enabled")
            self.recording_switch.configure(state="enabled")
            self.photo_button.configure(state="enabled")
            self.poll_battery.configure(state="enabled")
            self.poll_battery_callback()
        else:
            messagebox.showerror(title="Failed to Connect",
                                 message="The GoPro did not connect")

    def close_callback(self):
        if self.gopro.is_ble_connected:
            self.gopro.close()

        if self.gopro.is_ble_connected:
            messagebox.showerror(title="Failed to Disconnect",
                                 message="The GoPro did not disconnect.")

    def select_gopro(self, choice):
        match choice:
            case "GoPro 5990":
                self.gopro_name = "GoPro 5990"
            case _:
                self.gopro_name = None

        self.gopro = WirelessGoPro(target=self.gopro_name)

    def recording_switch_event(self):
        if self.recording_variable.get() == "on":
            self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.VIDEO)
            self.recording_switch.configure(text="Recording",
                                            button_color="red")
            self.gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        else:
            self.recording_switch.configure(text="Standby",
                                            button_color="white")
            self.gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)

    def poll_battery_callback(self):
        battery_percent_dict = self.gopro.ble_status.int_batt_per.get_value()
        battery_percent = list(battery_percent_dict.values())[0] / 100
        time_remaining_dict = self.gopro.ble_status.video_rem.get_value().data
        time_remaining = list(time_remaining_dict.values())[0]
        self.battery_indicator.update(battery_percent,
                                      self.resolution_dropdown.get(),
                                      self.frame_rate_dropdown.get(),
                                      time_remaining=time_remaining)


class BatteryIndicator(ctk.CTkFrame):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent")
        # Battery Percentage
        self.battery_percent_text = ctk.CTkLabel(self, text="")
        self.battery_percent_text.grid(row=0, column=0, sticky="nsew")
        self.battery_bar = ctk.CTkProgressBar(self, progress_color="green")
        self.battery_bar.grid(row=1, column=0)
        # Battery Life
        self.battery_time_label = ctk.CTkLabel(self, text="Battery Life")
        self.battery_time_label.grid(row=0, column=1, padx=10)
        self.battery_time_text = ctk.CTkLabel(self, text="0m")
        self.battery_time_text.grid(row=1, column=1, padx=10,
                                    sticky="nsew")
        # SD Card Remaining Time
        self.sd_time_label = ctk.CTkLabel(self, text="Time Remaining on Card")
        self.sd_time_label.grid(row=0, column=2, padx=10)
        self.sd_time_text = ctk.CTkLabel(self, text="0 minutes")
        self.sd_time_text.grid(row=1, column=2, padx=10, sticky="nsew")
        self.update(0.0, "", "", 0)

    def update(self, battery_percent: float, resolution: str, fps: str,
               time_remaining: int):
        if battery_percent > 0.6:
            self.battery_bar.configure(progress_color="green")
        elif battery_percent > 0.2:
            self.battery_bar.configure(progress_color="yellow")
        else:
            self.battery_bar.configure(progress_color="red")
        self.battery_percent_text.\
            configure(text=f"{int(battery_percent*100)}%")
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

        hours, minutes, seconds =\
            str(dt.timedelta(seconds=time_remaining)).split(":")
        time_on_card = (f"{hours}h {minutes}m {seconds}s")
        self.sd_time_text.configure(text=time_on_card)


if __name__ == "__main__":
    app = GoProApp()
    try:
        app.mainloop()
    finally:
        app.close_callback()
