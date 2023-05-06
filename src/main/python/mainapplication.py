import sys
import os
from configparser import ConfigParser

import cgitb
from qtpy import PYQT5, PYSIDE2
from fbs_runtime.application_context import cached_property
if PYQT5:
    from fbs_runtime.application_context.PyQt5 import ApplicationContext
elif PYSIDE2:
    from fbs_runtime.application_context.PySide2 import ApplicationContext
from qtpy.QtWidgets import QApplication
# import qdarkstyle
# from qdarkstyle.light.palette import LightPalette


class MyAppContext(ApplicationContext):
    @cached_property
    def app(self):
        mycustomapp = MyCustomApp(sys.argv)
        mycustomapp.setApplicationName(self.build_settings['app_name'])
        mycustomapp.setApplicationVersion(self.build_settings['version'])
        mycustomapp.mode_choosed = False
        return mycustomapp

    @cached_property
    def app_icon(self):
        """
        The app icon.
        """
        return self._qt_binding.QIcon(self.get_resource('Icon.ico'))


class MyCustomApp(QApplication):
    def __init__(self, *args, **kwargs):
        super(MyCustomApp, self).__init__(*args, **kwargs)
        # if PYQT5:
        #     self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5", palette=LightPalette))
        # elif PYSIDE2:
        #     self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside2", palette=LightPalette))
        # else:
        #     raise Exception("暂时不支持其他qt_api")


appctxt = MyAppContext()

CONFIG_FILE = os.path.join(appctxt.get_resource("data"), "config.txt")

if not os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, "w+") as f:
        pass

CONF = ConfigParser()
CONF.read(CONFIG_FILE, encoding='utf-8')

if not CONF.has_section("defult"):
    CONF.add_section("defult")

if not CONF.has_section("edge_tts"):
    CONF.add_section("edge_tts")

if not CONF.has_section("pytts3"):
    CONF.add_section("pytts3")
CONF.write(open(CONFIG_FILE, "w"))
