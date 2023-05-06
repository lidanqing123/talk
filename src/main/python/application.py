#!/usr/bin/env python
import os.path
from configparser import ConfigParser

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtPrintSupport import *
from qtpy.QtWidgets import *

# Local imports
import qtawesome as qta

from tts.edge_tts_widget import EdgeTtsWidget
from tts.pytts_widget import PyTtsWidget
from mainapplication import CONFIG_FILE
from mainapplication import appctxt


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.current_engine = None
        self.save_dir = None
        self.resize(1200, 600)
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.init_defult()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("Talk")

        self.newFile()

    def init_defult(self):
        CONF = ConfigParser()
        CONF.read(CONFIG_FILE, encoding='utf-8')
        if CONF.has_option("defult", "save_dir"):
            self.save_dir = CONF.get("defult", "save_dir")
        else:
            self.save_dir = QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[0]

        if CONF.has_option("defult", "current_engine"):
            self.current_engine = CONF.get("defult", "current_engine")
        else:
            self.current_engine = None

    def newFile(self):
        self.textEdit.clear()

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  "Choose a file", self.save_dir, "文本文件 (*.txt)")
        if not filename:
            return
        self.save_dir = os.path.dirname(filename)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        with open(filename, "r") as f:
            self.textEdit.setText(f.read())
        QApplication.restoreOverrideCursor()

    def print_(self):
        document = self.textEdit.document()
        printer = QPrinter()

        dlg = QPrintDialog(printer, self)
        if dlg.exec_() != QDialog.Accepted:
            return

        document.print_(printer)

        self.statusBar().showMessage("Ready", 2000)

    def savetext(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                                                  "Choose a file name", self.save_dir, "文本文件 (*.txt)")
        if not filename:
            return

        self.save_dir = os.path.dirname(filename)
        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Dock Widgets",
                                "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def saveaudio(self):
        ttswidget = self.tabWidget.currentWidget()
        saytext = self.textEdit.toPlainText().strip()
        if saytext:
            filename, _ = QFileDialog.getSaveFileName(self,
                                                      "Choose a file name",
                                                      self.save_dir,
                                                      "Audio files (*.mp3 *.wav)",
                                                      options=QFileDialog.DontUseNativeDialog)
            if not filename:
                return

            self.save_dir = os.path.dirname(filename)
            QApplication.setOverrideCursor(Qt.WaitCursor)
            ttswidget.save_to_file(saytext, filename)
            file = QFile(filename + ".txt")
            if not file.open(QFile.WriteOnly | QFile.Text):
                QMessageBox.warning(self, "Dock Widgets",
                                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
                pass
            out = QTextStream(file)
            out << self.textEdit.toPlainText()
            QApplication.restoreOverrideCursor()
            self.statusBar().showMessage("Saved '%s'" % filename, 2000)
        else:
            QMessageBox.warning(self, "save text to audio",
                                "没有需要转换的文字")

    def text_split_audio_save(self):

        ttswidget = self.tabWidget.currentWidget()
        saytext = self.textEdit.toPlainText().strip()
        if saytext:
            dir = QFileDialog.getExistingDirectory(self,
                                                   "选择一个目录",
                                                   self.save_dir,
                                                   QFileDialog.ShowDirsOnly)
            if not dir:
                return
            self.save_dir = dir
            QApplication.setOverrideCursor(Qt.WaitCursor)
            ttswidget.list_save_to_file(saytext.split("\n"), dir)
            QApplication.restoreOverrideCursor()
            self.statusBar().showMessage("Saved text_split_audio", 2000)
        else:
            QMessageBox.warning(self, "text split audio save",
                                "没有需要转换的文字")

    def undo(self):
        document = self.textEdit.document()
        document.undo()

    def playaudio(self):
        ttswidget = self.tabWidget.currentWidget()
        saytext = self.textEdit.toPlainText().strip()
        if saytext:
            ttswidget.say(saytext)
        else:
            QMessageBox.warning(self, "play audio",
                                "没有需要转换的文字")

    def pauseaudio(self):
        ttswidget = self.tabWidget.currentWidget()
        ttswidget.pause()

    def stopaudio(self):
        ttswidget = self.tabWidget.currentWidget()
        ttswidget.stop()

    def toggleViewsettings(self):
        if self.settings_dock.isVisible():
            self.settings_dock.hide()
        else:
            self.settings_dock.show()

    def about(self):
        QMessageBox.about(self, "About Talk",
                          """
                          <b>{app_name}</b> 是一个文本转语音工具，集成了edge_tts和pytts
                          <br>
                          <br>作者：{author}
                          <br>版本: {version}
                          <br>e-mail: 492847382@qq.com
                          """.format(**appctxt.build_settings)

                          )

    def createActions(self):
        newFileIcon = qta.icon('msc.new-file',
                               color='blue'
                               )
        self.newFileAct = QAction(newFileIcon, "&新建",
                                  self, shortcut=QKeySequence.New,
                                  statusTip="Create a new text file", triggered=self.newFile)

        previousFileIcon = qta.icon('fa.folder-open-o',
                                    color='blue'
                                    )
        self.previousFileAct = QAction(previousFileIcon, "&打开以前文件",
                                       self, shortcut=QKeySequence.Open,
                                       statusTip="open a text file", triggered=self.openFile)

        savFileIcon = qta.icon('ri.save-3-fill',
                               color='blue'
                               )
        self.savetextAct = QAction(savFileIcon, "&保存...", self,
                                   shortcut=QKeySequence.Save,
                                   statusTip="Save the current text file", triggered=self.savetext)

        saveaudioIcon = qta.icon('fa.file-audio-o',
                                 color='blue'
                                 )
        self.saveaudioAct = QAction(saveaudioIcon, "&保存音频文档...", self,
                                    shortcut=QKeySequence("Alt+S"),
                                    statusTip="保存音频文档", triggered=self.saveaudio)

        text_split_audioIcon = qta.icon('ri.file-shred-line',
                                        color='blue'
                                        )
        self.text_split_audioAct = QAction(text_split_audioIcon, "&分割并转换成音频文档...", self,
                                           shortcut=QKeySequence("Ctrl+F7"),
                                           statusTip="分割并转换成音频文档", triggered=self.text_split_audio_save)

        playaudioIcon = qta.icon('fa5.play-circle',
                                 color='blue'
                                 )
        self.playaudioAct = QAction(playaudioIcon, "&朗读...", self,
                                    shortcut=QKeySequence(Qt.Key_F5),
                                    statusTip="朗读", triggered=self.playaudio)

        pauseaudioIcon = qta.icon('fa5.pause-circle',
                                  color='blue'
                                  )
        self.pauseaudioAct = QAction(pauseaudioIcon, "&暂停...", self,
                                     shortcut=QKeySequence(Qt.Key_F6),
                                     statusTip="暂停", triggered=self.pauseaudio)

        stopaudioIcon = qta.icon('fa5.stop-circle',
                                 color='blue'
                                 )
        self.stopaudioAct = QAction(stopaudioIcon, "&停止...", self,
                                    shortcut=QKeySequence(Qt.Key_F7),
                                    statusTip="停止", triggered=self.stopaudio)

        settingaudioIcon = qta.icon('ri.user-settings-line',
                                    color='blue'
                                    )
        self.settingaudioAct = QAction(settingaudioIcon, "&配置声音...", self,
                                       # shortcut=QKeySequence.Save,
                                       statusTip="配置声音", triggered=self.toggleViewsettings)

        printIcon = qta.icon('fa.print',
                             color='blue'
                             )
        self.printAct = QAction(printIcon, "&打印...", self,
                                shortcut=QKeySequence.Print,
                                statusTip="Print the current form letter",
                                triggered=self.print_)

        self.undoAct = QAction(QIcon(':/images/undo.png'), "&Undo", self,
                               shortcut=QKeySequence.Undo,
                               statusTip="Undo the last editing action", triggered=self.undo)

        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                               statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&文件")
        self.fileMenu.addAction(self.newFileAct)
        self.fileMenu.addAction(self.previousFileAct)
        self.fileMenu.addAction(self.savetextAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveaudioAct)
        self.fileMenu.addAction(self.text_split_audioAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&编辑")
        self.editMenu.addAction(self.undoAct)

        self.pronounceMenu = self.menuBar().addMenu("&发音")
        self.pronounceMenu.addAction(self.playaudioAct)
        self.pronounceMenu.addAction(self.pauseaudioAct)
        self.pronounceMenu.addAction(self.stopaudioAct)
        self.pronounceMenu.addSeparator()
        self.pronounceMenu.addAction(self.saveaudioAct)
        self.pronounceMenu.addAction(self.text_split_audioAct)

        self.viewMenu = self.menuBar().addMenu("&声音")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&说明")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.fileToolBar = QToolBar("File")
        self.fileToolBar.setMovable(False)
        self.fileToolBar.setFixedHeight(35)
        self.fileToolBar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.TopToolBarArea, self.fileToolBar)
        self.fileToolBar.addAction(self.newFileAct)
        self.fileToolBar.addAction(self.previousFileAct)
        self.fileToolBar.addAction(self.savetextAct)
        self.fileToolBar.addAction(self.printAct)

        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.saveaudioAct)
        self.fileToolBar.addAction(self.text_split_audioAct)

        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.playaudioAct)
        self.fileToolBar.addAction(self.pauseaudioAct)
        self.fileToolBar.addAction(self.stopaudioAct)

        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.settingaudioAct)

        # 语音文件 处理

        #
        # self.editToolBar = QToolBar("Edit")
        # self.editToolBar.setFixedHeight(30)
        # self.addToolBar(self.editToolBar)
        # self.editToolBar.addAction(self.undoAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        self.settings_dock = settings_dock = QDockWidget("配置声音", self)
        self.settings_dock.setMaximumHeight(200)
        settings_dock.setAllowedAreas(Qt.TopDockWidgetArea)
        self.tabWidget = QTabWidget()

        self.tab1 = EdgeTtsWidget()
        self.tabWidget.addTab(self.tab1, "edge tts")
        if self.current_engine == self.tab1.objectName():
            self.tabWidget.setCurrentWidget(self.tab1)

        self.tab2 = PyTtsWidget()
        self.tabWidget.addTab(self.tab2, "pyttsx3")
        if self.current_engine == self.tab2.objectName():
            self.tabWidget.setCurrentWidget(self.tab2)

        self.tabWidget.currentChanged.connect(self.change_current_engine)

        settings_dock.setWidget(self.tabWidget)
        self.addDockWidget(Qt.TopDockWidgetArea, settings_dock)
        self.viewMenu.addAction(settings_dock.toggleViewAction())
        settings_dock.hide()

    def change_current_engine(self):
        self.current_engine = self.tabWidget.currentWidget().objectName()

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent) -> None:
        self.tab1.close()
        CONF = ConfigParser()
        CONF.read(CONFIG_FILE, encoding='utf-8')
        CONF.set("defult", "save_dir", str(self.save_dir))
        CONF.set("defult", "current_engine", str(self.current_engine))
        CONF.write(open(CONFIG_FILE, "w"))


if __name__ == '__main__':
    import sys
    from mainapplication import appctxt

    main_appctxt = appctxt
    mainWin = MainWindow()
    mainWin.show()
    exit_code = main_appctxt.app.exec_()
    sys.exit(exit_code)
