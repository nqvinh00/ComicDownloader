import customtkinter as ctkinter
from downloader import Downloader
from threading import Thread


class App(ctkinter.CTk):
    def __init__(self, geometry: str, mode: str = "dark", color_theme: str = "dark-blue"):
        """ Setup UI for app with customtkinter.
        Simply, it has a label, an entry to enter URL, a button to start download process.
        Also, a progress bar and a label for progress status.
        """
        super().__init__()

        self.title = "Comic Downloader"
        self.geometry(geometry)
        ctkinter.set_appearance_mode(mode)
        ctkinter.set_default_color_theme(color_theme)

        self.frame = ctkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = ctkinter.CTkLabel(
            master=self.frame, text="Comic Downloader", width=200, height=25, font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)

        self.entry = ctkinter.CTkEntry(master=self.frame, placeholder_text="URL",
                                       placeholder_text_color="gray", font=("Roboto", 16), width=400, height=50)
        self.entry.pack(pady=12, padx=10)

        self.button = ctkinter.CTkButton(
            master=self.frame, border_width=0, corner_radius=8, text="Download", width=200, height=50, command=self.button_event, font=("Roboto", 16))
        self.button.pack(pady=12, padx=10)

        self.progress_bar = ctkinter.CTkProgressBar(
            master=self.frame, indeterminate_speed=0.5, mode="indeterminate")
        self.progress_bar.set(0)

        self.label_status = ctkinter.CTkLabel(
            master=self.frame, width=50, height=25, font=("Roboto", 12))

    def button_event(self):
        """ Define event for button click.
        If input, start download process by spawn Thread and monitor it.
        """
        input = self.entry.get()
        if self.button.cget("text") != "Download":
            self.button.configure(text="Download")

        if input:
            downloader = Downloader(input)
            self.button.configure(state="disabled")
            self.label_status.configure(text="Downloading", text_color="white")
            self.label_status.pack(pady=6, padx=10)
            self.progress_bar.pack(pady=12, padx=10)
            self.progress_bar.start()
            try:
                t = Thread(target=self.start_download, args=(downloader,))
                t.start()
                self.monitor(t, downloader)
            except Exception as err:
                self.label_status.configure(
                    text="Error - {}".format(err), text_color="red")
                self.button.configure(state="normal", text="Try Again")
                self.progress_bar.stop()

    def start_download(self, downloader: Downloader):
        downloader.download_comic()

    def monitor(self, t: Thread, downloader: Downloader):
        # Monitor download process
        if t.is_alive() or not downloader.done():
            self.after(200, lambda: self.monitor(t, downloader))
        else:
            self.progress_bar.stop()
            self.button.configure(text="Download")
            self.button.configure(state="normal")
            self.label_status.configure(
                text="Done: {}".format(downloader.get_path()), text_color="white")
