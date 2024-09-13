"""
Project: Player
Author: Mohammad Saleh (mohammad3a1eh)
GitHub: https://github.com/mohammad3a1eh/player

Description:
This Python project is a multimedia player designed to play audio files from a user-friendly interface.
It allows users to browse, select, and play their favorite media files directly from their local storage.

Features:
- Support for various audio formats (just MP3).
- Simple and intuitive graphical user interface (GUI).
- Play, pause, stop, next, previous.
- Volume control and mute option.
- Playlist management: add, remove, and organize multiple media files.
- Display of media information, such as duration, file name, and current time.
- Lightweight and fast performance suitable for everyday use.

Dependencies:
- Python 3.x
- Required libraries: (list the necessary Python libraries like `pygame`, `win32mica`, `mutagen`, `winreg`, etc.)

Usage:
Run the main script to launch the player. Users can interact with the GUI to manage their media files and enjoy seamless playback.

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mutagen.mp3 import MP3
from os import getcwd, path
from win32mica import ApplyMica, MicaTheme, MicaStyle
from models import style
from models import loader
from pygame import mixer
import random
import os
import platform
import ctypes


# ===========thumbnail buttons=============
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton, QWinTaskbarButton
# =========================================


# Initialize the mixer module for sound playback
mixer.init()

# Get the current working directory and store it in PATH
PATH = getcwd()

# Define necessary variables
is_play = False
playlist = {
    "name": [],
    "path": []
}
played_music = None
played_count = 0
music_length = 0
mods = {
    "Repeat-all": fr"{PATH}/assets/icons/repeat.png",
    "Repeat-one": fr"{PATH}/assets/icons/repeatone.png",
    "Shuffle": fr"{PATH}/assets/icons/shuffle.png",
    "No-repeat": fr"{PATH}/assets/icons/norepeat.png"
}
mod = list(mods.keys())[0]

color = tuple(int(style.accent_[i:i+2], 16) for i in (0, 2, 4))


# Checks if dark mode is enabled by calling DwmGetWindowAttribute with attribute 20
def is_dark_mode():
    try:
        is_dark = ctypes.windll.dwmapi.DwmGetWindowAttribute(0, 20)
        return bool(is_dark)
    except:
        return False


# Checks if the Windows version is 11 by looking for "10.0.22000" in the version string
def win_11_detect():
    version = platform.version()
    if "10.0.22000" in version:
        return False
    else:
        return True




# Define the MusicPlayer class inheriting from QMainWindow
class MusicPlayer(QMainWindow):
    # Initialize the user interface
    def __init__(self):
        super().__init__()

        self.init_ui()



    # Apply the specified stylesheet based on the selected theme
    def ApplyStyleSheet(self, theme):
        if theme == MicaTheme.DARK:
            self.setStyleSheet(style.dark)
        else:
            self.setStyleSheet(style.light)



    # Add a file to the global 'files' dictionary if it is not already present
    def add_to_files(self, path):
        global files
        filename = path.split('\\')[-1]
        if filename not in files:
            files[filename] = path



    # Initialize the user interface components
    def init_ui(self):
        global playlist
        self.setWindowTitle('Music Player')
        self.setWindowIcon(QIcon(fr"{PATH}/assets/icons/music.png"))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 500)
        self.setMinimumSize(800, 500)
        self.setMaximumSize(800, 500)
        
        # ===========thumbnail buttons=============
        self.toolBar = QWinThumbnailToolBar(self)
        
        self.toolBtnPrev = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnPrev.setToolTip('Previous')
        self.toolBtnPrev.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.toolBtnPrev.clicked.connect(self.prevsong)
        self.toolBar.addButton(self.toolBtnPrev)
        
        self.toolBtnControl = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnControl.setToolTip('Play')
        self.toolBtnControl.setProperty('status', 0)
        self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.toolBtnControl.clicked.connect(self.play_pause)
        self.toolBar.addButton(self.toolBtnControl)
        
        self.toolBtnNext = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnNext.setToolTip('Next')
        self.toolBtnNext.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.toolBtnNext.clicked.connect(self.nextsong)
        self.toolBar.addButton(self.toolBtnNext)
        # =========================================

        self.cover_label = QLabel(self)
        self.cover_label.setGeometry(QRect(10, 10, 300, 300))
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_label.setPixmap(QPixmap(fr"{PATH}/assets/icons/music.png").scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio))

        self.music_list = QListView(self)
        self.music_list.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.music_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.music_list.setStyleSheet(style.transparent)
        self.music_list.setGeometry(QRect(320, 10, 470, 440))
        self.music_list.doubleClicked.connect(self.play_item)
        self.music_list.setIconSize(QSize(50,50))
        font = QFont()
        font.setPointSize(15)
        self.music_list.setFont(font)

        self.model = QStandardItemModel()
        self.music_list.setModel(self.model)
        self.music_list.setSpacing(5)

        self.addmusic = QPushButton(self)
        self.addmusic.setObjectName(u"addmusic")
        self.addmusic.setIconSize(QSize(31,31))
        self.addmusic.setIcon(QIcon(fr"{PATH}/assets/icons/add.png"))
        self.addmusic.setStyleSheet(style.transparent)
        self.addmusic.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addmusic.setGeometry(QRect(760, 460, 31, 31))
        self.addmusic.clicked.connect(self.add_file)
        self.addmusic.setFlat(True)

        self.removemusic = QPushButton(self)
        self.removemusic.setObjectName(u"removemusic")
        self.removemusic.setIconSize(QSize(31, 31))
        self.removemusic.setIcon(QIcon(fr"{PATH}/assets/icons/remove.png"))
        self.removemusic.setStyleSheet(style.transparent)
        self.removemusic.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.removemusic.clicked.connect(self.del_file)
        self.removemusic.setGeometry(QRect(720, 460, 31, 31))

        self.play = QPushButton(self)
        self.play.setObjectName(u"play")
        self.play.setIconSize(QSize(71, 71))
        self.play.setIcon(QIcon(fr"{PATH}/assets/icons/play.png"))
        self.play.setStyleSheet(style.transparent)
        self.play.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.play.setGeometry(QRect(90, 390, 71, 71))
        self.play.clicked.connect(self.play_pause)

        self.stop = QPushButton(self)
        self.stop.setObjectName(u"stop")
        self.stop.setIconSize(QSize(51, 51))
        self.stop.setIcon(QIcon(fr"{PATH}/assets/icons/stop.png"))
        self.stop.setStyleSheet(style.transparent)
        self.stop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.stop.setGeometry(QRect(180, 400, 51, 51))
        self.stop.clicked.connect(self.stopsong)

        self.back = QPushButton(self)
        self.back.setObjectName(u"back")
        self.back.setIconSize(QSize(51, 51))
        self.back.setIcon(QIcon(fr"{PATH}/assets/icons/back.png"))
        self.back.setStyleSheet(style.transparent)
        self.back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back.setGeometry(QRect(20, 400, 51, 51))
        self.back.clicked.connect(self.prevsong)

        self.next = QPushButton(self)
        self.next.setObjectName(u"next")
        self.next.setIconSize(QSize(51, 51))
        self.next.setIcon(QIcon(fr"{PATH}/assets/icons/next.png"))
        
        self.next.setStyleSheet(style.transparent)
        self.next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.next.setGeometry(QRect(250, 400, 51, 51))
        self.next.clicked.connect(self.nextsong)

        self.numberlist = QLabel(self)
        self.numberlist.setObjectName(u"numberlist")
        self.numberlist.setText("example text")
        self.numberlist.setGeometry(QRect(330, 460, 390, 31))
        font = QFont()
        font.setPointSize(10)
        self.numberlist.setFont(font)

        self.music_name = QLabel(self)
        self.music_name.setObjectName(u"music_name")
        self.music_name.setText("")
        self.music_name.setGeometry(QRect(10, 310, 300, 71))
        font1 = QFont()
        font1.setPointSize(13)
        self.music_name.setFont(font1)
        self.music_name.setWordWrap(True)
        self.music_name.setAlignment(Qt.AlignCenter)

        self.dial = QDial(self)
        self.dial.setObjectName(u"dial")
        self.dial.setGeometry(QRect(670, 450, 40, 50))
        self.dial.setRange(0, 100)
        self.dial.setValue(50)
        self.dial.setWrapping(False)
        mixer.music.set_volume(0.5)
        self.dial.valueChanged.connect(self.change_volume)
        
        self.mod_key = QPushButton(self)
        self.mod_key.setObjectName(u"mod_key")
        self.mod_key.setGeometry(QRect(635, 460, 31, 31))
        self.mod_key.setIconSize(QSize(31, 31))
        self.mod_key.setIcon(QIcon(mods[mod]))
        self.mod_key.setStyleSheet(style.transparent)
        self.mod_key.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.mod_key.clicked.connect(self.mod_key_action)
        

        self.progressBar = QSlider(Qt.Horizontal ,self)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 470, 300, 16))
        self.progressBar.setValue(24)
        self.progressBar.sliderMoved.connect(self.sliderMoved)
        self.progressBar.sliderReleased.connect(self.handleSliderReleased)
        

        # Initialize the timer with a 1-second interval and connect it to the updateprogressbar method
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateprogressbar)

        # Apply Mica style to the window and show the window
        if win_11_detect():
            ApplyMica(self.winId(), MicaTheme.AUTO, MicaStyle.DEFAULT, OnThemeChange=self.ApplyStyleSheet)
        else:
            if is_dark_mode():
                self.setStyleSheet(style.dark)
            else:
                self.setStyleSheet(style.light)
        self.show()
        
        self.auto_add_file()
        
        
        
    # ===========thumbnail buttons=============
    # Handle the show event to set the toolbar window
    def showEvent(self, event):
        super(MusicPlayer, self).showEvent(event)
        if not self.toolBar.window():
            self.toolBar.setWindow(self.windowHandle())
    # =========================================



    def add_file(self):
        """
        Opens a file dialog to select audio files and adds them to the playlist.
        For each selected file:
        - Adds the file name and path to the playlist.
        - Creates a list item for the file and adds it to the model.
        - Attempts to extract and display the album cover from the file.
        - Sets a default icon if the cover is not available.
        - Updates the label to show the total number of songs in the playlist.
        """
        
        file_paths = QFileDialog.getOpenFileNames(self,"Add Sound","","Sound Filed(*.mp3)")
        paths = file_paths[0]
            
        for file in paths:
            print(file_paths)
            playlist["name"].append(file.split("/")[-1])
            playlist["path"].append(file)

            item = QStandardItem(file.split("/")[-1])


            self.model.appendRow(item)

            audio = MP3(file)
            try:
                apic = audio.tags['APIC:'].data
                cover = QPixmap()
                cover.loadFromData(apic)
                cover = cover.scaled(50, 50, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            except:
                cover = QPixmap(fr"{PATH}/assets/icons/music.png").scaled(50, 50, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

            item.setData(QIcon(cover), QtCore.Qt.DecorationRole)
            self.numberlist.setText(f"There are {len(playlist['name'])} songs available")



    def auto_add_file(self):
        """
        Automatically adds files from a predefined list to the playlist.
        - Reads file paths from 'autoload.txt' using the 'mp3finder' method.
        - For each file path:
        - Adds the file name and path to the playlist.
        - Creates a list item for the file and appends it to the model.
        - Attempts to extract and display the album cover from the file.
        - Uses a default icon if the cover is not available.
        - Updates the label to show the total number of songs in the playlist.
        """
        
        paths = loader.mp3finder("autoload.txt")
            
        for file in paths:
            playlist["name"].append(file.split("/")[-1])
            playlist["path"].append(file)

            item = QStandardItem(file.split("/")[-1])


            self.model.appendRow(item)

            audio = MP3(file)
            try:
                apic = audio.tags['APIC:'].data
                cover = QPixmap()
                cover.loadFromData(apic)
                cover = cover.scaled(50, 50, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            except:
                cover = QPixmap(fr"{PATH}/assets/icons/music.png").scaled(50, 50, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

            item.setData(QIcon(cover), QtCore.Qt.DecorationRole)
            self.numberlist.setText(f"There are {len(playlist['name'])} songs available")



    def del_file(self):
        """
        Deletes the currently selected file from the playlist.
        - Retrieves the selected file name from the list view.
        - Attempts to remove the file's path and name from the playlist:
        - If successful, clears and rebuilds the model with the updated playlist.
        - For each remaining file:
            - Creates a list item and appends it to the model.
            - Attempts to extract and display the album cover.
            - Uses a default icon if the cover is not available.
        - Updates the label to show the new total number of songs in the playlist.
        - If the file name is not found, no action is taken (handles ValueError).
        """

        index = self.music_list.currentIndex().data()
        try:
            playlist["path"].remove(playlist["path"][playlist["name"].index(index)])
            playlist["name"].remove(index)

            self.model.clear()

            for file in playlist["name"]:
                item = QStandardItem(file)
                self.model.appendRow(item)
                audio = MP3(playlist["path"][playlist["name"].index(file)])

                try:
                    apic = audio.tags['APIC:'].data
                    cover = QPixmap()
                    cover.loadFromData(apic)
                    cover = cover.scaled(50, 50, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                except:
                    cover = QPixmap(fr"{PATH}/assets/icons/music.png").scaled(50, 50, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

                item.setData(QIcon(cover), QtCore.Qt.DecorationRole)
                self.numberlist.setText(f"There are {len(playlist['name'])} songs available")
        except ValueError:
            pass
        
        
        
    def change_volume(self, value):
        """
        Changes the volume of the music playback.
        - Converts the provided volume value (0-100) to a range between 0.0 and 1.0.
        - Sets the volume of the music mixer to the computed value.
        """

        volume = value / 100.0
        mixer.music.set_volume(volume)



    def play_item(self):
        """
        Plays the currently selected music item from the playlist.
        - Retrieves the selected file's path and updates global variables to reflect the currently playing track and reset play count.
        - Loads and starts playing the selected music file using the mixer.
        - Retrieves the length of the music track and updates the progress bar.
        - Starts the timer to update the progress bar.
        - Attempts to load and display the album cover for the music file; uses a default icon if the cover is not available.
        - Updates the cover label with the album cover image.
        - Sets the play status to 'True' and updates the displayed music name.
        - Changes the play button icon to a 'pause' icon.
        """

        global is_play, played_count, played_music, music_length
        index = self.music_list.currentIndex().data()
        music = playlist["path"][playlist["name"].index(index)]
        played_music = index
        played_count = 0

        mixer.music.load(music)
        mixer.music.play()

        audio = MP3(music)

        music_length = round(audio.info.length)
        self.progressBar.setMaximum(music_length)
        self.progressBar.setValue(played_count)
        self.timer.start()

        try:
            apic = audio.tags['APIC:'].data
            cover = QPixmap()
            cover.loadFromData(apic)
            cover = cover.scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        except:
            cover = QPixmap(fr"{PATH}/assets/icons/music.png").scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        self.cover_label.setPixmap(cover)
        is_play = True
        self.music_name.setText(playlist["name"][playlist["path"].index(music)])
        self.play.setIcon(QIcon(fr"{PATH}/assets/icons/pause.png"))



    def nextsong(self):
        """
        Plays the next song in the playlist.
        - Stops the timer and resets the play count.
        - Attempts to set the next song to play:
        - If the end of the playlist is reached, loops back to the first song.
        - Loads and plays the selected music file using the mixer.
        - Updates the progress bar with the length of the new track and starts the timer.
        - Attempts to load and display the album cover for the new track; uses a default icon if the cover is not available.
        - Updates the cover label with the album cover image.
        - Sets the play status to 'True' and updates the displayed music name.
        - Changes the play button icon to a 'pause' icon.
        """

        global played_music, music_length, played_count, is_play
        played_count = 0
        self.timer.stop()
        try:
            played_music = playlist["name"][playlist["name"].index(played_music)+1]
        except:
            played_music = playlist["name"][0]
        music = playlist["path"][playlist["name"].index(played_music)]

        mixer.music.load(music)
        mixer.music.play()

        audio = MP3(music)

        music_length = round(audio.info.length)
        self.progressBar.setMaximum(music_length)
        self.progressBar.setValue(played_count)
        self.timer.start()

        try:
            apic = audio.tags['APIC:'].data
            cover = QPixmap()
            cover.loadFromData(apic)
            cover = cover.scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        except:
            cover = QPixmap(fr"{PATH}/assets/icons/music.png").scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        self.cover_label.setPixmap(cover)
        is_play = True
        self.music_name.setText(playlist["name"][playlist["path"].index(music)])
        self.play.setIcon(QIcon(fr"{PATH}/assets/icons/pause.png"))
        
        
        
    def nextsong_auto(self):
        global played_music, music_length, played_count, is_play
        played_count = 0
        self.timer.stop()
        
        
        if mod == "Repeat-all":
            try:
                played_music = playlist["name"][playlist["name"].index(played_music)+1]
            except IndexError:
                played_music = playlist["name"][0]
                
            music = playlist["path"][playlist["name"].index(played_music)]

            mixer.music.load(music)
            mixer.music.play()

            audio = MP3(music)

            music_length = round(audio.info.length)
            self.progressBar.setMaximum(music_length)
            self.progressBar.setValue(played_count)
            self.timer.start()
        elif mod == "Repeat-one":
            try:
                played_music = playlist["name"][playlist["name"].index(played_music)]
            except IndexError:
                played_music = playlist["name"][0]
                
            music = playlist["path"][playlist["name"].index(played_music)]

            mixer.music.load(music)
            mixer.music.play()

            audio = MP3(music)

            music_length = round(audio.info.length)
            self.progressBar.setMaximum(music_length)
            self.progressBar.setValue(played_count)
            self.timer.start()
        elif mod == "Shuffle":
            maximum = len(playlist["name"])
            choice = random.randint(0, maximum)
            
            played_music = playlist["name"][choice]
            music = playlist["path"][playlist["name"].index(played_music)]

            mixer.music.load(music)
            mixer.music.play()

            audio = MP3(music)

            music_length = round(audio.info.length)
            self.progressBar.setMaximum(music_length)
            self.progressBar.setValue(played_count)
            self.timer.start()
            
        elif mod == "No-repeat":
            audio = ""
        

        try:
            apic = audio.tags['APIC:'].data
            cover = QPixmap()
            cover.loadFromData(apic)
            cover = cover.scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        except:
            cover = QPixmap(fr"{PATH}/assets/icons/music.png").scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        self.cover_label.setPixmap(cover)
        is_play = True
        try:
            self.music_name.setText(playlist["name"][playlist["path"].index(music)])
        except:
            pass
        self.play.setIcon(QIcon(fr"{PATH}/assets/icons/pause.png"))



    def prevsong(self):
        """
        Plays the previous song in the playlist.
        - Stops the timer and resets the play count.
        - Attempts to set the previous song to play:
        - If at the beginning of the playlist, loops back to the last song.
        - Loads and plays the selected music file using the mixer.
        - Updates the progress bar with the length of the new track and starts the timer.
        - Attempts to load and display the album cover for the new track; uses a default icon if the cover is not available.
        - Updates the cover label with the album cover image.
        - Sets the play status to 'True' and updates the displayed music name.
        - Changes the play button icon to a 'pause' icon.
        """

        global played_music, music_length, played_count, is_play
        played_count = 0
        self.timer.stop()
        try:
            played_music = playlist["name"][playlist["name"].index(played_music)-1]
        except:
            played_music = playlist["name"][-1]


        music = playlist["path"][playlist["name"].index(played_music)]
        mixer.music.load(music)
        mixer.music.play()

        audio = MP3(music)

        music_length = round(audio.info.length)
        self.progressBar.setMaximum(music_length)
        self.progressBar.setValue(played_count)
        self.timer.start()

        try:
            apic = audio.tags['APIC:'].data
            cover = QPixmap()
            cover.loadFromData(apic)
            cover = cover.scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        except:
            cover = QPixmap(fr"{PATH}/assets/icons/music.png").scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        self.cover_label.setPixmap(cover)
        is_play = True
        self.music_name.setText(playlist["name"][playlist["path"].index(music)])
        self.play.setIcon(QIcon(fr"{PATH}/assets/icons/pause.png"))



    def stopsong(self):
        """
        Stops the current song and resets the player.
        - Stops the timer and resets the play count.
        - Stops the music playback and clears the progress bar.
        - Updates the cover label to show a default music icon.
        - Resets the play status and clears the displayed music name.
        - Changes the play button icon to a 'play' icon.
        """

        global played_count, played_music, is_play
        played_count = 0
        try:
            self.timer.stop()
        except:
            pass

        played_music = None
        mixer.music.stop()

        self.progressBar.setValue(0)
        cover = QPixmap(fr"{PATH}/assets/icons/music.png").scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.cover_label.setPixmap(cover)
        is_play = True
        self.music_name.setText("")
        self.play.setIcon(QIcon(fr"{PATH}/assets/icons/play.png"))



    def updateprogressbar(self):
        """
        Updates the progress bar based on the current playback position.
        - Increments the play count if a song is playing.
        - Updates the progress bar with the current play count.
        - If the end of the song is reached, automatically plays the next song.
        """

        global played_count, music_length
        if is_play:
            played_count += 1
            self.progressBar.setValue(played_count)
            if played_count == music_length:
                self.nextsong_auto()
                
                

    def play_pause(self):
        """
        Toggles between play and pause states for the current song.
        - If the song is playing, pauses it and updates the play button icon to 'play'.
        - If the song is paused, resumes playback and updates the play button icon to 'pause'.
        """

        global is_play
        if is_play:
            is_play = False
            mixer.music.pause()
            self.play.setIcon(QIcon(fr"{PATH}/assets/icons/play.png"))
            self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.toolBtnControl.setToolTip('Play')
        else:
            is_play = True
            mixer.music.unpause()
            self.play.setIcon(QIcon(fr"{PATH}/assets/icons/pause.png"))
            self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.toolBtnControl.setToolTip('Pause')
            
            
    
    def mod_key_action(self):
        """
        This function changes the current music playback mode.

        - It checks the current mode stored in the global variable 'mod'.
        - Then it cycles through the available modes in the 'mods' dictionary.
        - If the current mode is the last one, it resets to the first mode.
        - Otherwise, it moves to the next mode in the list.
        - Finally, the corresponding icon for the new mode is updated on the UI, reflecting the change in playback mode.

        This allows the user to switch between different playback modes (e.g., shuffle, repeat) for music tracks.
        """
        
        global mod
        
        n_mod = list(mods.keys()).index(mod)
        count_mod = len(list(mods.keys())) - 1
        
        if n_mod == count_mod:
            mod = list(mods.keys())[0]
        else:
            mod = list(mods.keys())[n_mod + 1]
            
        self.mod_key.setIcon(QIcon(mods[mod]))

    
        
    def sliderMoved(self):
        """
        This function is triggered when the user moves the slider.
        It manually adjusts the current position of the music track being played.
        
        - Retrieves the current value of the slider (representing the position in the track).
        - Updates the 'played_count' variable globally to reflect this new position.
        """
        
        global played_count

        value = self.progressBar.value()
        played_count = value
        mixer.music.stop()

        

    def handleSliderReleased(self):
        """
        This function is triggered when the user releases the mouse after moving the slider.
        It starts playing the music from the new position set by the slider.
        """
        
        mixer.music.play(start=played_count)
            


# Starts the application and runs the music player
if __name__ == '__main__':
    if win_11_detect():
        app = QApplication(sys.argv)
    else:
        if is_dark_mode():
            os.environ[
                "QTWEBENGINE_CHROMIUM_FLAGS"
            ] = "--blink-settings=darkMode=4,darkModeImagePolicy=2"
            app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        else:
            app = QApplication(sys.argv)
    
    player = MusicPlayer()
    sys.exit(app.exec_())



# All """comments""" in this code are written by ChatGPT, an AI language model, to provide explanations and descriptions of the functionality and behavior of the code.
