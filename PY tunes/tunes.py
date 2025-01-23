import os
import tkinter as tk
from tkinter import filedialog, ttk
from pygame import mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Music Player")
        self.root.geometry("400x500")
        self.root.configure(bg="#333")

        # Initialize Pygame Mixer
        mixer.init()

        # Track List and Current Song
        self.playlist = []
        self.current_song = None

        # Create UI Elements
        self.create_widgets()

    def create_widgets(self):
        """Create and place the UI elements."""
        # Title Label
        title_label = tk.Label(self.root, text="Music Player", font=("Arial", 20, "bold"), fg="white", bg="#333")
        title_label.pack(pady=10)

        # Playlist Frame
        self.playlist_frame = tk.Frame(self.root, bg="#444")
        self.playlist_frame.pack(pady=10, fill="both", expand=True)

        self.playlist_box = tk.Listbox(self.playlist_frame, bg="#222", fg="white", font=("Arial", 14), selectbackground="skyblue", selectforeground="black")
        self.playlist_box.pack(side="left", fill="both", expand=True)

        playlist_scrollbar = ttk.Scrollbar(self.playlist_frame, orient="vertical", command=self.playlist_box.yview)
        playlist_scrollbar.pack(side="right", fill="y")

        self.playlist_box.config(yscrollcommand=playlist_scrollbar.set)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#333")
        btn_frame.pack(pady=20)

        self.add_button = tk.Button(btn_frame, text="Add Song", command=self.add_song, bg="skyblue", fg="black", width=12, font=("Arial", 12))
        self.add_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(btn_frame, text="Play", command=self.play_music, bg="green", fg="white", width=12, font=("Arial", 12))
        self.play_button.grid(row=0, column=1, padx=10)

        self.pause_button = tk.Button(btn_frame, text="Pause", command=self.pause_music, bg="orange", fg="white", width=12, font=("Arial", 12))
        self.pause_button.grid(row=1, column=0, pady=10, padx=10)

        self.stop_button = tk.Button(btn_frame, text="Stop", command=self.stop_music, bg="red", fg="white", width=12, font=("Arial", 12))
        self.stop_button.grid(row=1, column=1, pady=10, padx=10)

    def add_song(self):
        """Add a new song to the playlist."""
        file_path = filedialog.askopenfilename(title="Select a Song", filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            self.playlist.append(file_path)
            self.playlist_box.insert("end", os.path.basename(file_path))

    def play_music(self):
        """Play the selected song."""
        if not self.playlist:
            return

        selected_index = self.playlist_box.curselection()
        if not selected_index:
            return

        song_path = self.playlist[selected_index[0]]

        # Stop any current song
        mixer.music.stop()

        # Load and play the new song
        mixer.music.load(song_path)
        mixer.music.play()
        self.current_song = song_path

    def pause_music(self):
        """Pause or unpause the music."""
        if mixer.music.get_busy():
            mixer.music.pause()

    def stop_music(self):
        """Stop the music playback."""
        mixer.music.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
