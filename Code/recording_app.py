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
        # Connection Button
        self.connect = ctk.CTkButton(self, text="Open Connection",
                                     command=self.connect_callback)
        self.connect.grid(row=1, column=0, padx=10, pady=10)
        # Drop Down Menus
        default_resolution = ctk.StringVar(value="Select Resolution")
        self.resolution_dropdown = ctk.CTkOptionMenu(
            self, values=["1080p", "1440p", "2.7K", "2.7K (4x3)", "4K",
                          "4K (4x3)", "5K", "5K (4x3)", "5.3K", "5.3K (4x3)"],
            command=self.set_resolution, variable=default_resolution)
        self.resolution_dropdown.grid(row=0, column=0, padx=10, pady=10)

    def connect_callback(self):
        print("Trying GoPro Connection")
        if not self.gopro.is_ble_connected:
            self.gopro.open()

        if self.gopro.is_ble_connected:
            print("GoPro Connected")
            self.connect._state = "disabled"
        else:
            print("The GoPro did not connect")

    def close_callback(self):
        if self.gopro.is_ble_connected:
            self.gopro.close()

        if not self.gopro.is_ble_connected:
            print("GoPro Disconnected")
        else:
            print("The GoPro did not disconnect.")

    def set_resolution(self, choice):
        match choice:
            case "1080p":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_1080)
            case "1440p":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_1440)
            case "2.7K":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_2_7K)
            case "2.7K (4x3)":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_2_7K_4_3)
            case "4K":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_4K)
            case "4K (4x3)":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_4K_4_3)
            case"5K":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_5K)
            case "5K (4x3)":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_5_K_4_3)
            case "5.3K":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_5_3_K)
            case "5.3K (4x3)":
                self.gopro.ble_setting.resolution.set(
                    Params.Resolution.RES_5_3_K_4_3)
            case _:
                print("This is not an available resolution")


if __name__ == "__main__":
    app = GoProApp()
    try:
        app.mainloop()
    finally:
        app.close_callback()
