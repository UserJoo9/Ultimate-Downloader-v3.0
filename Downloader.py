import tkinter
import webbrowser
from tkinter import *
import os
from tkinter import messagebox, filedialog
from threading import Thread

import AppOpener
from requests import get

try:
    import customtkinter
except:
    os.system('pip install customtkinter')

try:
    import winotify
    from winotify import Notification, audio
except:
    os.system('pip install winotify')

try:
    import pyperclip
except:
    os.system('pip install pyperclip')

try:
    from pytube import YouTube
    from pytube import Playlist
except:
    os.system('pip install pytube')

try:
    from PIL import Image, ImageTk
except:
    os.system('pip install pillow')


def checkForUpdates():
    currentVersion = 4.0
    try:
        txt = float(get("https://pastebin.com/raw/FR7sD2hT").text)
        if txt > currentVersion:
            notification("New Update Available!",
                         "There Was New Update Available For Our App, New Features Waiting For You..!", "Download Now!",
                         "https://userjoo9.github.io/youssefinfo/#projects")
        else:
            pass
    except:
        pass


def notification(title, msg, buttonLabel, function):
    toaster = Notification(
        app_id="YouTube Free Downloader",
        title=title,
        msg=msg,
        duration="long",
        icon=r"D:\programming\python\YouTube Downloader Original\images\favicon.ico"
    )
    toaster.set_audio(audio.Default, loop=False)
    toaster.add_actions(label=buttonLabel, launch=function)
    toaster.show()


def WarningNotify(s):
    messagebox.showwarning("Warning!", s)


def ErrorNotify(s):
    messagebox.showerror("Error!", s)


def InfoNotify(s):
    messagebox.showinfo("Notify!", s)


def on_complete(*args):
    global folder
    notification('Download completed!', 'Download process is completed you can check now!', "Open Folder!", folder)
    l9.configure(text=f"Downloaded in: {folder}")


def geturl(*args):
    global height_quality, lowest_quality, audio_only, link, video_object
    try:
        link = e1.get()
        video_object = YouTube(link, on_complete_callback=on_complete)

        height_quality = str(video_object.streams.get_highest_resolution().filesize / 1000000).split('.')
        height_quality = height_quality[0]
        lowest_quality = str(video_object.streams.get_lowest_resolution().filesize / 1000000).split('.')
        lowest_quality = lowest_quality[0]
        audio_only = str(video_object.streams.get_audio_only().filesize / 1000000).split('.')
        audio_only = audio_only[0]

        l4.configure(text=f"Title: {video_object.title}")
        l5.configure(text=f"Duration: {round(video_object.length / 60, 2)} minutes")

        b2.configure(text=f'High quality\n720p \n{height_quality} Mb', fg_color='red', command=downloadHight)

        b3.configure(text=f'Low quality\n360p \n{lowest_quality} Mb', fg_color='brown', command=downloadLowest)

        b4.configure(text=f'Audio mp3 \n{audio_only} Mb', fg_color='blue', command=downloadAudio)


    except Exception:
        ErrorNotify("Invalid YouTube url!")


def getplaylisturl(*args):
    global height_quality, lowest_quality, audio_only, link, yt_playlist
    hq = 0
    lq = 0
    ao = 0
    try:
        link = e1.get()
        yt_playlist = Playlist(link)
        for video in yt_playlist.videos:
            height_quality = video.streams.get_highest_resolution().filesize / 1000000
            hq += int(height_quality)
            lowest_quality = video.streams.get_lowest_resolution().filesize / 1000000
            lq += int(lowest_quality)
            audio_only = video.streams.get_audio_only().filesize / 1000000
            ao += int(audio_only)
        l4.configure(text=f"Title: {yt_playlist.title}")
        l5.configure(text=f"Duration: Can't calculate!!")

        b2.configure(text=f'High quality\n720p\nTotal {hq} Mb', fg_color="red", command=downloadPlaylistHight)

        b3.configure(text=f'Low quality\n360p\nTotal {lq} Mb', fg_color="brown", command=downloadPlaylistLowest)

        b4.configure(text=f'Audio mp3\nTotal {ao} Mb', fg_color="blue", command=downloadPlaylistAudio)

    except Exception:
        ErrorNotify("Invalid Playlist url!")


