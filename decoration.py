import random

from PySide6.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QFont


# =========================
# FLOATING EMOJI
# =========================
class FloatingDecoration(QLabel):
    def __init__(self, emoji, parent=None):
        super().__init__(emoji, parent)

        self.setStyleSheet("background: transparent;")
        self.setFont(QFont("Segoe UI Emoji", 18))

        self.x_speed = random.randint(-2, 2)
        self.y_speed = random.randint(1, 3)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.move(
            self.x() + self.x_speed,
            self.y() + self.y_speed
        )

        # Respawn at top
        if self.y() > self.parent().height():
            self.move(
                random.randint(0, self.parent().width()),
                -20
            )


# =========================
# ADD FLOATING DECORATIONS
# =========================
def setup_decorations(window):

    emojis = [
        "🌸",
        "⭐",
        "✨",
        "💖",
        "🎀",
        "🐾"
    ]

    window.decorations = []

    for _ in range(25):

        decor = FloatingDecoration(
            random.choice(emojis),
            window
        )

        decor.move(
            random.randint(0, window.width()),
            random.randint(0, window.height())
        )

        decor.show()

        window.decorations.append(decor)


# =========================
# BUTTON GLOW EFFECT
# =========================
def add_glow(widget, color="#ff7aa2"):

    glow = QGraphicsDropShadowEffect()

    glow.setBlurRadius(25)
    glow.setOffset(0)

    glow.setColor(QColor(color))

    widget.setGraphicsEffect(glow)