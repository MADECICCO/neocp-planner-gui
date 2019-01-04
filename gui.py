import tkinter as tk
from configparser import ConfigParser


class ScrollFrame(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super(ScrollFrame, self).__init__(master, *args, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.viewPort = tk.Frame(
            self.canvas,
            background="#ffffff")

        self.viewPort.bind("<Configure>", self.on_frame_configure)

        self.vsb = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview)
        self.vsb.pack(side="right", fill="y")

        self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vsb.set)

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class Option(tk.Frame):
    def __init__(self, master, text, entry_default, *args, **kwargs):
        super(Option, self).__init__(master, *args, **kwargs)
        # self.pack(expand=True, fill="x")
        self.label = tk.Label(self, text=text)
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self)
        self.entry.insert("end", entry_default)
        self.entry.pack(side=tk.RIGHT)


class Toolbar(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super(Toolbar, self).__init__(master, *args, **kwargs)

        self.file = tk.Button(self, text="File", bd=1, relief=tk.FLAT)
        self.file.pack(side="left")

        self.settings = tk.Button(self, text="Settings", bd=1, relief=tk.FLAT)
        self.settings.pack(side="left")


class Console(tk.Text):
    def __init__(self, master, *args, **kwargs):
        super(Console, self).__init__(master, *args, **kwargs)

        # self.pack()
        # self.configure(background="black", foreground="white")

        self.configure(font=("Consolas", 12))
        self.insert("end", "<<< Initialized!")
        self.configure(state=tk.DISABLED)

    def out(self, text):
        self.configure(state=tk.NORMAL)
        self.insert("end", "\n<<< " + str(text))
        self.configure(state=tk.DISABLED)
        self.see('end')


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

    def center(self):
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def main():
    config = ConfigParser()

    # Load Option presets
    config.read("config.ini")

    # [OBS]
    obs_code = config["OBS"]["obs_code"]
    continous = config["OBS"]["continuous"]

    # [Option]
    min_score = config["OPTIONS"]["min_score"]
    min_ef_mag = config["OPTIONS"]["min_ef_mag"]
    min_alt = config["OPTIONS"]["min_alt"]
    max_scat_xcoo = config["OPTIONS"]["max_scat_xcoo"]
    max_scat_ycoo = config["OPTIONS"]["max_scat_ycoo"]
    max_not_seen = config["OPTIONS"]["max_not_seen"]
    max_sun_alt = config["OPTIONS"]["max_sun_alt"]
    min_d_from_moon = config["OPTIONS"]["min_d_from_moon"]
    min_motion_speed = config["OPTIONS"]["min_motion_speed"]

    # Main app
    app = App()
    app.title("NEOCP Planner")
    app.geometry("1000x600")

    toolbar = Toolbar(app)
    toolbar.pack(side="top", fill="x")

    main_frame = tk.Frame(app)
    main_frame.pack(side="top", expand=True, fill="both", padx=5, pady=5)

    left_frame = tk.LabelFrame(main_frame, text="Options")
    left_frame.pack(side="left", fill="both", padx=5, pady=5)

    right_frame = tk.LabelFrame(main_frame, text="Minor Planets")
    right_frame.pack(side="right", fill="both", padx=5, pady=5, expand=True)

    option_0 = Option(left_frame, "Obs. code?", obs_code)
    option_0.pack(fill="x")

    option_1 = Option(left_frame, "Min. score?", min_score)
    option_1.pack(fill="x")

    option_2 = Option(left_frame, "Min. ef. magnitude?", min_ef_mag)
    option_2.pack(fill="x")

    option_3 = Option(left_frame, "Min. altitude?", min_alt)
    option_3.pack(fill="x")

    option_4 = Option(left_frame, "Max. scat. in x?", max_scat_xcoo)
    option_4.pack(fill="x")

    option_5 = Option(left_frame, "Max. scat. in y?", max_scat_ycoo)
    option_5.pack(fill="x")

    option_6 = Option(left_frame, "Max. days not seen?", max_not_seen)
    option_6.pack(fill="x")

    option_7 = Option(left_frame, "Max. sun altitude?", max_sun_alt)
    option_7.pack(fill="x")

    option_8 = Option(left_frame, "Min. distance from Moon?", min_d_from_moon)
    option_8.pack(fill="x")

    option_9 = Option(left_frame, "Min. motion speed?", min_motion_speed)
    option_9.pack(fill="x")
    # ...
    continous = tk.Checkbutton(left_frame, text="Continous?")
    continous.pack()

    console = Console(app)
    console.pack(side="bottom", fill="both", expand=False, padx=5, pady=5)

    add = tk.Button(right_frame, text="Add")
    add.pack(side="bottom")

    mp_editor = ScrollFrame(right_frame)
    mp_editor.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    # console.out("Hello, World!")
    app.center()
    app.mainloop()


if __name__ == "__main__":
    main()
