import customtkinter as ctk
from open_gopro import WirelessGoPro, Params

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class GoProApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        # GoPro Variables
        self.gopro = WirelessGoPro(target="GoPro 5990")
        # Global App Parameters
        self.title("GoPro Control App")
        self.config(padx=10, pady=10)
        # Drop Down Menus
        default_resolution = ctk.StringVar(value="Select Resolution")
        self.resolution_dropdown = ctk.CTkOptionMenu(
            self, values=["1080p", "2.7K", "2.7K (4x3)", "4K",
                          "4K (4x3)", "5K (4x3)", "5.3K"],
            command=self.set_resolution, variable=default_resolution,
            state="disabled")
        self.resolution_dropdown.grid(row=0, column=0, padx=10, pady=10)

        default_frame_rate = ctk.StringVar(value="Select Frame Rate")
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
        self.recording_switch.grid(row=1, column=0, padx=10, pady=10)
        # Connection Button
        self.connect = ctk.CTkButton(self, text="Open Connection",
                                     command=self.connect_callback)
        self.connect.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

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

    def connect_callback(self):
        print("Trying GoPro Connection")
        if not self.gopro.is_ble_connected:
            self.gopro.open()

        if self.gopro.is_ble_connected:
            print("GoPro Connected")
            self.connect._state = "disabled"
            self.frame_rate_dropdown.configure(state="enabled")
            self.resolution_dropdown.configure(state="enabled")
            self.recording_switch.configure(state="enabled")
        else:
            print("The GoPro did not connect")

    def close_callback(self):
        if self.gopro.is_ble_connected:
            self.gopro.close()

        if not self.gopro.is_ble_connected:
            print("GoPro Disconnected")
        else:
            print("The GoPro did not disconnect.")

    def recording_switch_event(self):
        if self.recording_variable.get() == "on":
            self.recording_switch.configure(text="Recording",
                                            button_color="red")
            self.gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        else:
            self.recording_switch.configure(text="Standby",
                                            button_color="white")
            self.gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)


if __name__ == "__main__":
    app = GoProApp()
    try:
        app.mainloop()
    finally:
        app.close_callback()
