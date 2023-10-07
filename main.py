from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                            QLabel, QSlider, QFileDialog, QScrollBar, QScrollArea)
from PyQt5.QtCore import (Qt, QUrl, QPoint,  QEvent, 
                          QPropertyAnimation, QParallelAnimationGroup,
                          QVariantAnimation, QAbstractAnimation)

from pathlib import Path
import sys
import os
import random
import webbrowser

import resources # no del import "resources"


class PositionWindowMouse(QWidget):
    def __init__(self, parent=None):
        super(PositionWindowMouse, self).__init__(parent)
        self.start = QPoint(0, 0)
        self.pressing = False

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.move(self.mapToGlobal(self.movement))
            self.start = self.end

    def mouseReleaseEvent(self, event):
        self.pressing = False


class Panel(QWidget):
    def __init__(self, parent=None):
        super(Panel, self).__init__(parent)
        self.css = """
            QPushButton {
                border-radius: 5;
                background-color: none;
                border: none;
                color: white;
                font-size: 24px;
            }

            QPushButton#openfull_window {
                color: grey;
            }
            QPushButton#close_window:hover {
                color: grey;
            }
            QPushButton#hide_window:hover {
                color: grey
            }
            QWidget#plane {
                background-color: #292929
            }

            QWidget#plane_left_menu {
                background-color: #2E2E2E;
            }
            QLabel {
                font-size: 350px;
                color: #292929
            }
        """

        self.plane = QWidget(self)
        self.plane.setGeometry(-1, -1, 902, 50)
        self.plane.setObjectName('plane')
        self.plane.setStyleSheet(self.css)

        self.anim_and_info_creators = QPushButton(self)
        self.anim_and_info_creators.setGeometry(810, 739, 20, 20)
        self.anim_and_info_creators.setStyleSheet('background-color: none; border-radius: 10px;')

        self.title_bar = QLabel('Scrambler-MP3 ', self)
        self.title_bar.setStyleSheet("font-size: 18px; color: silver; background-color: none")
        self.title_bar.setGeometry(370, 10, 200, 30)

        self.hide_window = QPushButton('─', self)
        self.hide_window.setGeometry(750, 14, 25,25)
        self.hide_window.setObjectName('hide_window')
        self.hide_window.setStyleSheet(self.css)

        self.openfull_window = QPushButton('□', self)
        self.openfull_window.setGeometry(800, 12, 25, 25)
        self.openfull_window.setObjectName('openfull_window')
        self.openfull_window.setStyleSheet(self.css)

        self.close_window = QPushButton('×', self)
        self.close_window.setGeometry(850, 13, 25, 25)
        self.close_window.setObjectName('close_window')
        self.close_window.setStyleSheet(self.css)

        self.label_music = QLabel('♫', self)
        self.label_music.move(280, 150)
        self.label_music.setStyleSheet(self.css)
        self.label_music.adjustSize()


class MultiplayButton(QWidget):
    def __init__(self, parent = None):
        super(MultiplayButton, self).__init__(parent)
        self.css = """
        QPushButton {
            color: white;
            border-radius: 15;
            border: 1px solid #292929;
            font-size: 40px
        }
        QPushButton::hover{
            background-color: #444444
        }

        QPushButton#StopSound {
            font-size: 25px
        }

        """
        
        self.plane = QWidget(self)
        self.plane.setGeometry(0, 700, 902, 100)
        self.plane.setObjectName('plane')
        self.plane.setStyleSheet(Panel().css)

        self.PreviousPlaySound = QPushButton('◁', self)
        self.PreviousPlaySound.setGeometry(300, 725, 50, 50)
        self.PreviousPlaySound.setObjectName('PreviousPlaySound')
        self.PreviousPlaySound.setStyleSheet(self.css)

        self.PlaySound = QPushButton('▶', self)
        self.PlaySound.setGeometry(395, 715, 60, 60)
        self.PlaySound.setObjectName('PlaySound')
        self.PlaySound.setStyleSheet(self.css)

        self.StopSound = QPushButton('||', self)
        self.StopSound.setGeometry(393, 715, 60, 60)
        self.StopSound.setObjectName('StopSound')
        self.StopSound.setStyleSheet(self.css)
        self.StopSound.hide()

        self.NextPlaySound = QPushButton('▷', self)
        self.NextPlaySound.setGeometry(500, 725, 50, 50)
        self.NextPlaySound.setObjectName('NextPlaySound')
        self.NextPlaySound.setStyleSheet(self.css)

