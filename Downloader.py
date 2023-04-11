import webbrowser
from tkinter import *
import os
from tkinter import messagebox, filedialog
from threading import Thread
import AppOpener
from requests import get
import customtkinter
from winotify import Notification, audio
import pyperclip
from pytube import YouTube
from pytube import Playlist
from PIL import Image


class UltimateDownloader():

    def __init__(self):
        self.theme_mode = "dark"
        self.currentVersion = 3.0
        self.devsite = "https://creators.nafezly.com/u/youssefelkhdodairy"

    def checkForUpdates(self):

        try:
            txt = float(get("https://pastebin.com/raw/FR7sD2hT").text)
            if txt > self.currentVersion:
                self.notification("New Update Available!",
                                  "There Was New Update Available For Our App, New Features Waiting For You..!",
                                  "Download Now!",
                                  f"{self.devsite}")
            else:
                pass
        except:
            pass

    def notification(self, title, msg, buttonLabel, function):
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

    def WarningNotify(self, s):
        messagebox.showwarning("Warning!", s)

    def ErrorNotify(self, s):
        messagebox.showerror("Error!", s)

    def InfoNotify(self, s):
        messagebox.showinfo("Notify!", s)

    def on_complete(self, *args):
        self.notification('Download completed!', 'Download process is completed you can check now!', "Open Folder!",
                          self.folder)
        self.download_path.configure(text=f"Downloaded in: {self.folder}")

    def on_progress(self, stream, chunk, bytes_remaining):
        self.broggress_bar.set(0.0)
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_complete = bytes_downloaded / total_size * 100
        self.broggress_bar.set(float(percentage_of_complete) / 100)
        self.top.update_idletasks()

    def processingAnimation(self, mode):
        if mode == "loading":
            self.broggress_bar.configure(mode="indeterminate")
            self.broggress_bar.start()
        else:
            self.broggress_bar.configure(mode="determinate")
            self.broggress_bar.stop()
            self.broggress_bar.set(0.0)

    def geturl(self, *args):
        try:
            self.processingAnimation("loading")
            self.download_status.configure(text="Status: processing...")
            link = self.url_entry.get()
            ytv = YouTube(link, on_complete_callback=self.on_complete, on_progress_callback=self.on_progress)
            height_quality = str(ytv.streams.get_highest_resolution().filesize_mb).split('.')
            height_quality = height_quality[0]
            rare_quality = str(ytv.streams.get_lowest_resolution().filesize_mb).split('.')
            rare_quality = rare_quality[0]
            audio_only = str(ytv.streams.get_audio_only().filesize_mb).split('.')
            audio_only = audio_only[0]

            self.download_status.configure(text="Status: ready!")
            self.title_label.configure(text=f"Title: {ytv.title}")
            self.duration_label.configure(text=f"Duration: {round(ytv.length / 60, 2)} minutes")
            self.file_size_label.configure(
                text=f"File size: HQ-{height_quality}, RQ-{rare_quality}, MP3-{audio_only} >> Mb")
            self.playlist_height_quality_download.configure(text=f'HQ', fg_color="#1f6aa5", command=None)
            self.playlist_medium_quality_download.configure(text=f'RQ', fg_color="#1f6aa5", command=None)
            self.playlist_low_quality_download.configure(text=f'MP3', fg_color="#1f6aa5", command=None)
            self.video_height_quality_download.configure(text=f'HQ', fg_color='red',
                                                         command=lambda: self.downloadHight(ytv))
            self.video_medium_quality_download.configure(text=f'RQ', fg_color='brown',
                                                         command=lambda: self.downloadLowest(ytv))
            self.video_low_quality_download.configure(text=f'MP3', fg_color='blue',
                                                      command=lambda: self.downloadAudio(ytv))
            self.processingAnimation("stop")

        except:
            self.ErrorNotify("Invalid YouTube url!")

    def getplaylisturl(self, *args):
        self.download_status.configure(text="Status: processing...")
        hq = 0
        rq = 0
        ao = 0
        du = 0
        self.processingAnimation("loading")
        try:
            link = self.url_entry.get()
            yt_playlist = Playlist(link)
            for video in yt_playlist.videos:
                height_quality = video.streams.get_highest_resolution().filesize_mb
                hq += int(height_quality)
                rare_quality = video.streams.get_lowest_resolution().filesize_mb
                rq += int(rare_quality)
                audio_only = video.streams.get_audio_only().filesize_mb
                ao += int(audio_only)
            for video in yt_playlist.videos:
                try:
                    du += float(video.length)
                except TypeError:
                    du += float(0.0)

            self.download_status.configure(text="Status: ready!")
            self.title_label.configure(text=f"Title: {yt_playlist.title}")
            self.duration_label.configure(text=f"Duration: {round(du / 60, 2)} minutes")
            self.file_size_label.configure(text=f"File size: HQ-{hq}, RQ-{rq}, MP3-{ao} >> Mb")
            self.video_height_quality_download.configure(text=f'HQ', fg_color="#1f6aa5", command=None)
            self.video_medium_quality_download.configure(text=f'RQ', fg_color="#1f6aa5", command=None)
            self.video_low_quality_download.configure(text=f'MP3', fg_color="#1f6aa5", command=None)
            self.playlist_height_quality_download.configure(text=f'HQ', fg_color="red",
                                                            command=lambda: self.downloadPlaylistHight(link))
            self.playlist_medium_quality_download.configure(text=f'RQ', fg_color="brown",
                                                            command=lambda: self.downloadPlaylistLowest(link))
            self.playlist_low_quality_download.configure(text=f'MP3', fg_color="blue",
                                                         command=lambda: self.downloadPlaylistAudio(link))
            self.processingAnimation("stop")

        except:
            self.ErrorNotify("Invalid Playlist url!")

    def downloadHight(self, video_object):
        try:
            self.folder = filedialog.askdirectory()
            if self.folder == '' or self.folder == ' ':
                self.download_status.configure(text="Status: ")
            elif os.path.exists(self.folder + "/" + video_object.title + ".mp4") or os.path.exists(
                    self.folder + "/" + video_object.title + ".mp3"):
                self.InfoNotify("File is already exists!")
            else:
                self.InfoNotify("Download started")
                self.download_status.configure(text="Status: Downloading...")
                video_object.streams.get_highest_resolution().download(self.folder)
                self.download_status.configure(text="Status: Downloaded successfully!")
        except:
            self.ErrorNotify("Download failed!")

    def downloadLowest(self, video_object):
        try:
            self.folder = filedialog.askdirectory()
            if self.folder == '' or self.folder == ' ':
                self.download_status.configure(text="Status: ")
            elif os.path.exists(self.folder + "/" + video_object.title + ".mp4") or os.path.exists(
                    self.folder + "/" + video_object.title + ".mp3"):
                self.InfoNotify("File is already exists!")
            else:
                self.InfoNotify("Download started")
                self.download_status.configure(text="Status: Downloading...")
                video_object.streams.get_lowest_resolution().download(self.folder)
                self.download_status.configure(text="Status: Downloaded successfully!")
        except:
            self.ErrorNotify("Download failed!")

    def downloadAudio(self, video_object):
        try:
            self.folder = filedialog.askdirectory()
            if self.folder == '' or self.folder == ' ':
                self.download_status.configure(text="Status: ")
            elif os.path.exists(self.folder + "/" + video_object.title + ".mp4") or os.path.exists(
                    self.folder + "/" + video_object.title + ".mp3"):
                self.InfoNotify("File is already exists!")
            else:
                self.InfoNotify("Download started")
                self.download_status.configure(text="Status: Downloading...")
                video = video_object.streams.filter(only_audio=True).first()
                downloaded_file = video.download(self.folder)
                base, ext = os.path.splitext(downloaded_file)
                new_file = base + '.mp3'
                os.rename(downloaded_file, new_file)
                self.on_complete()
                self.download_status.configure(text="Status: Downloaded successfully!")
        except:
            self.ErrorNotify("Download failed!")

    def downloadPlaylistHight(self, link):
        yt_playlist = Playlist(link)
        try:
            self.folder = filedialog.askdirectory()
            if self.folder == '' or self.folder == ' ':
                self.download_status.configure(text="Status: ")
            else:
                self.InfoNotify("Download started")
                self.download_status.configure(text="Status: Downloading...")
                for video in yt_playlist.videos:
                    video.streams.get_highest_resolution().download(self.folder)
                self.on_complete()
                self.download_status.configure(text="Status: Downloaded successfully!")
        except:
            self.ErrorNotify("Download failed!")

    def downloadPlaylistLowest(self, link):
        yt_playlist = Playlist(link)
        try:
            self.folder = filedialog.askdirectory()
            if self.folder == '' or self.folder == ' ':
                self.download_status.configure(text="Status: ")
            else:
                self.InfoNotify("Download started")
                self.download_status.configure(text="Status: Downloading...")
                for video in yt_playlist.videos:
                    video.streams.get_lowest_resolution().download(self.folder)
                self.on_complete()
                self.download_status.configure(text="Status: Downloaded successfully!")
        except:
            self.ErrorNotify("Download failed!")

    def downloadPlaylistAudio(self, link):
        yt_playlist = Playlist(link)
        try:
            self.folder = filedialog.askdirectory()
            if self.folder == '' or self.folder == ' ':
                self.download_status.configure(text="Status: ")
            else:
                self.InfoNotify("Download started")
                self.download_status.configure(text="Status: Downloading...")
                for video in yt_playlist.videos:
                    video = video.streams.filter(only_audio=True).first()
                    downloaded_file = video.download(self.folder)
                    base, ext = os.path.splitext(downloaded_file)
                    new_file = base + '.mp3'
                    os.rename(downloaded_file, new_file)
                self.on_complete()
                self.download_status.configure(text="Status: Downloaded successfully!")
        except:
            self.ErrorNotify("Download failed!")

    def browse(self, *args):
        try:
            os.startfile(self.folder)
        except:
            self.ErrorNotify("No directory selected")

    def stopdownload(*args):
        stop = False

    def dev(self):
        try:
            webbrowser.open(f'{self.devsite}')
        except:
            self.ErrorNotify("Redirecting failed!")

    def geturlx(self, *args):
        print(self.choices.get())
        if self.choices.get() == "YT Video":
            Thread(target=self.geturl).start()
        elif self.choices.get() == "YT PlayList":
            Thread(target=self.getplaylisturl).start()
        elif self.choices.get() == "Audio":
            self.WarningNotify("This type not available yet!")
        elif self.choices.get() == "Audio":
            self.WarningNotify("This type not available yet!")
        else:
            self.ErrorNotify('Select type of download')

    def paste(self):
        spam = pyperclip.paste()
        self.url_entry.delete('0', 'end')
        self.url_entry.insert('end', spam)

    def popup(self, e):
        self.my_menu.tk_popup(e.x_root, e.y_root)

    def stop(self, *args):
        try:
            self.top.destroy()
            AppOpener.close("Ultimate Downloader")
        except:
            pass

    def check_theme_mode(self):
        try:
            with open("Dtheme.apr", "r") as f:
                self.theme_mode = f.read()
            f.close()
            if self.theme_mode == "dark":
                return "dark"
            else:
                return "light"
        except:
            with open("Dtheme.apr", "w") as f:
                f.write("dark")
            f.close()

    def appearanceMode(self):
        if self.dark_mode_switch.get() == "on":
            customtkinter.set_appearance_mode("dark")
            with open("Dtheme.apr", "w") as f:
                f.write("dark")
            f.close()
        else:
            customtkinter.set_appearance_mode("light")
            with open("Dtheme.apr", "w") as f:
                f.write("light")
            f.close()

    def gui(self):
        self.top = customtkinter.CTk()
        self.top.title(f'Ultimate Downloader v{self.currentVersion}')
        self.top.resizable(False, False)
        self.top.iconbitmap("images\\favicon.ico")

        self.dwImage = customtkinter.CTkImage(light_image=Image.open("images/UltimateDownloader Banner.png"),
                                              dark_image=Image.open("images/UltimateDownloader Banner.png"),
                                              size=(580, 130))
        self.logo = customtkinter.CTkLabel(self.top, image=self.dwImage, text="")
        self.logo.grid(row=0, column=0, columnspan=4, pady=(0, 5))

        self.choices = customtkinter.CTkOptionMenu(self.top, height=30, width=130, values=["YT Video", "YT PlayList"],
                                                   corner_radius=15, font=("cairo", 14, "bold"))
        self.choices.grid(row=1, column=0, padx=5)
        self.choices.set("YT Video")

        self.url_entry = customtkinter.CTkEntry(self.top, height=30, placeholder_text="URL HERE",
                                                font=('Calbiri', 14, "bold"), width=300, corner_radius=15,
                                                fg_color="#0055AA")
        self.url_entry.grid(row=1, column=1, columnspan=2, padx=5)
        self.url_entry.bind("<Return>", self.geturlx)
        self.url_entry.focus_set()
        self.url_entry.bind('<Button-3>', self.popup)
        self.url_entry.bind('<Return>', self.geturlx)

        self.fetch_image = customtkinter.CTkImage(light_image=Image.open("images/info.jpg"),
                                                  dark_image=Image.open("images/info.jpg"),
                                                  size=(25, 25))

        self.fetch_burron = customtkinter.CTkButton(self.top, image=self.fetch_image, text="",
                                                    font=('Calbiri', 16, 'bold'), height=30, width=120,
                                                    corner_radius=15, command=self.geturlx)
        self.fetch_burron.grid(row=1, column=3, padx=5)

        self.title_label = customtkinter.CTkLabel(self.top, text='Title: ', font=('Calbiri', 16, 'bold'))
        self.title_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")

        self.duration_label = customtkinter.CTkLabel(self.top, text='Duration: ', font=('Calbiri', 16, 'bold'))
        self.duration_label.grid(row=3, column=0, columnspan=4, padx=10, sticky="w")

        self.file_size_label = customtkinter.CTkLabel(self.top, text='File size: ', font=('Calbiri', 16, 'bold'))
        self.file_size_label.grid(row=4, column=0, columnspan=4, padx=10, sticky="w")

        self.available_label = customtkinter.CTkLabel(self.top, text='Available to download:',
                                                      font=('Calbiri', 16, 'bold'))
        self.available_label.grid(row=5, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="w")

        # self.file_download_label = customtkinter.CTkLabel(self.top, text='File / Others ', font=('Calbiri', 16, 'bold'))
        # self.file_download_label.grid(row=6, column=0, padx=10,  pady=(0, 10), sticky="w")
        #
        # self.file_download_button = customtkinter.CTkButton(self.top, text=f'Download', font=('Calbiri', 16, 'bold'), width=120,
        #                                         height=30, corner_radius=15)
        # self.file_download_button.grid(row=6, column=1, columnspan=4, pady=(0, 10), padx=5, sticky="e")

        self.video_download_label = customtkinter.CTkLabel(self.top, text='YT Video ', font=('Calbiri', 16, 'bold'))
        self.video_download_label.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="w")

        self.video_height_quality_download = customtkinter.CTkButton(self.top, text=f'HQ', font=('Calbiri', 16, 'bold'),
                                                                     width=120, height=30, corner_radius=15)
        self.video_height_quality_download.grid(row=7, column=3, padx=5, pady=(0, 10), sticky="e")

        self.video_medium_quality_download = customtkinter.CTkButton(self.top, text=f'RQ', font=('Calbiri', 16, 'bold'),
                                                                     width=120, height=30, corner_radius=15)
        self.video_medium_quality_download.grid(row=7, column=2, padx=(5, 20), pady=(0, 10), sticky="e")

        self.video_low_quality_download = customtkinter.CTkButton(self.top, text=f'MP3', font=('Calbiri', 16, 'bold'),
                                                                  width=120, height=30, corner_radius=15)
        self.video_low_quality_download.grid(row=7, column=1, pady=(0, 10), sticky="e")

        self.playlist_download_label = customtkinter.CTkLabel(self.top, text='YT PLayList ',
                                                              font=('Calbiri', 16, 'bold'))
        self.playlist_download_label.grid(row=8, column=0, padx=10, pady=(0, 10), sticky="w")

        self.playlist_height_quality_download = customtkinter.CTkButton(self.top, text=f'HQ',
                                                                        font=('Calbiri', 16, 'bold'),
                                                                        width=120, height=30, corner_radius=15)
        self.playlist_height_quality_download.grid(row=8, column=3, padx=5, pady=(0, 10), sticky="e")

        self.playlist_medium_quality_download = customtkinter.CTkButton(self.top, text=f'RQ',
                                                                        font=('Calbiri', 16, 'bold'),
                                                                        width=120, height=30, corner_radius=15)
        self.playlist_medium_quality_download.grid(row=8, column=2, padx=(5, 20), pady=(0, 10), sticky="e")

        self.playlist_low_quality_download = customtkinter.CTkButton(self.top, text=f'MP3',
                                                                     font=('Calbiri', 16, 'bold'),
                                                                     width=120, height=30, corner_radius=15)
        self.playlist_low_quality_download.grid(row=8, column=1, pady=(0, 10), sticky="e")

        # self.audio_download_label = customtkinter.CTkLabel(self.top, text='Audio ', font=('Calbiri', 16, 'bold'))
        # self.audio_download_label.grid(row=9, column=0, padx=10, pady=(0, 10), sticky="w")
        #
        # self.audio_download = customtkinter.CTkButton(self.top, text=f'MP3', font=('Calbiri', 16, 'bold'), width=120, height=30, corner_radius=15)
        # self.audio_download.grid(row=9, column=3, padx=5, pady=(0, 10), sticky="e")

        # self.pause_button = customtkinter.CTkButton(self.top, text=f'||', font=('Calbiri', 14, 'bold'), width=70, height=25,
        #                              corner_radius=15)
        # self.pause_button.grid(row=10, column=0, padx=10, pady=(10), sticky="e")

        self.broggress_bar = customtkinter.CTkProgressBar(self.top, width=450, height=20)
        self.broggress_bar.grid(row=10, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")
        self.processingAnimation("stop")

        self.download_status = customtkinter.CTkLabel(self.top, text=f'Status: ', font=('Calbiri', 16, 'bold'))
        self.download_status.grid(row=11, column=0, columnspan=4, padx=10, sticky="w")

        self.download_path = customtkinter.CTkLabel(self.top, text='Downloaded in: ', font=('Calbiri', 16, 'bold'))
        self.download_path.grid(row=12, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        self.browse_button = customtkinter.CTkButton(self.top, text='Browse', font=('Calbiri', 16, 'bold'), width=120,
                                                     corner_radius=15, command=self.browse)
        self.browse_button.grid(row=12, column=3, padx=5, pady=10, sticky="e")

        tm = self.check_theme_mode()
        if tm == "dark":
            self.appearanceVar = customtkinter.StringVar(value="on")
        else:
            self.appearanceVar = customtkinter.StringVar(value="off")
        customtkinter.set_appearance_mode(self.theme_mode)

        self.dark_mode_switch = customtkinter.CTkSwitch(master=self.top, text="Dark Mode", command=self.appearanceMode,
                                                        variable=self.appearanceVar, onvalue="on", offvalue="off",
                                                        font=("calbiri", 12, "bold"))
        self.dark_mode_switch.grid(row=13, column=0, columnspan=4, pady=10, padx=10)

        self.about_button = customtkinter.CTkButton(self.top, text='!',
                                                    font=('Calbiri', 14, 'bold'), width=5, corner_radius=15,
                                                    command=self.dev)
        self.about_button.grid(row=13, column=3, padx=5, pady=10, sticky="e")

        self.top.protocol("WM_DELETE_WINDOW", self.stop)
        self.my_menu = Menu(self.top, tearoff=False)
        self.my_menu.add_command(label='paste', command=self.paste)
        self.checkForUpdates()
        self.top.mainloop()


if __name__ == "__main__":
    UD = UltimateDownloader()
    Thread(target=UD.gui).start()
