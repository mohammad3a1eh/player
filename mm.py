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


mixer.init()

PATH = getcwd()
is_play = False
playlist = {
    "name": [],
    "path": []
}
played_music = None
played_count = 0
music_length = 0

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def ApplyStyleSheet(self, theme):
        if theme == MicaTheme.DARK:
            self.setStyleSheet(style.dark)
        else:
            self.setStyleSheet(style.light)


    def add_to_files(self, path):
        global files
        filename = path.split('\\')[-1]
        if filename not in files:
            files[filename] = path

    def init_ui(self):
        global playlist
        self.setWindowTitle('Music Player')
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 500)
        self.setMinimumSize(100, 100)
        self.setMinimumSize(100, 100)

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
        # self.music_name.setStyleSheet("border: 1px solid red")
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

        self.progressBar = QProgressBar(self)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 470, 300, 16))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateprogressbar)

        ApplyMica(self.winId(), MicaTheme.AUTO, MicaStyle.DEFAULT, OnThemeChange=self.ApplyStyleSheet)
        self.show()


    def add_file(self):
        file_paths = QFileDialog.getOpenFileNames(self,"Add Sound","","Sound Filed(*.mp3)")
        for file in file_paths[0]:
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
        index = self.music_list.currentIndex().data()

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

    def change_volume(self, value):
        volume = value / 100.0
        mixer.music.set_volume(volume)

    def play_item(self):
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
        global played_music, music_length, played_count, is_play
        played_count = 0
        self.timer.stop()
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


    def prevsong(self):
        global played_music, music_length, played_count, is_play
        played_count = 0
        self.timer.stop()
        try:
            played_music = playlist["name"][playlist["name"].index(played_music)-1]
        except IndexError:
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
        global played_count, music_length
        if is_play:
            played_count += 1
            self.progressBar.setValue(played_count)
            if played_count == music_length:
                self.nextsong()

    def play_pause(self):
        global is_play
        if is_play:
            is_play = False
            mixer.music.pause()
            self.play.setIcon(QIcon(fr"{PATH}/assets/icons/play.png"))
        else:
            is_play = True
            mixer.music.unpause()
            self.play.setIcon(QIcon(fr"{PATH}/assets/icons/pause.png"))







if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    sys.exit(app.exec_())
