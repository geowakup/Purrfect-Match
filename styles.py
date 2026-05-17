import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THEME_DIR = os.path.join(BASE_DIR, "themes")


def load_theme(themes_name):
    path = os.path.join(THEME_DIR, f"{themes_name}.qss")

    with open(path, "r", encoding="utf-8") as file:
        return file.read()