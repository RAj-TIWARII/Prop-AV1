import os
import tkinter as tk
from tkinter import ttk
from pygame import mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x600")
        self.root.configure(bg="#212121")

        # Initialize Pygame Mixer
        mixer.init()

        # Get all songs from the folder
        self.playlist = self.load_songs()
        self.current_index = 0
        self.is_paused = False

        # Create UI Elements
        self.create_widgets()

    def load_songs(self):
        """Load all mp3 files from the current directory."""
        return [f for f in os.listdir('.') if f.endswith('.mp3')]

    def create_widgets(self):
        """Create and place the UI elements."""
        # Title Label with sleek UI
        title_label = tk.Label(self.root, text="🎶 Music Player 🎶", font=("Arial", 24, "bold"), fg="white", bg="#212121")
        title_label.pack(pady=10)

        # Music playing Image (replace with your own gif)
        self.music_img = tk.Label(self.root, text="Music Playing Image Here", font=("Arial", 16), fg="white", bg="#212121")
        self.music_img.pack(pady=10)

        # Playlist Frame
        self.playlist_frame = tk.Frame(self.root, bg="#424242")
        self.playlist_frame.pack(pady=20, fill="both", expand=True)

        # Playlist Listbox (with better design)
        self.playlist_box = tk.Listbox(self.playlist_frame, bg="#303030", fg="white", font=("Arial", 14), selectbackground="lightblue", selectforeground="black", bd=0)
        self.playlist_box.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Scrollbar for Playlist
        playlist_scrollbar = ttk.Scrollbar(self.playlist_frame, orient="vertical", command=self.playlist_box.yview)
        playlist_scrollbar.pack(side="right", fill="y")

        self.playlist_box.config(yscrollcommand=playlist_scrollbar.set)

        # Populate the playlist
        for song in self.playlist:
            self.playlist_box.insert("end", song)

        # Controls Frame with a modern look
        controls_frame = tk.Frame(self.root, bg="#212121")
        controls_frame.pack(pady=20)

        # Control Buttons with modern design
        self.play_button = tk.Button(controls_frame, text="Play", command=self.play_music, bg="#00b14a", fg="white", width=10, font=("Arial", 14), relief="flat")
        self.play_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.toggle_pause, bg="#ffab00", fg="white", width=10, font=("Arial", 14), relief="flat")
        self.pause_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop_music, bg="#e74c3c", fg="white", width=10, font=("Arial", 14), relief="flat")
        self.stop_button.grid(row=0, column=2, padx=10)

        self.prev_button = tk.Button(controls_frame, text="Previous", command=self.play_previous, bg="#bdc3c7", fg="white", width=10, font=("Arial", 14), relief="flat")
        self.prev_button.grid(row=1, column=0, padx=10, pady=10)

        self.next_button = tk.Button(controls_frame, text="Next", command=self.play_next, bg="#bdc3c7", fg="white", width=10, font=("Arial", 14), relief="flat")
        self.next_button.grid(row=1, column=2, padx=10, pady=10)

        # Loop Toggle Button
        self.loop_button = tk.Button(controls_frame, text="Loop: Off", command=self.toggle_loop, bg="#444444", fg="white", width=10, font=("Arial", 14), relief="flat")
        self.loop_button.grid(row=1, column=1, pady=10)

        # Volume Slider with professional touch
        volume_frame = tk.Frame(self.root, bg="#212121")
        volume_frame.pack(pady=20)

        tk.Label(volume_frame, text="Volume", font=("Arial", 14), fg="white", bg="#212121").pack(side="left", padx=10)
        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient="horizontal", command=self.set_volume, length=200)
        self.volume_slider.pack(side="left")
        self.volume_slider.set(50)

    def play_music(self):
        """Play the selected or current song."""
        if not self.playlist:
            return

        selected_index = self.playlist_box.curselection()
        if selected_index:
            self.current_index = selected_index[0]

        song_path = self.playlist[self.current_index]

        # Stop any current song
        mixer.music.stop()

        # Load and play the new song
        mixer.music.load(song_path)
        mixer.music.play()
        self.is_paused = False
        self.update_playlist_selection()

    def play_next(self):
        """Play the next song in the playlist."""
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_music()

    def play_previous(self):
        """Play the previous song in the playlist."""
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_music()

    def toggle_pause(self):
        """Pause or unpause the current song."""
        if mixer.music.get_busy():
            if not self.is_paused:
                mixer.music.pause()
                self.is_paused = True
            else:
                mixer.music.unpause()
                self.is_paused = False

    def stop_music(self):
        """Stop the music playback."""
        mixer.music.stop()
        self.is_paused = False

    def toggle_loop(self):
        """Toggle looping on or off."""
        self.is_looping = not self.is_looping
        self.loop_button.config(text=f"Loop: {'On' if self.is_looping else 'Off'}")
        if self.is_looping:
            mixer.music.set_endevent()  # Auto-repeat not built-in, handled externally if desired

    def set_volume(self, volume):
        """Set the music volume."""
        mixer.music.set_volume(float(volume) / 100)

    def update_playlist_selection(self):
        """Highlight the current song in the playlist."""
        self.playlist_box.selection_clear(0, "end")
        self.playlist_box.selection_set(self.current_index)
        self.playlist_box.activate(self.current_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
