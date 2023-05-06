#!/usr/bin/env python3


from qtpy.QtWidgets import *


from tts.edge_tts_engine import EdgeTtsEngine
from tts.WidgetBase import WidgetBase


class EdgeTtsWidget(WidgetBase):
    rate_defult = 0
    volume_defult = 0
    voice_defult = "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)"
    file_defult_suffix = '.mp3'
    config_section_name = 'edge_tts'

    def __init__(self, *args, **kwargs):
        super(EdgeTtsWidget, self).__init__(*args, **kwargs)
        self.class_now = EdgeTtsWidget
        self.setObjectName(self.config_section_name)

    def init_range(self):
        self.rate_slider.setMaximum(100)
        self.rate_slider.setMinimum(-99)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setMinimum(-99)

    def init_engine(self):
        self.engine_obj = EdgeTtsEngine(
            voice=self.voice_defult, rate=self.rate, volume=self.volume)

    def init_voices_combox(self):
        for i, item in enumerate(self.engine_obj.voice_all):
            self.voices_combox.addItem(item["FriendlyName"], item)
            if item["Name"] == self.voice_defult:
                self.voices_combox.setCurrentIndex(i)

    def voices_combox_change(self):
        data = self.voices_combox.currentData()
        self.voice = data["Name"]
        self.engine_obj.voice = self.voice

    def rate_slider_change(self, value):
        value = int(value)
        if value >= 0:
            flag = "+"
        else:
            flag = ""
        self.rate = value
        self.rate_up_value_label.setText(f"{flag}{value}%")
        self.engine_obj.rate = f"{flag}{value}%"

    def volume_slider_change(self, value):
        value = int(value)
        if value >= 0:
            flag = "+"
        else:
            flag = ""
        self.volume = value
        self.volume_up_value_label.setText(f"{flag}{value}%")
        self.engine_obj.volume = f"{flag}{value}%"

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
        self._ShortName = data.get("ShortName")
        self._FriendlyName = data.get("FriendlyName")
        self._Gender = data.get("Gender")
        self._Locale = data.get("Locale")
        self._Status = data.get("Status")
        self._Language = data.get("Language")

        self.setWindowTitle("关于")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        if self._Name:
            name_label = QLabel("Name:")
            name_detail_label = QLabel(self._Name)
            layout.addRow(name_label, name_detail_label)

        if self._ShortName:
            shortname_label = QLabel("ShortName:")
            shortname_detail_label = QLabel(self._ShortName)
            layout.addRow(shortname_label, shortname_detail_label)

        if self._FriendlyName:
            FriendlyName_label = QLabel("FriendlyName:")
            FriendlyName_detail_label = QLabel(self._FriendlyName)
            layout.addRow(FriendlyName_label, FriendlyName_detail_label)

        if self._Gender:
            Gender_label = QLabel("Gender:")
            Gender_detail_label = QLabel(self._Gender)
            layout.addRow(Gender_label, Gender_detail_label)

        if self._Locale:
            Locale_label = QLabel("Locale:")
            Locale_detail_label = QLabel(self._Locale)
            layout.addRow(Locale_label, Locale_detail_label)

        if self._Status:
            Status_label = QLabel("Status:")
            Status_detail_label = QLabel(self._Status)
            layout.addRow(Status_label, Status_detail_label)

        if self._Language:
            Language_label = QLabel("Language:")
            Language_detail_label = QLabel(self._Language)
            layout.addRow(Language_label, Language_detail_label)


if __name__ == "__main__":

    import sys
    from mainapplication import appctxt
    main_appctxt = appctxt
    mainWin = EdgeTtsWidget()
    mainWin.show()
    exit_code = main_appctxt.app.exec_()
    sys.exit(exit_code)
