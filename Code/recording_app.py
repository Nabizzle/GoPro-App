import customtkinter as ctk
from open_gopro import WirelessGoPro, Params

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class GoProApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.gopro_name = "GoPro 5990"
        self.gopro = WirelessGoPro(target=self.gopro_name)
        # Global App Parameters
        self.title("GoPro Control App")
        self.config(padx=10, pady=10)
        # Drop Down Menus
        default_resolution = ctk.StringVar(value="1080p")
        self.resolution_dropdown = ctk.CTkOptionMenu(
            self, values=["1080p", "2.7K", "2.7K (4x3)", "4K",
                          "4K (4x3)", "5K (4x3)", "5.3K"],
            command=self.set_resolution, variable=default_resolution,
            state="disabled")
        self.resolution_dropdown.grid(row=0, column=0, padx=10, pady=10)

        default_frame_rate = ctk.StringVar(value="30 fps")
        self.frame_rate_dropdown = ctk.CTkOptionMenu(
            self, values=["24 fps", "30 fps", "60 fps" "120 fps", "240 fps"],
            command=self.set_frame_rate, variable=default_frame_rate,
            state="disabled")
        self.frame_rate_dropdown.grid(row=0, column=1, padx=10, pady=10)
        # Recording Switch
        self.recording_variable = ctk.StringVar(value="off")
        self.recording_switch = ctk.CTkSwitch(
            self, text="Record Video", variable=self.recording_variable,
            onvalue="on", offvalue="off", command=self.recording_switch_event,
            state="disabled", switch_width=50, switch_height=25)
        self.recording_switch.grid(row=0, column=2, padx=10, pady=10)
        # Battery Indicator
        self.poll_battery = ctk.CTkButton(
            self, text="Refresh Battery Indicator",
            command=self.poll_battery_callback, state="disabled")
        self.poll_battery.grid(row=1, column=0, padx=10, pady=10)
        self.battery_indicator = BatteryIndicator(self)
        self.battery_indicator.grid(row=1, column=1, columnspan=2)
        # Connection Button
        self.connect = ctk.CTkButton(self, text="Open Connection",
                                     command=self.connect_callback)
        self.connect.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        default_gopro_name = ctk.StringVar(value="5990")
        self.gopro_list = ctk.CTkOptionMenu(
            self, values=["5990", "Connect to First"],
            command=self.select_gopro, variable=default_gopro_name)
        self.gopro_list.grid(row=2, column=0, padx=10, pady=10)

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
                print("This is not an available resolution")

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
                print("This is not an available frame rate")

        self.poll_battery_callback()

    def connect_callback(self):
        print("Trying GoPro Connection")
        if not self.gopro.is_ble_connected:
            self.gopro.open()

        if self.gopro.is_ble_connected:
            print("GoPro Connected")
            self.gopro.ble_command.load_preset_group(
                group=Params.PresetGroup.VIDEO)
            self.connect._state = "disabled"
            self.set_resolution(self.resolution_dropdown.get())
            self.set_frame_rate(self.frame_rate_dropdown.get())
            self.frame_rate_dropdown.configure(state="enabled")
            self.resolution_dropdown.configure(state="enabled")
            self.recording_switch.configure(state="enabled")
            self.poll_battery.configure(state="enabled")
            self.poll_battery_callback()
        else:
            print("The GoPro did not connect")

    def close_callback(self):
        if self.gopro.is_ble_connected:
            self.gopro.close()

        if not self.gopro.is_ble_connected:
            print("GoPro Disconnected")
        else:
            print("The GoPro did not disconnect.")

    def select_gopro(self, choice):
        match choice:
            case "5990":
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
        self.battery_indicator.update(battery_percent,
                                      self.resolution_dropdown.get(),
                                      self.frame_rate_dropdown.get())


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
        self.battery_percent_text = ctk.CTkLabel(self, text="")
        self.battery_percent_text.grid(row=0, column=0)
        self.battery_bar = ctk.CTkProgressBar(self, progress_color="green")
        self.battery_bar.grid(row=1, column=0)
        self.battery_time_text = ctk.CTkLabel(self, text="0m")
        self.battery_time_text.grid(row=0, column=1, rowspan=2, padx=10)
        self.update(0.0, "", "")

    def update(self, battery_percent: float, resolution: str, fps: str):
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


if __name__ == "__main__":
    app = GoProApp()
    try:
        app.mainloop()
    finally:
        app.close_callback()