class InfoMedia(QWidget):
    def __init__(self, parent=None):
        super(InfoMedia, self).__init__(parent)
        self.css = """
            QLabel#author {
                color: silver;
                font-size: 16px;
            }

        """

        self.img_label = QLabel(self)
        self.img_label.setGeometry(190, 115, 500, 400)

        self._plane_label_info = QWidget(self)

        self._plane_label_info.setGeometry(190, 515, 500, 100)
        self._plane_label_info.setStyleSheet('background-color: #313131')
        self._plane_label_info.hide()

        self._author = QLabel(self._plane_label_info)
        self._author.setObjectName('author')
        self._author.setStyleSheet(self.css)
        self._author.setGeometry(10, 10, 250, 20)

        self._name_music = QLabel(self._plane_label_info)
        self._name_music.setObjectName('author')
        self._name_music.setStyleSheet(self.css)
        self._name_music.setGeometry(10, 40, 250, 20)

        
class Menu(QWidget):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        self.css = """
        QPushButton#open_folder_music {
            background-color: #02B6F4;
            font-size: 13px;
            color: silver;
        }
        QPushButton#open_folder_music:hover {
            color: white;
        }
        QPushButton#music_list {
            font-size: 10px;
        }
        QPushButton#open_menu {
            color: white;
            font-size: 40px;
            background-color: none;
            border: none;
        }
        QPushButton#open_menu:hover {
            color: grey;
        }
        QComboBox {
            background-color: #292929;
            color: white;
            border: none;
            font-size: 13px;
            border-radius: 3px;
        }
        QComboBox::drop-down {
            width: 0;
            border: 0;
        }
        QComboBox QAbstractItemView{
            color: grey;
            background-color: #292929;
            selection-background-color: #292929;
            border: none;
            selection-color: white;
            border-style: solid;
        }
        QScrollArea {
            border: 1px solid #292929;
        }
        QScrollArea:vertical {
            background-color: #292929;            
        }
        QScrollBar:vertical {
            background-color: #292929;
        }
        QScrollBar::handle:vertical {
            background-color: #303030;
            border-radius: 1px;
            width: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #393939;
        }
        QScrollBar::sub-line:vertical
        {
            margin: 3px 0px 3px 0px;
            border-color: none;  
            height: 10px;
            width: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::add-line:vertical
        {
            margin: 3px 0px 3px 0px;
            border-color: none;
            height: 10px;
            width: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
        {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
        {
            background: none;
        }
        """
        self.style_button_panel = """
        QPushButton {
            background-color: #292929;
            font-size: 12px;
            color: grey;
            padding: 10px;
            width: 359px;
            border-radius: none;
            border-bottom: 2px solid grey;
        }
        QPushButton::hover {
            color: white;
            font-size: 13px;
            border-bottom: 3px solid #00ACFC;
        }
        """
        
        self.open_menu = QPushButton('≡', self)
        self.open_menu.setGeometry(30, 4, 30, 40)
        self.open_menu.setObjectName('open_menu')
        self.open_menu.setStyleSheet(self.css)
        self.open_menu.clicked.connect(self.open_plane_menu)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(-901, 49, 900, 651)
        self.scroll_area.setStyleSheet(self.css)

        self.scroll_bar = QScrollBar(self)
        self.scroll_bar.setStyleSheet(self.css)
        self.scroll_area.setVerticalScrollBar(self.scroll_bar)
        
        self.plane_left_menu = QWidget(self)
        self.plane_left_menu.setGeometry(0, 0, 380, 651)
        self.plane_left_menu.setObjectName('plane_left_menu')
        self.plane_left_menu.setStyleSheet(Panel().css)
        self.scroll_area.setWidget(self.plane_left_menu)
        
        self.open_folder_music = QPushButton('Open Folder Music', self.scroll_area)
        self.open_folder_music.setGeometry(0, 0, 380, 48)
        self.open_folder_music.clicked.connect(self.open_folder_dialog)

        self.info_music_css = """
            QLabel#style_title {
                color: silver;
                font-size: 16px;
            }
            QRadioButton {
                color: white;
                border-bottom: 1px solid green;
            }
            QRadioButton:hover {
                border-bottom: 1px solid orange;
            }
            QPushButton#del_by_id {
                background-color: #313131;
                font-size: 15px;
                border: none;
            }
            QPushButton#del_by_id:hover {
                border-bottom: 1px solid red;
            }
            QCheckBox {
                color: white;
                font-size: 13px;
            }
            QCheckBox:hover {
                border-bottom: 1px solid green;
            }
        """

        self.telegram_and_github_button_style = """
            QPushButton {
                color: silver;
                font-size: 15px;
                border-radius: 2px;
            }
            QPushButton:hover {
                font-size: 15px;
                color: white;
                background-color: #2F2F30;
            }
            QPushButton#to_GitHub {
                border-bottom: 1px solid #02B6F4;
            }
            QPushButton#to_Telegram {
                border-bottom: 1px solid #02B6F4;           
            }
        """

        self.img_label_in_panel = QLabel(self.scroll_area)
        self.img_label_in_panel.setGeometry(490, 115, 300, 250)

        self.label_music_is_none_info = QLabel('♫', self.scroll_area)
        self.label_music_is_none_info.move(490, 80)
        self.label_music_is_none_info.setStyleSheet("font-size: 350px; color: #313131")
        self.label_music_is_none_info.adjustSize()

        self._plane_label_info_in_panel = QWidget(self.scroll_area)
        self._plane_label_info_in_panel.setGeometry(490, 365, 300, 100)
        self._plane_label_info_in_panel.setStyleSheet('background-color: #313131')
        self._plane_label_info_in_panel.hide()

        self._author_in_panel = QLabel(self._plane_label_info_in_panel)
        self._author_in_panel.setObjectName('style_title')
        self._author_in_panel.setStyleSheet(self.info_music_css)
        self._author_in_panel.setGeometry(10, 10, 250, 20)

        self._name_music_in_panel = QLabel(self._plane_label_info_in_panel)
        self._name_music_in_panel.setObjectName('style_title')
        self._name_music_in_panel.setStyleSheet(self.info_music_css)
        self._name_music_in_panel.setGeometry(10, 40, 250, 20)

        self.to_Telegram = QPushButton('Telegram', self.scroll_area)
        self.to_Telegram.setObjectName('to_Telegram')
        self.to_Telegram.setStyleSheet(self.telegram_and_github_button_style)
        self.to_Telegram.setGeometry(440, 570, 150, 30)
        self.to_Telegram.clicked.connect(self.open_telegram_channel)
        
        self.to_GitHub = QPushButton('GitHub', self.scroll_area)
        self.to_GitHub.setObjectName('to_GitHub')
        self.to_GitHub.setStyleSheet(self.telegram_and_github_button_style)
        self.to_GitHub.setGeometry(695, 570, 150, 30)
        self.to_GitHub.clicked.connect(self.open_github_repository)

        self.anim_group = QParallelAnimationGroup()
        self.AnimationPanel = QPropertyAnimation(self.scroll_area, b"pos")

        self.player = QMediaPlayer(self)
        self.player.setVolume(50)

        self.playlist = QMediaPlaylist(self.player)
        self.playlist.error()

        self.color_1 = QColor(240, 53, 218)
        self.color_2 = QColor(61, 217, 245)

        self._animation = QVariantAnimation(self)
        self._animation.setStartValue(0.00001)
        self._animation.setEndValue(0.9999)
        self._animation.setDuration(250)
        self._animation.valueChanged.connect(self._animate)

        self.isOpenPanel = False
        self.list_music = []
        self.pos_heigth = 50
        self.index_button = []
        self.list_button_panel = []
        self.identX = 0

    def _animate(self, value):
        self.qss = """
            font: 75 11pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius: 10px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1})".format(
            color1=self.color_1.name(), color2=self.color_2.name(), value=value
        )
        
        self.qss += grad
        self.open_folder_music.setStyleSheet(self.qss)

    def enterEvent(self, event: QEvent) -> None:
        self._animation.setDirection(QAbstractAnimation.Forward)
        self._animation.start()
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self._animation.setDirection(QAbstractAnimation.Backward)
        self._animation.start()
        return super().leaveEvent(event)
    
    def open_plane_menu(self):
        if self.isOpenPanel == False:
            self.AnimationPanel.setEndValue(QPoint(0, 49))
            self.AnimationPanel.setDuration(200)

            self.animation_group_tasks()
            self.isOpenPanel = True
        else:
            self.close_plane_menu()

    def close_plane_menu(self):
        self.AnimationPanel.setEndValue(QPoint(-901, 49))
        self.AnimationPanel.setDuration(200)

        self.animation_group_tasks()
        self.isOpenPanel = False

    def animation_group_tasks(self):
        self.anim_group.addAnimation(self.AnimationPanel)
        self.anim_group.start()

    def open_folder_dialog(self):
        filenames = QFileDialog.getExistingDirectory(self, "Выберите файлы MP3", "Музыка")
        try:
            files = os.listdir(filenames)
            
            for mp3 in files:
                _mp3 = f"{filenames}/{mp3}"

                if Path(_mp3).suffix == ".mp3":
                    if not _mp3 in self.list_music:
                        self.url = QUrl.fromLocalFile(_mp3)
                        self.playlist.addMedia(QMediaContent(self.url))
                        self.list_music.append(_mp3)

                        self.new_label = QPushButton(self.url.fileName()[:-4], self.plane_left_menu)
                        self.new_label.setGeometry(0, self.pos_heigth, 359, 120)
                        self.new_label.setStyleSheet(self.style_button_panel)
                        self.new_label.setToolTip(self.url.fileName())
                        self.new_label.setCursor(Qt.PointingHandCursor)
                        self.new_label.adjustSize()

                        self.new_label.clicked.connect(lambda state, indexButton=self.identX, objButton=self.new_label: self.get_obj_name(indexButton, objButton))
                        self.new_label.show()

                        self.list_button_panel.append(self.new_label)
                        self.identX += 1
                        self.pos_heigth += 38
                        self.index_music = 0

        except FileNotFoundError:
            pass

        if len(self.list_music) > 12:
            self.plane_left_menu.setGeometry(0, 49, 380, self.pos_heigth+20)

        self.player.setPlaylist(self.playlist)
        self.close_plane_menu()

    def get_obj_name(self, *args):
        self.player.playlist().setCurrentIndex(args[0])

    def open_telegram_channel(self):
        webbrowser.open("https://t.me/ProgramsCreatorRu")

    def open_github_repository(self):
        webbrowser.open('https://github.com/Shedrjoinzz')    


class MediaPlayer(QMainWindow, PositionWindowMouse, Menu, Panel, InfoMedia, MultiplayButton):
    def __init__(self):
        super(MediaPlayer, self).__init__()
        self.css = """
        QMainWindow{
            background-color: #202020;
        }
        QToolTip {
            color: silver;
            border: 1px solid #292929;
            background-color: #292929;
            font-size: 13px;
         }
        QWidget#plane_volume_music {
            background-color: #313131;
            border-radius: 10px;
        }
        QPushButton#set_volume_music {
            border-radius: 15px;
            background-color: #292929;
            font-size: 20px;
        }
        QPushButton#set_volume_music:hover {
            background-color: #313131;
        }

        QPushButton#del_list_button {
            color: grey;
            background-color: #292929;
            font-size: 14px;
            border: none;
            border-radius: 10px;
        }
        QLabel#number_music {
            font-size: 15px;
            color: grey;
        }
        QLabel {
            color: silver;
            font-size: 14px;
        }
        QSlider::groove:horizontal {  
                height: 10px;
                margin: 0px;
                border-radius: 5px;
                background: grey;
            }
        QSlider::handle:horizontal {
                background: #fff;
                border: 1px solid #E3DEE2;
                width: 17px;
                margin: -5px 0; 
                border-radius: 9px;
            }
        QSlider::sub-page:qlineargradient {
            background: orange;
            border-radius: 5px;
            }
        """

        self.setStyleSheet(self.css)
        self.PlaySound.clicked.connect(self.PlayMusic)
        self.StopSound.clicked.connect(self.PauseMusic)
        
        self.NextPlaySound.clicked.connect(self.NextMusic)
        self.PreviousPlaySound.clicked.connect(self.BackMusic)

        self.player.stateChanged.connect(self.handle_state_changed)
        self.player.currentMediaChanged.connect(self.Bar)
        
        self.statusBar().setStyleSheet("color: grey; font-size: 16px; background-color: #292929;")

        self.player.volumeChanged.connect(self.vchange)
        
        self.number_music = QLabel(self)
        self.number_music.setObjectName('number_music')
        self.number_music.setStyleSheet(self.css)
        self.number_music.setGeometry(165, 725, 100, 50)

        self.time_music = QLabel('00:00 | 00:00', self)
        self.time_music.setObjectName('number_music')
        self.time_music.setGeometry(20, 725, 100, 50)

        self.slider_music = QSlider(Qt.Horizontal, self)
        self.slider_music.setGeometry(0, 690, 900, 20)
        self.slider_music.sliderMoved.connect(self.scroll_music_position)

        self.plane_volume_music = QWidget(self)
        self.plane_volume_music.setObjectName('plane_volume_music')
        self.plane_volume_music.setGeometry(620, 670, 250, 50)
        self.plane_volume_music.hide()

        self.slider_volume = QSlider(Qt.Horizontal, self.plane_volume_music)
        self.slider_volume.setGeometry(10, 17, 200, 20)
        self.slider_volume.setMaximum(100)
        self.slider_volume.setValue(50)
        self.slider_volume.sliderMoved.connect(self.SetPlayPosition)

        self.volume = QLabel(self.plane_volume_music)
        self.volume.setText(f'{self.player.volume()}')
        self.volume.setStyleSheet(self.css)
        self.volume.setGeometry(215, 17, 50, 16)

        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(":/photo/two_volume.png"))

        self.set_volume_music = QPushButton(self)
        self.set_volume_music.setIcon(self.icon)
        self.set_volume_music.setObjectName('set_volume_music')
        self.set_volume_music.setStyleSheet(self.css)
        self.set_volume_music.setGeometry(650, 725, 50, 50)
        self.set_volume_music.clicked.connect(self.show_volum_panel)
        
        self.set_random = QPushButton(self)
        self.set_random.setIcon(QIcon(QPixmap(":/photo/random_off.png")))
        self.set_random.setObjectName('set_volume_music')
        self.set_random.setStyleSheet(self.css)
        self.set_random.setGeometry(720, 726, 50, 50)
        self.set_random.clicked.connect(self.set_random_music)

        self.set_while = QPushButton(self)
        self.set_while.setIcon(QIcon(QPixmap(":/photo/while_off.png")))
        self.set_while.setObjectName('set_volume_music')
        self.set_while.setStyleSheet(self.css)
        self.set_while.setGeometry(580, 726, 50, 50)
        self.set_while.clicked.connect(self.set_while_music)

        self.del_list_button = QPushButton('🗑', self)
        self.del_list_button.setGeometry(243, 740, 50, 50)
        self.del_list_button.setObjectName('del_list_button')        
        self.del_list_button.clicked.connect(self.active_del_function)
        self.del_list_button.adjustSize()
        self.del_list_button.setToolTip('Delete playlist')

        self._animation_label = QVariantAnimation(self)
        self._animation_label.setStartValue(0.00001)
        self._animation_label.setEndValue(0.9999)
        self._animation_label.setDuration(1000)
        self._animation_label.valueChanged.connect(self._animate_label)

        self.duraction_mins = 0
        self.duraction_second = 0
        self.position_mins = 0
        self.position_second = 0
        self.isRandomMusic = False
        self.isWhileMusic = False
        self.regulation_rand_music = ""
        
        self.player.durationChanged.connect(self.duraction_music)
        self.player.positionChanged.connect(self.position_music)

        self.close_window.clicked.connect(self.exit_window)
        self.hide_window.clicked.connect(self.hiden_window)

        self.player.mediaStatusChanged.connect(self.show_meta_data)

    def active_del_function(self):
        if self.list_music != []:
            for i in self.list_button_panel:
                i.hide()
            
            self.list_music.clear()
            self.playlist.clear()
            self.player.playlist().clear()
            self.list_button_panel.clear()
            self.StopSound.hide()
            self.PlaySound.show()
            self.plane_left_menu.setGeometry(0, 0, 380, 651)
            self.pos_heigth = 100
            self.identX = 0
            self.number_music.setText("")
            self.index_button.clear()

    def _animate_label(self, value):
        self.qss = """
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius: 10px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1})".format(
            color1=self.color_1.name(), color2=self.color_2.name(), value=value
        )
        self.qss += grad
        self.anim_and_info_creators.setStyleSheet(self.qss)

    def scroll_music_position(self, value):
        self.player.setPosition(value)

    def SetPlayPosition(self, value):
        self.player.setVolume(value)
        self.volume.setText(f'{self.player.volume()}')

    def duraction_music(self, value):
        self.slider_music.setMaximum(value)

        # Duraction
        self.duraction_mins = self.player.duration() // 1000 // 60
        self.duraction_second = self.player.duration() // 1000 % 60
        self.time_music.setText("{:02d}:{:02d} | {:02d}:{:02d}".format(self.position_mins, self.position_second, self.duraction_mins, self.duraction_second))
        
    def position_music(self, value):
        self.slider_music.setValue(value)
    
        # Position
        self.position_mins = value // 1000 // 60
        self.position_second = value // 1000 % 60
        self.time_music.setText("{:02d}:{:02d} | {:02d}:{:02d}".format(self.position_mins, self.position_second, self.duraction_mins, self.duraction_second))

    def show_volum_panel(self):
        if self.plane_volume_music.isHidden():
            self.plane_volume_music.show()
            self.set_volume_music.setStyleSheet('background-color: #313131')
        else:
            self.plane_volume_music.hide()
            self.set_volume_music.setStyleSheet(self.css)

    def vchange(self, value):
        if value == 0:
            self.icon.addPixmap(QPixmap(":/photo/off_volume.png"))

        elif value > 0 and value < 30:
            self.icon.addPixmap(QPixmap(":/photo/one_volume.png"))

        elif value >= 25 and value < 60:
            self.icon.addPixmap(QPixmap(":/photo/two_volume.png"))
            
        elif value >= 60:
            self.icon.addPixmap(QPixmap(":/photo/three_volume.png"))

        self.set_volume_music.setIcon(self.icon)

    def set_random_music(self):
        if self.isRandomMusic:
            self.set_random.setIcon(QIcon(QPixmap(":/photo/random_off.png")))
            self.isRandomMusic = False
            self.set_is_enbaled_list_button(flag=True)

        else:
            self.isRandomMusic = True
            self.set_random.setIcon(QIcon(QPixmap(":/photo/random_on.png")))
            self.set_is_enbaled_list_button()

    def set_is_enbaled_list_button(self, flag=False):
        if self.list_button_panel != []:
            for i in self.list_button_panel:
                i.setEnabled(flag)
                if flag:
                    i.setCursor(Qt.PointingHandCursor)
                else:
                    i.setCursor(Qt.ArrowCursor)

    def set_while_music(self):
        if self.isWhileMusic == False:
            self.set_while.setIcon(QIcon(QPixmap(":/photo/while_on.png")))
            self.isWhileMusic = 1

        elif self.isWhileMusic == 1:
            self.set_while.setIcon(QIcon(QPixmap(":/photo/while_on_one.png")))
            self.isWhileMusic = 2

        elif self.isWhileMusic == 2:
            self.set_while.setIcon(QIcon(QPixmap(":/photo/while_off.png")))
            self.isWhileMusic = False

    def PlayMusic(self):
        if self.list_music != []:
            self.player.play()
            self.PlaySound.hide()
            self.StopSound.show()

    def PauseMusic(self):
        if self.list_music != []:
            self.player.pause()
            self.PlaySound.show()
            self.StopSound.hide()        
    
    def show_meta_data(self, state):
        author = self.player.metaData('Author')
        title = self.player.metaData('Title')
        image = self.player.metaData('ThumbnailImage')
        if not image is None \
            and not author is None \
            and not title is None:

            self._author.setText(str(author[0]).title())
            self._author_in_panel.setText(str(author[0]).title())

            self._name_music.setText(str(title).title())
            self._name_music_in_panel.setText(str(title).title())
            
            self.img_label.setPixmap(QPixmap(image).scaled(500, 400))
            self.img_label_in_panel.setPixmap(QPixmap(image).scaled(300, 250))

            self.img_label.show()
            self.label_music.hide()
            self._plane_label_info.show()
            self.img_label_in_panel.show()
            self.label_music_is_none_info.hide()
            self._plane_label_info_in_panel.show()
        else:
            self.img_label.hide()
            self.label_music.show()
            self._plane_label_info.hide()
            self.img_label_in_panel.hide()
            self.label_music_is_none_info.show()
            self._plane_label_info_in_panel.hide()

    def Bar(self, media):
        self.media = media
        if not media.isNull() and self.list_button_panel != []:
            if self.isWhileMusic != 2 and self.isRandomMusic == False:
                self.index_music = self.player.playlist().currentIndex()

            if self.isRandomMusic:
                self.index_music = random.randint(0, len(self.list_music)-1)

            if not self.list_button_panel[self.index_music] in self.index_button:
                self.index_button.append(self.list_button_panel[self.index_music])
                self.list_button_panel[self.index_music].setStyleSheet(self.style_button_panel.replace('2px solid grey', '3px solid #F7BC13; font-size: 13px; color: #F7BC13; background-color: #313131;'))

            if len(self.index_button) == 2:
                self.index_button[0].setStyleSheet(self.style_button_panel)
                self.index_button.pop(0)
            
            self.player.playlist().setCurrentIndex(self.index_music)
            self.number_music.setText(f'{self.index_music+1}/{self.playlist.mediaCount()}')
            self.statusBar().showMessage(f'{self.media.canonicalUrl().fileName()}')

    def NextMusic(self):
        if self.list_music != []:
            if self.isRandomMusic:
                self.player.playlist().shuffle()

            if self.isRandomMusic == False:
                self.player.playlist().next()

    def BackMusic(self):
        if self.list_music != []:
            if self.isRandomMusic:
                self.player.playlist().shuffle()

            if self.isRandomMusic == False:
                self.player.playlist().previous()

    def handle_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self._animation_label.setDirection(QAbstractAnimation.Forward)
            self._animation_label.start()
            self.statusBar().showMessage(self.media.canonicalUrl().fileName())
            self.PlaySound.hide()
            self.StopSound.show()

        if state == QMediaPlayer.StoppedState:
            self.StopSound.hide()
            self.PlaySound.show()
            self.index_button[0].setStyleSheet(self.style_button_panel)
            if self.index_music+1 == len(self.list_music) and self.isWhileMusic == 1:
                self._animation_label.setDirection(QAbstractAnimation.Backward)
                self._animation_label.start()
                self.player.playlist().setCurrentIndex(0)
                self.player.play()

            if self.isWhileMusic == 2:
                self.player.playlist().setCurrentIndex(self.index_music)
                self.player.play()

        if state == QMediaPlayer.PausedState:
            self._animation_label.setDirection(QAbstractAnimation.Backward)
            self._animation_label.start()
            self.statusBar().showMessage('Pause')
            self.StopSound.hide()
            self.PlaySound.show()

    def hiden_window(self):
        self.showMinimized()

    def exit_window(self):
        sys.exit()

def main():
    app = QApplication(sys.argv)
    window = MediaPlayer()
    window.setFixedSize(900, 800)
    window.setWindowFlag(Qt.FramelessWindowHint)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()