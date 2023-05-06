
from abc import ABC
from abc import abstractmethod
import os
from configparser import ConfigParser

from qtpy.QtMultimedia import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import qtawesome as qta


from mainapplication import CONFIG_FILE


class MyMeta(type(ABC), type(QWidget)):
    pass


class WidgetBase(ABC, QWidget, metaclass=MyMeta):
    rate_defult = None
    volume_defult = None
    voice_defult = None
    class_now = None
    file_defult_suffix = None
    config_section_name = None

    playerStateChanged = Signal(QMediaPlayer.State)

    def __init__(self, *args, **kwargs):
        super(WidgetBase, self).__init__(*args, **kwargs)
        self.player = None
        self.media_content = None
        self.playfilename = None
        self.say_text = None
        self.say_paramas = None
        self.engine_obj = None

        self.voice = None
        self.rate = None
        self.volume = None

        self.init_defult()

        self.init_ui()
        self.init_range()
        self.init_MediaPlayer()
        self.init_engine()
        self.init_voices_combox()

        self.rate_slider_change(self.rate_defult)
        self.volume_slider_change(self.volume_defult)

        self.rate_slider.valueChanged.connect(self.rate_slider_change)
        self.volume_slider.valueChanged.connect(self.volume_slider_change)
        self.voices_combox.currentIndexChanged.connect(self.voices_combox_change)

        self.re_init_engine_btn.clicked.connect(self.init_voices_combox)
        self.about_voice_btn.clicked.connect(self.about_voice)
        self.preset_voice_btn.clicked.connect(self.preset_voice)
        self.reset_voice_btn.clicked.connect(self.reset_voice)
        # self.reset_voice_btn.clicked.connect(self.say)
        self.playerStateChanged.connect(self.play_btn_func)

    def init_defult(self):
        CONF = ConfigParser()
        CONF.read(CONFIG_FILE, encoding='utf-8')
        if CONF.has_option(self.config_section_name, "rate_defult"):
            self.rate_defult = float(CONF.get(self.config_section_name, "rate_defult"))
        else:
            pass
        self.rate = self.rate_defult

        if CONF.has_option(self.config_section_name, "volume_defult"):
            self.volume_defult = float(CONF.get(self.config_section_name, "volume_defult"))
        else:
            pass
        self.volume = self.volume_defult

        if CONF.has_option(self.config_section_name, "voice_defult"):
            self.voice_defult = CONF.get(self.config_section_name, "voice_defult")
        else:
            pass
        self.voice = self.voice_defult

    def init_ui(self):
        vlayout = QVBoxLayout(self)

        hlayout1 = QHBoxLayout()
        vlayout.addLayout(hlayout1)

        self.voices_combox = QComboBox(self)
        self.voices_combox.setFixedHeight(30)
        re_init_engine__Icon = qta.icon('fa.refresh',
                               color='blue', options=[{'scale_factor': 0.5}]
                               )
        self.re_init_engine_btn = QPushButton()
        self.re_init_engine_btn.setFixedSize(30, 30)
        self.re_init_engine_btn.setIcon(re_init_engine__Icon)
        self.re_init_engine_btn.setToolTip("重新启动发音引擎")

        self.about_voice_btn = QPushButton("关于")
        self.about_voice_btn.setFixedSize(100, 30)

        self.preset_voice_btn = QPushButton("预设")
        self.preset_voice_btn.setFixedSize(100, 30)
        self.preset_voice_btn.setToolTip("记忆当前配置语音参数")

        self.reset_voice_btn = QPushButton("重置")
        self.reset_voice_btn.setFixedSize(100, 30)
        self.reset_voice_btn.setToolTip("将语音参数重置为默认配置")

        hlayout1.addWidget(self.voices_combox)
        hlayout1.addWidget(self.re_init_engine_btn)
        hlayout1.addWidget(self.about_voice_btn)
        hlayout1.addWidget(self.preset_voice_btn)
        hlayout1.addWidget(self.reset_voice_btn)

        frame = QFrame()
        hlayout2 = QHBoxLayout()
        hlayout2.setSpacing(30)  # 设置各控件之间的间距
        frame.setLayout(hlayout2)

        ## 语速
        rate_layout = QVBoxLayout()
        rate_layout.setSpacing(5)
        rate_up_layout = QFormLayout()
        rate_up_label = QLabel("语速:")
        self.rate_up_value_label = QLabel("")
        rate_up_layout.addRow(rate_up_label, self.rate_up_value_label)
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.setFocusPolicy(Qt.StrongFocus)
        self.rate_slider.setTickPosition(QSlider.TicksBothSides)
        self.rate_slider.setTickInterval(10)
        self.rate_slider.setSingleStep(1)
        rate_layout.addLayout(rate_up_layout)
        rate_layout.addWidget(self.rate_slider)
        rate_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        ## 音量
        volume_layout = QVBoxLayout()
        volume_layout.setSpacing(5)
        volume_up_layout = QFormLayout()
        volume_up_label = QLabel("音量:")
        self.volume_up_value_label = QLabel("")
        volume_up_layout.addRow(volume_up_label, self.volume_up_value_label)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setFocusPolicy(Qt.StrongFocus)
        self.volume_slider.setTickPosition(QSlider.TicksBothSides)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setSingleStep(1)
        volume_layout.addLayout(volume_up_layout)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        hlayout2.addLayout(rate_layout)
        hlayout2.addLayout(volume_layout)

        vlayout.addWidget(frame)

    @abstractmethod
    def init_range(self):
        self.rate_slider.setMaximum(100)
        self.rate_slider.setMinimum(-99)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setMinimum(-99)

    @abstractmethod
    def init_engine(self):
        pass

    @abstractmethod
    def init_voices_combox(self):
        for i, item in enumerate(self.engine_obj.voice_all):
            self.voices_combox.addItem(item["FriendlyName"], item)
            if item["Name"] == self.voice_defult:
                self.voices_combox.setCurrentIndex(i)

    def init_MediaPlayer(self):
        self.player = QMediaPlayer(self)
        self.player.setVolume(100)
        self.player.stateChanged.connect(self.playerStateChanged.emit)

    @abstractmethod
    def voices_combox_change(self):
        data = self.voices_combox.currentData()
        self.voice = data["Name"]
        self.engine_obj.voice = self.voice

    @abstractmethod
    def rate_slider_change(self, value):
        if isinstance(value, str):
            self.rate = value
        elif isinstance(value, (int, float)):
            if value >= 0:
                flag = "+"
            else:
                flag = ""
            self.rate = f"{flag}{value}%"
        self.rate_up_value_label.setText(self.rate)
        self.engine_obj.rate = self.rate

    @abstractmethod
    def volume_slider_change(self, value):
        if isinstance(value, str):
            self.volume = value
        elif isinstance(value, (int, float)):
            if value >= 0:
                flag = "+"
            else:
                flag = ""
            self.volume = f"{flag}{value}%"
        self.volume_up_value_label.setText(self.volume)
        self.engine_obj.volume = self.volume

    @abstractmethod
    def about_voice(self):
        pass

    def preset_voice(self):
        CONF = ConfigParser()
        CONF.read(CONFIG_FILE, encoding='utf-8')

        CONF.set(self.config_section_name, "rate_defult", str(self.rate))
        CONF.set(self.config_section_name, "volume_defult", str(self.volume))
        CONF.set(self.config_section_name, "voice_defult", str(self.voice))

        CONF.write(open(CONFIG_FILE, "w"))

    def reset_voice(self):
        self.engine_obj.rate = self.class_now.rate_defult
        self.engine_obj.volume = self.class_now.volume_defult
        self.voice_defult = self.class_now.voice_defult
        self.init_voices_combox()

        self.rate_slider_change(self.class_now.rate_defult)
        self.volume_slider_change(self.class_now.volume_defult)

    def play_btn_func(self, state):
        # print(state)
        pass

    def say(self, text: str):
        self.playerStateChanged.emit(QMediaPlayer.PlayingState)
        say_paramas = f"{self.voice}{self.volume}{self.rate}"
        if self.say_text != text or self.say_paramas != say_paramas:
            self.say_text = text
            self.say_paramas = say_paramas
            self.media_content = None
            if self.playfilename and os.path.isfile(self.playfilename):
                os.remove(self.playfilename)
            self.playfilename = None
            # 生成文件
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.playfilename = self.engine_obj.say(self.say_text, suffix=self.file_defult_suffix)
            QApplication.restoreOverrideCursor()

            self.media_content = QMediaContent(QUrl.fromLocalFile(self.playfilename))
            self.player.setMedia(self.media_content)
        self.player.play()

    def save_to_file(self, text, filename):
        self.engine_obj.save_to_file(text, filename, rm_midfile=False)

    def list_save_to_file(self, text, filename):
        self.engine_obj.list_save_to_file(text, filename)

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def closeEvent(self, event:PySide2.QtGui.QCloseEvent) -> None:
        """
        程序退出时清理临时文件
        :param event:
        :return:
        """
        if self.playfilename and os.path.isfile(self.playfilename):
            os.remove(self.playfilename)