def downloadHight(*args):
    global folder
    try:
        folder = filedialog.askdirectory()
        if folder == ' ':
            l8.configure(text="Status: ")
        elif os.path.exists(folder+"/"+video_object.title+".mp4") or os.path.exists(folder+"/"+video_object.title+".mp3"):
            InfoNotify("File is already exists!")
        else:
            InfoNotify("Download started")
            video_object.streams.get_highest_resolution().download(folder)
            l8.configure(text="Status: Downloaded successfully!")
    except Exception:
        ErrorNotify("Download failed!")


def downloadLowest(*args):
    global folder
    try:
        folder = filedialog.askdirectory()
        if folder == ' ':
            l8.configure(text="Status: ")
        elif os.path.exists(folder+"/"+video_object.title+".mp4") or os.path.exists(folder+"/"+video_object.title+".mp3"):
            InfoNotify("File is already exists!")
        else:
            InfoNotify("Download started")
            video_object.streams.get_lowest_resolution().download(folder)
            l8.configure(text="Status: Downloaded successfully!")
    except Exception:
        ErrorNotify("Download failed!")


def downloadAudio(*args):
    global folder
    try:
        folder = filedialog.askdirectory()
        if folder == ' ':
            l8.configure(text="Status: ")
        elif os.path.exists(folder+"/"+video_object.title+".mp4") or os.path.exists(folder+"/"+video_object.title+".mp3"):
            InfoNotify("File is already exists!")
        else:
            InfoNotify("Download started")
            video = video_object.streams.filter(only_audio=True).first()
            downloaded_file = video.download(folder)
            base, ext = os.path.splitext(downloaded_file)
            new_file = base + '.mp3'
            os.rename(downloaded_file, new_file)
            on_complete()
            l8.configure(text="Status: Downloaded successfully!")
    except Exception:
        ErrorNotify("Download failed!")


def downloadPlaylistHight(*args):
    global folder
    yt_playlist = Playlist(link)
    try:
        folder = filedialog.askdirectory()
        if folder == ' ':
            l8.configure(text="Status: ")
        else:
            InfoNotify("Download started")
            for video in yt_playlist.videos:
                video.streams.get_highest_resolution().download(folder)
            on_complete()
            l8.configure(text="Status: Downloaded successfully!")
    except Exception:
        ErrorNotify("Download failed!")


def downloadPlaylistLowest(*args):
    global folder
    yt_playlist = Playlist(link)
    try:
        folder = filedialog.askdirectory()
        if folder == ' ':
            l8.configure(text="Status: ")
        else:
            InfoNotify("Download started")
            for video in yt_playlist.videos:
                video.streams.get_lowest_resolution().download(folder)
            on_complete()
            l8.configure(text="Status: Downloaded successfully!")
    except Exception:
        ErrorNotify("Download failed!")


def downloadPlaylistAudio(*args):
    global folder
    yt_playlist = Playlist(link)
    try:
        folder = filedialog.askdirectory()
        if folder == ' ':
            l8.configure(text="Status: ")
        else:
            InfoNotify("Download started")
            for video in yt_playlist.videos:
                video = video.streams.filter(only_audio=True).first()
                downloaded_file = video.download(folder)
                base, ext = os.path.splitext(downloaded_file)
                new_file = base + '.mp3'
                os.rename(downloaded_file, new_file)
            on_complete()
            l8.configure(text="Status: Downloaded successfully!")
    except Exception:
        ErrorNotify("Download failed!")


def browse(*args):
    global folder
    try:
        os.startfile(folder)
    except Exception:
        ErrorNotify("No directory selected")


def stopdownload(*args):
    global stop
    stop = False


def dev():
    try:
        webbrowser.open('https://userjoo9.github.io/youssefinfo/#')
    except Exception:
        ErrorNotify("Redirecting failed!")


