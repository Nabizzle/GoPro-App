import customtkinter as ctk
from open_gopro import WirelessGoPro

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class GoProApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        # GoPro Variables
        self.gopro = WirelessGoPro(target="GoPro 5990")
        self.title("GoPro Control App")
        # Connection Buttons
        self.connect = ctk.CTkButton(self, text="Open Connection",
                                     command=self.connect_callback)
        self.connect.grid(row=0, column=0)

    def connect_callback(self):
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


if __name__ == "__main__":
    app = GoProApp()
    try:
        app.mainloop()
    finally:
        app.close_callback()
