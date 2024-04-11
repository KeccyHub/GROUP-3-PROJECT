from tkinter import *
import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from PIL import ImageTk, Image

g3 = tk.Tk()
g3.title("G3 Video Player")
g3.geometry("800x700+290+10")
g3.minsize(0,0)

icon = PhotoImage(file="logo.png")
g3.iconphoto(False, icon)

frame = tk.Frame(g3, width=800, height=700, bg="#000000")
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

img = ImageTk.PhotoImage(Image.open("logo.png"))

label = Label(frame, image = img)
label.pack(fill="both")

def open_new_window(g3):
    op = tk.Toplevel(g3)
    op.title("G3 PLAYER")
    op.geometry("800x700+270+10")
    op.minsize(0,0)

    bottom_frame = tk.Frame(g3, bg="#FFFFFF")
    bottom_frame.pack(fill="both", side=BOTTOM)

    def duration(event):
        dur = g3_player.video_info()["duration"]
        end_time["text"] = str(datetime.timedelta(seconds=dur))
        slider["to"] = dur

    def update_slide(event):
        val.set(g3_player.current_duration())

    def open_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            g3_player.load(file_path)
            slider.config(to=0, from_=0)
            play_pause_btn["text"] = "Play"
            val.set(0)

    def seek(value):
        g3_player.seek(int(value))

    def skip(value:int):
        g3_player.seek(int(slider.get()) + value)
        val.set(slider.get() + value)

    def play_pause():
        if g3_player.is_paused():
            g3_player.play()
            play_pause_btn["text"] = "Pause"
        else:
            g3_player.pause()
            play_pause_btn["text"] = "Play"

    def video_ended(event):
        slider.set(slider["to"])
        play_pause_btn["text"] = "Play"
        slider.set(0)

    open_btn = tk.Button(g3, text="Open File", bg="#FFFFFF", font=("calibri", 12, "bold"), command=open_file)
    open_btn.pack(ipadx=4, ipady=2, anchor=tk.NW)

    g3_player = TkinterVideo(g3, scaled=True)
    g3_player.pack(expand=True, fill="both")

    backward = PhotoImage(file="backward.png")
    back_btn = tk.Button(bottom_frame, image=backward, bd=0, height=50, width=50, command=lambda: skip(-5))
    back_btn.pack(side=LEFT)

    play_pause_btn = tk.Button(bottom_frame, text="Play", width=30, height=2, command=play_pause)
    play_pause_btn.pack(expand=TRUE, fill="both", side=LEFT)

    forward = PhotoImage(file="forward.png")
    forward_btn = tk.Button(bottom_frame, image=forward, bd=0, height=50, width=50, command=lambda: skip(5))
    forward_btn.pack(side=LEFT)

    start_time = tk.Label(g3, text=str(datetime.timedelta(seconds=0)))
    start_time.pack(side="left")

    val = tk.IntVar(g3)
    slider = tk.Scale(g3, variable=val, from_=0, to=0, orient="horizontal", command=seek)
    slider.pack(side="left", fill="x", expand=True)

    end_time = tk.Label(g3, text=str(datetime.timedelta(seconds=0)))
    end_time.pack(side="left")

    g3_player.bind("<<Duration>>", duration)
    g3_player.bind("<<SecondChanged>>", update_slide)
    g3_player.bind("<<Ended>>", video_ended)


open_btn = tk.Button(frame, text="Enter", width=40, height=2, command=lambda:open_new_window(g3))
open_btn.pack(expand=TRUE, fill="both", side=LEFT)





g3.mainloop()