def geturlx(*args):
    global combobox
    print(combobox.get())
    if combobox.get() == "YT Video":
        geturl()
    elif combobox.get() == "YT PlayList":
        getplaylisturl()
    else:
        ErrorNotify('Select type of download')


def paste():
    spam = pyperclip.paste()
    e1.delete('0', 'end')
    e1.insert('end', spam)


def popup(e):
    my_menu.tk_popup(e.x_root, e.y_root)


def exiT(*args):
    top.destroy()
    try:
        AppOpener.close("Ultimate Downloader")
    except:
        pass

theme_mode = "dark"
def check_theme_mode():
    global theme_mode, switch_var
    theme_mode = "dark"
    try:
        with open("Dtheme.apr", "r") as f:
            theme_mode = f.read()
        f.close()
        if theme_mode == "on":
            switch_var = customtkinter.StringVar(value="on")
        else:
            switch_var = customtkinter.StringVar(value="off")
    except:
        with open("Dtheme.apr", "w") as f:
            f.write("dark")
        f.close()

check_theme_mode()

customtkinter.set_appearance_mode(theme_mode)

def gui():
    global combobox, top, l4, e1, l5, l9, l8, my_menu, b2, b3, b4, switch_var
    top = customtkinter.CTk()
    top.title('Ultimate Downloader v3.0')
    top.geometry('506x560')
    top.resizable(False, False)
    # top.iconbitmap("images\\favicon.ico")

    switch_var = customtkinter.StringVar(value="on")

    def switch_event():
        if dark_mode_switch.get() == "on":
            customtkinter.set_appearance_mode("dark")
            with open("Dtheme.apr", "w") as f:
                f.write("dark")
            f.close()
        else:
            customtkinter.set_appearance_mode("light")
            with open("Dtheme.apr", "w") as f:
                 f.write("light")
            f.close()

    # youtubeImg = customtkinter.CTkImage(light_image=Image.open("images/YoutubeLogo.png"),
    #                                     dark_image=Image.open("images/YoutubeLogo.png"),
    #                                     size=(150, 50))
    # logo = customtkinter.CTkLabel(top, image=youtubeImg, text="", fg_color="white", corner_radius=15, height=70)
    # logo.pack(pady=10)

    l1 = customtkinter.CTkLabel(top, text="Ultimate Downloader", font=('Calbiri', 28, 'bold'))
    l1.place(x=85, y=20)

    dwImage = customtkinter.CTkImage(light_image=Image.open("images/downloadicon.png"),
                                        dark_image=Image.open("images/downloadicon.png"),
                                        size=(30, 30))
    logo = customtkinter.CTkLabel(top, image=dwImage, text="")
    logo.place(x=380, y=20)

    # var = IntVar()
    # rb1 = customtkinter.CTkRadioButton(top, text='Video', variable=var, value=1, font=('Calbiri', 14, 'bold'), width=30)
    # rb1.place(x=160, y=105)
    # var.set(1)
    # rb2 = customtkinter.CTkRadioButton(top, text='PLayList', variable=var, value=2, font=('Calbiri', 14, 'bold'), width=30)
    # rb2.place(x=260, y=105)

    combobox = customtkinter.CTkOptionMenu(top, height=40, width=130, values=["YT Video", "YT PlayList", "File", "Game", "Application"], corner_radius=15, font=("cairo", 14, "bold"))
    combobox.place(x=10, y=80)
    combobox.set("File")

    e1 = customtkinter.CTkEntry(top, placeholder_text="URL HERE", font=('Calbiri', 14, "bold"), width=270, corner_radius=15, fg_color="#0055AA")
    e1.place(x=150, y=80, height=40)
    e1.bind("<Return>", geturlx)
    e1.focus_set()
    e1.bind('<Button-3>', popup)
    e1.bind('<Return>', geturlx)

    infoImg = customtkinter.CTkImage(light_image=Image.open("images/info.jpg"),
                                     dark_image=Image.open("images/info.jpg"),
                                     size=(30, 30))

    b1 = customtkinter.CTkButton(top, image=infoImg, text="", font=('Calbiri', 16, 'bold'), width=50, corner_radius=15, command=geturlx)
    b1.place(x=430, y=80, height=40)

    l3 = customtkinter.CTkLabel(top, text='Information:- ', font=('Calbiri', 16, 'bold'))
    l3.place(x=20, y=125)

    l4 = customtkinter.CTkLabel(top, text='Title: ', font=('Calbiri', 16, 'bold'))
    l4.place(x=30, y=150)

    l5 = customtkinter.CTkLabel(top, text='Duration: ', font=('Calbiri', 16, 'bold'))
    l5.place(x=30, y=175)

    l10 = customtkinter.CTkLabel(top, text='File size: ', font=('Calbiri', 16, 'bold'))
    l10.place(x=30, y=200)

    l7 = customtkinter.CTkLabel(top, text='Available to download:', font=('Calbiri', 16, 'bold'))
    l7.place(x=20, y=235)

    b7 = customtkinter.CTkButton(top, text=f'High quality', font=('Calbiri', 16, 'bold'), width=150, height=50, corner_radius=15)
    b7.place(x=20, y=270)

    b2 = customtkinter.CTkButton(top, text=f'Rare quality', font=('Calbiri', 16, 'bold'), width=150, height=50, corner_radius=15)
    b2.place(x=180, y=270)

    b3 = customtkinter.CTkButton(top, text=f'Low quality', font=('Calbiri', 16, 'bold'), width=150, height=50, corner_radius=15)
    b3.place(x=340, y=270)

    b4 = customtkinter.CTkButton(top, text=f'Audio mp3', font=('Calbiri', 16, 'bold'), width=150, height=50, corner_radius=15)
    b4.place(x=20, y=330)

    b6 = customtkinter.CTkButton(top, text=f'Game', font=('Calbiri', 16, 'bold'), width=150, height=50,
                                 corner_radius=15)
    b6.place(x=180, y=330)

    b7 = customtkinter.CTkButton(top, text=f'File/App', font=('Calbiri', 16, 'bold'), width=150, height=50,
                                 corner_radius=15)
    b7.place(x=340, y=330)

    b8 = customtkinter.CTkButton(top, text=f'||', font=('Calbiri', 14, 'bold'), width=50, height=30,
                                 corner_radius=15)
    b8.place(x=20, y=395)

    bb = customtkinter.CTkProgressBar(top, width=360, height=20)
    bb.place(x=80, y=400)
    bb.set(0)

    l10 = customtkinter.CTkLabel(top, text='0%', font=('Calbiri', 16, 'bold'))
    l10.place(x=460, y=397)

    l8 = customtkinter.CTkLabel(top, text=f'Status: ', font=('Calbiri', 16, 'bold'))
    l8.place(x=20, y=440)

    l9 = customtkinter.CTkLabel(top, text='Downloaded in: ', font=('Calbiri', 16, 'bold'))
    l9.place(x=20, y=470)

    b5 = customtkinter.CTkButton(top, text='Browse', font=('Calbiri', 16, 'bold'), width=8, corner_radius=15, command=browse)
    b5.place(x=410, y=470)

    dark_mode_switch = customtkinter.CTkSwitch(master=top, text="Dark Mode", command=switch_event,
                                               variable=switch_var, onvalue="on", offvalue="off",
                                               font=("calbiri", 12, "bold"))
    dark_mode_switch.place(x=210, y=525)

    bx = customtkinter.CTkButton(top, text='!',
                        font=('Calbiri', 14, 'bold'), width=5, corner_radius=15, command=dev)
    bx.place(x=465, y=525)

    top.protocol("WM_DELETE_WINDOW", exiT)
    my_menu = Menu(top, tearoff=False)
    my_menu.add_command(label='paste', command=paste)
    checkForUpdates()
    top.mainloop()


gui_thread = Thread(target=gui)
gui_thread.start()
