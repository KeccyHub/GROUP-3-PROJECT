import tkinter as tk
import av
import datetime
from tkinter import filedialog
from PIL import ImageTk, Image
import pygame
from moviepy.editor import VideoFileClip
from tkVideoPlayer import TkinterVideo

video_player= None
backward = None
forward = None
play_image = None
pause_image = None
audio_path = None
video_path = None
sound_on_image = None
sound_off_image = None
sound_enabled = True
stop_image = None
stop_btn = None
quit_image = None
vol_up = None
vol_down = None
current_time = None
quit_btn = None
new_position = None


def open_video():
    global video_entry, video_preview
    file_path = filedialog.askopenfilename(title="Select Video File",
                                           filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if file_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, file_path)
        video_preview.config(image=get_video_preview(file_path))


def convert_and_play():
    video_path = video_entry.get()
    if not video_path:
        return

    # Get the audio file path
    audio_path = convert_to_audio(video_path)

    if audio_path:
        # Play video with the generated audio
        play_video_with_audio(video_path, audio_path)
    



def convert_to_audio(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path.replace('.mp4', '_audio.mp3')  # Save audio as MP3

    try:
        audio = video.audio
        audio.write_audiofile(audio_path, fps=44100)
        audio.close()
        return audio_path
    except Exception as e:
        print("Error converting to audio:", str(e))
        return None


def play_video_with_audio(video_path, audio_path):
    global video_player, backward, forward, quit_image, current_time, play_image, pause_image, sound_enabled, sound_off_image, sound_on_image, stop_btn, stop_image, vol_up, vol_down
    root.withdraw()  # Hide the main window during video playback
    g3 = tk.Toplevel()
    g3.title("G3 Video Player")
    g3.geometry("1024x768")

    im = tk.PhotoImage(file="logo.png")
    loo_label = tk.Label(root, image=im)
    loo_label.pack()
    loo_label=im
    
    video_player = TkinterVideo(master=g3, scaled=True)
    video_player.pack(expand=True, fill="both")
    
    video_player.load(video_path)
    video_player.play()
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(-1)  # Play audio in loop (-1)
    
    
    def on_close():
        video_player.destroy()
        pygame.mixer.music.stop()
        g3.destroy()
        root.deiconify()  # Show the main window when closing the video window
    
    g3.protocol("WM_DELETE_WINDOW", on_close)

    control_frame = tk.Frame(g3, bg="#f0f0f0", width=1)
    control_frame.pack(fill="both", side=tk.BOTTOM, padx=2, pady=1)

    def play_video():
        video_player.play()
        pygame.mixer.music.unpause()
    
    def pause_video():
        video_player.pause()
        pygame.mixer.music.pause()
    
    def toggle_sound():
        global sound_enabled
        sound_enabled = not sound_enabled
        if sound_enabled:
            sound_btn.config(image=sound_on_image)
            pygame.mixer.music.set_volume(1.0)
        else:
            sound_btn.config(image=sound_off_image)
            pygame.mixer.music.set_volume(0.0)

    def quit_video():
        global quit_image
        if quit_image:
            video_player.stop()
            pygame.mixer.music.stop()
            video_player.destroy()
            root.destroy()  # To completely close the application
    
    def stop_video():
        global stop_image
        if stop_image:
            video_player.stop()
            pygame.mixer.music.stop()
            video_player.destroy()
            root.deiconify()

    def duration(event):
        dur = video_player.video_info()["duration"]
        end_time.config(text=str(datetime.timedelta(seconds=dur)))
        slider["to"] = dur
        val.set(video_player.current_duration())
        pygame.mixer.music.play(start=video_player.current_duration())

    def update_slide(event):
        val.set(video_player.current_duration())
        pygame.mixer.music.play(start=video_player.current_duration())

    def seek(value):
        video_player.seek(int(value))
        pygame.mixer.music.play(start=int(value))
        
    def skip(value:int):
        global new_position
        current_position = video_player.current_duration()
        new_position = current_position + value
        video_player.seek(int(new_position))
        pygame.mixer.music.play(start=int(new_position))
            

    def video_ended(event):
        slider.set(slider["to"])
        video_player.stop()
        pygame.mixer.music.stop()
        slider.set(0)


    val = tk.IntVar(g3)

    end_time = tk.Label(g3, text=str(datetime.timedelta(seconds=0)))
    end_time.pack(side="left")

    slider = tk.Scale(g3, variable=val,from_=0, to=0, orient="horizontal", command=seek)
    slider.pack(side="left", fill="x", expand=True)

    backward = tk.PhotoImage(file="backward.png")
    back_btn = tk.Button(control_frame, image=backward, command= lambda: skip(-10))
    back_btn.grid(row=1, column=0, columnspan=1, padx=20, sticky="ew")

    forward = tk.PhotoImage(file="forward.png")
    forward_btn = tk.Button(control_frame, image=forward, command= lambda: skip(5))
    forward_btn.grid(row=1, column=1, columnspan=1, padx=20, sticky="ew")
    
    sound_on_image = tk.PhotoImage(file="sound_on.png")
    sound_off_image = tk.PhotoImage(file="sound_off.png")
    sound_btn = tk.Button(control_frame, image=sound_on_image, command=toggle_sound)
    sound_btn.grid(row=1, column=2, columnspan=1, padx=20, sticky="ew")

    def decrease_volume():
        current_volume = pygame.mixer.music.get_volume()
        if current_volume > 0:
            pygame.mixer.music.set_volume(max(0, current_volume - 0.1))
    
    def increase_volume():
        current_volume = pygame.mixer.music.get_volume()
        if current_volume < 1:
            pygame.mixer.music.set_volume(min(1, current_volume + 0.1))

    pause_image = tk.PhotoImage(file="pause.png")
    pause_btn = tk.Button(control_frame, image=pause_image, command= pause_video)
    pause_btn.grid(row=1, column=3, columnspan=1, padx=20, sticky="ew")

    
    play_image = tk.PhotoImage(file="play.png")
    play_btn = tk.Button(control_frame, image=play_image, command=play_video)
    play_btn.grid(row=1, column=4, columnspan=1, padx=30, sticky="ew")
    
    vol_down = tk.PhotoImage(file="decrease_volume.png")
    volume_down_btn = tk.Button(control_frame, image=vol_down, command=decrease_volume)
    volume_down_btn.grid(row=1, column=5, columnspan=1, padx=30, sticky="ew")
    
    vol_up = tk.PhotoImage(file="increase_volume.png")
    volume_up_btn = tk.Button(control_frame, image=vol_up, command=increase_volume)
    volume_up_btn.grid(row=1, column=6, columnspan=1, padx=20, sticky="ew")

    quit_image = tk.PhotoImage(file="quit.png")
    quit_btn = tk.Button(control_frame, image=quit_image, command= quit_video)
    quit_btn.grid(row=1, column=7, columnspan=1, padx=20, sticky="ew")

    
    stop_image = tk.PhotoImage(file="stop.png")
    stop_btn = tk.Button(control_frame, image=stop_image, command=stop_video)
    stop_btn.grid(row=1, column=8, columnspan=1,padx=20, sticky="ew")
   
    video_player.bind("<<Duration>>", lambda event: duration(event))
    video_player.bind("<<SecondChanged>>", update_slide)
    video_player.bind("<<Ended>>", video_ended)
    





def get_video_preview(video_path, width=320, height=240):
    try:
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(0)
        clip.close()
        img = Image.fromarray(frame)
        img.thumbnail((width, height))
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print("Error getting video preview:", str(e))
        return None


root = tk.Tk()
root.title("G3 Video Player")
root.geometry("1024x768")


# Logo image
img = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=img, bg="#000000")
logo_label.pack(expand=True, fill="both", pady=60)

icon = tk.PhotoImage(file="logo.png")
root.iconphoto(True, icon)

root.configure(bg="#000000")

# UI Elements
frame = tk.Frame(root, bg="#000000")
frame.pack(pady=10)


video_label = tk.Label(frame, text="Video File:", fg="white", bg="#6c3483", font=("calibri", 12, ("bold")))
video_label.grid(row=0, column=0, padx=10, pady=10)

video_entry = tk.Entry(frame, width=40)
video_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

open_button = tk.Button(frame, text="Open File", fg="white", bg="#6c3483",font=("calibri", 12, ("bold")), command=open_video)
open_button.grid(row=0, column=2, padx=10, pady=10)

video_preview = tk.Label(root, bg="#000000")
video_preview.pack(pady=20)

convert_button = tk.Button(frame, text="Play", fg="white", bg="#6c3483", font=("calibri", 12, ("bold")), command=convert_and_play)
convert_button.grid(row=0, column=3, padx=10, pady=10)






root.mainloop()

