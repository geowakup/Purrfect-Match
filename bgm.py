import os

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer


class BGMPlayer:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.audio_dir = os.path.join(self.base_dir, "assets", "audio")
        self.player = QMediaPlayer()
        self.player.setVolume(100)
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.current_track = None
        self._load_track()

    def _load_track(self):
        if not os.path.isdir(self.audio_dir):
            return

        tracks = [
            filename for filename in sorted(os.listdir(self.audio_dir))
            if filename.lower().endswith((".mp3", ".wav", ".ogg", ".flac"))
        ]

        if not tracks:
            return

        self.current_track = os.path.join(self.audio_dir, tracks[0])
        self.player.setSource(QUrl.fromLocalFile(self.current_track))

    def has_tracks(self):
        return self.current_track is not None

    def play(self):
        if self.has_tracks():
            self.player.play()

    def pause(self):
        if self.has_tracks():
            self.player.pause()

    def stop(self):
        if self.has_tracks():
            self.player.stop()

    def toggle(self):
        if not self.has_tracks():
            return False

        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.pause()
            return False

        self.play()
        return True

    def set_volume(self, value):
        self.player.setVolume(max(0, min(100, int(value))))
