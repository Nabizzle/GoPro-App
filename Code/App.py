import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class GoProApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("GoPro Control App")


if __name__ == "__main__":
    app = GoProApp()
    app.mainloop()
