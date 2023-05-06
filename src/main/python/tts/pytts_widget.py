#!/usr/bin/env python3

from qtpy.QtWidgets import *

from tts.pytts_engine import Pyttsx3Engine
from tts.WidgetBase import WidgetBase


class PyTtsWidget(WidgetBase):
    rate_defult = 200
    volume_defult = 100
    voice_defult = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0"
    file_defult_suffix = '.wav'
    config_section_name = 'pytts3'

    def __init__(self, *args, **kwargs):
        super(PyTtsWidget, self).__init__(*args, **kwargs)
        self.class_now = PyTtsWidget
        self.setObjectName(self.config_section_name)

    def init_range(self):
        self.rate_slider.setMaximum(400)
        self.rate_slider.setMinimum(10)
        self.rate_slider.setValue(self.rate_defult)
        self.rate_slider.setTickInterval(40)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setMinimum(1)
        self.volume_slider.setValue(self.volume_defult)

    def init_engine(self):
        self.engine_obj = Pyttsx3Engine(
            voice=self.voice_defult, rate=self.rate, volume=self.volume)

    def init_voices_combox(self):
        for i, item in enumerate(self.engine_obj.voice_all):
            self.voices_combox.addItem(item["Description"], item)
            if item["Id"] == self.voice_defult:
                self.voices_combox.setCurrentIndex(i)

    def voices_combox_change(self):
        data = self.voices_combox.currentData()
        self.voice = data["Id"]
        self.engine_obj.voice = self.voice

    def rate_slider_change(self, value):
        self.rate = value
        self.rate_up_value_label.setText(str(self.rate))
        self.engine_obj.rate = self.rate

    def volume_slider_change(self, value):
        self.volume = value
        self.volume_up_value_label.setText(str(value))
        self.engine_obj.volume = self.volume/100

    def about_voice(self):
        data = self.voices_combox.currentData()
        aboutdialog = AboutDialog(data=data)
        aboutdialog.exec_()

    def play_btn_func(self, state):
        # print(state)
        pass


class AboutDialog(QDialog):
    def __init__(self, data: dict = None, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.data = data
        self._Name = data.get("Name")
        self._Description = data.get("Description")
        self._Id = data.get("Id")
        self._Gender = data.get("Gender")
        self._Age = data.get("Age")
        self._Vendor = data.get("Vendor")
        self._Language = data.get("Language")
        self._Language_code = data.get("Language_code")

        self.setWindowTitle("关于")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        if self._Name:
            name_label = QLabel("Name:")
            name_detail_label = QLabel(self._Name)
            layout.addRow(name_label, name_detail_label)

        if self._Description:
            description_label = QLabel("Description:")
            description_detail_label = QLabel(self._Description)
            layout.addRow(description_label, description_detail_label)

        if self._Id:
            id_label = QLabel("Id:")
            id_detail_label = QLabel(self._Id)
            layout.addRow(id_label, id_detail_label)

        if self._Gender:
            Gender_label = QLabel("Gender:")
            Gender_detail_label = QLabel(self._Gender)
            layout.addRow(Gender_label, Gender_detail_label)

        if self._Age:
            age_label = QLabel("Age:")
            age_detail_label = QLabel(self._Age)
            layout.addRow(age_label, age_detail_label)

        if self._Vendor:
            Vendor_label = QLabel("Vendor:")
            Vendor_detail_label = QLabel(self._Vendor)
            layout.addRow(Vendor_label, Vendor_detail_label)

        if self._Language:
            Language_label = QLabel("Language:")
            Language_detail_label = QLabel(self._Language)
            layout.addRow(Language_label, Language_detail_label)


if __name__ == "__main__":

    import sys
    from mainapplication import appctxt
    main_appctxt = appctxt
    mainWin = PyTtsWidget()
    mainWin.show()
    exit_code = main_appctxt.app.exec_()
    sys.exit(exit_code)