# Most of the styles are from here: https://github.com/witalihirsch/QTVin11

from winreg import *

registry = ConnectRegistry(None,HKEY_CURRENT_USER)
key = OpenKey(registry, r'SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Explorer\\Accent')
key_value = QueryValueEx(key,'AccentColorMenu')
accent_int = key_value[0]
accent = accent_int-4278190080
accent = str(hex(accent)).split('x')[1]
accent = accent[4:6]+accent[2:4]+accent[0:2]
accent = 'rgb'+str(tuple(int(accent[i:i+2], 16) for i in (0, 2, 4)))

transparent = "background-color: transparent;"

dark = """
* {
    color: white;
}
QScrollBar:vertical {
    border: 6px solid rgb(255, 255, 255, 0);
    width: 16px;
}

QScrollBar:vertical:hover {
    border: 6px solid rgb(255, 255, 255, 0);
}

QScrollBar::handle:vertical {
    background-color: rgb(255, 255, 255, 130);
    border-radius: 2px;
    min-height: 25px;
}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar::add-line:vertical {
    height: 0px;
}

QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: 6px solid rgb(255, 255, 255, 0);
    height: 16px;
}

QScrollBar:horizontal:hover {
    border: 6px solid rgb(255, 255, 255, 0);
}

QScrollBar::handle:horizontal {
    background-color: rgb(255, 255, 255, 130);
    border-radius: 2px;
    min-width: 25px;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QScrollBar::add-line:horizontal {
height: 0px;
}

QScrollBar::sub-line:horizontal {
height: 0px;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
height: 0px;
}

QProgressBar {
    background-color: qlineargradient(spread:reflect, x1:0.5, y1:0.5, x2:0.5, y2:1, stop:0.119403 rgba(255, 255, 255, 250), stop:0.273632 rgba(0, 0, 0, 0));
    border-radius: 2px;
    min-height: 4px;
    max-height: 4px;
}

QProgressBar::chunk {
    background-color: """+accent+""";
    border-radius: 2px;
}

"""

light = """
* {
    color: black;
}
QScrollBar:vertical {
    border: 6px solid rgb(0, 0, 0, 0);
    width: 16px;
}

QScrollBar:vertical:hover {
    border: 6px solid rgb(0, 0, 0, 0);
}

QScrollBar::handle:vertical {
    background-color: rgb(0, 0, 0, 110);
    border-radius: 2px;
    min-height: 25px;
}

QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::sub-line:vertical:hover {
    height: 0px;
}

QScrollBar::sub-line:vertical:pressed {
    height: 0px;
}

QScrollBar::add-line:vertical {
    height: 0px;
}

QScrollBar::add-line:vertical:hover {
    height: 0px;
}

QScrollBar::add-line:vertical:pressed {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: 6px solid rgb(0, 0, 0, 0);
    height: 16px;
}

QScrollBar:horizontal:hover {
    border: 6px solid rgb(0, 0, 0, 0);
}

QScrollBar::handle:horizontal {
    background-color: rgb(0, 0, 0, 110);
    border-radius: 2px;
    min-width: 25px;
}

QScrollBar::sub-line:horizontal {
    height: 0px;
}

QScrollBar::sub-line:horizontal:hover {
    height: 0px;
}

QScrollBar::sub-line:horizontal:pressed {
    height: 0px;
}

QScrollBar::add-line:horizontal {
    height: 0px;
}

QScrollBar::add-line:horizontal:hover {
    height: 0px;
}

QScrollBar::add-line:horizontal:pressed {
    height: 0px;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QProgressBar {
    background-color: qlineargradient(spread:reflect, x1:0.5, y1:0.5, x2:0.5, y2:1, stop:0.233831 rgba(0, 0, 0, 255), stop:0.343284 rgba(0, 0, 0, 0));
    border-radius: 2px;
    min-height: 4px;
    max-height: 4px;
}

QProgressBar::chunk {
    background-color: """+accent+""";
    border-radius: 2px;
}
"""