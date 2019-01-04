import tkinter as tk
import os


class ScrollFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super(ScrollFrame, self).__init__(master, *args, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.viewPort = tk.Frame(self.canvas, background="#ffffff")
        self.viewPort.bind("<Configure>", self.onFrameConfigure)

        self.vsb = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview)
        self.vsb.pack(side="right", fill="y")

        self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vsb.set)

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class Filter(tk.Frame):
    def __init__(self, master, text, entry_default, *args, **kwargs):
        super(Filter, self).__init__(master, *args, **kwargs)
        # self.pack(expand=True, fill="x")
        self.label = tk.Label(self, text=text)
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self)
        self.entry.insert("end", entry_default)
        self.entry.pack(side=tk.RIGHT)


class Toolbar(tk.Frame):
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
        # self.config(background="black", foreground="white")
        self.configure(font=("Consolas", 12))
        self.insert("end", "<<< Initialized!")
        self.config(state=tk.DISABLED)

    def out(self, text):
        self.config(state=tk.NORMAL)
        self.insert("end", "\n<<< " + text)
        self.config(state=tk.DISABLED)


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
    app = App()
    app.title("NEOCP Planner")
    app.geometry("1000x600")

    toolbar = Toolbar(app)
    toolbar.pack(side="top", fill="x")

    main_frame = tk.Frame(app)
    main_frame.pack(side="top", expand=True, fill="both", padx=5, pady=5)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", padx=5, pady=5)

    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="right", fill="both", padx=5, pady=5, expand=True)

    f1 = Filter(left_frame, "Min.alt?", 15)
    f1.pack(fill="x")
    # ...
    continous = tk.Checkbutton(left_frame, text="Continous?")
    continous.pack()

    console = Console(app)
    console.pack(side="bottom", fill="both", expand=False, padx=5, pady=5)

    mp_editor = ScrollFrame(right_frame)
    for i in range(25):
        fr = tk.Frame(mp_editor.viewPort)
        fr.pack(fill="x")
        label = tk.Label(fr, text=str(i))
        label.pack(side="left")
    mp_editor.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    # console.out("Hello, World!")
    app.center()
    app.mainloop()


if __name__ == "__main__":
    main()
