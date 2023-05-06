
import sys
import cgitb

from qtpy.QtCore import QLockFile
from qtpy.QtWidgets import QMessageBox

from mainapplication import appctxt
from application import MainWindow


if __name__ == '__main__':

    sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    try:
        main_appctxt = appctxt
        lock_file = QLockFile("dundi.lock")
        if lock_file.tryLock():
            mainWin = MainWindow()
            mainWin.show()
            exit_code = main_appctxt.app.exec_()
            sys.exit(exit_code)

        else:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Warning)
            error_message.setWindowTitle("Error")
            error_message.setText("The application is already running!")
            error_message.setStandardButtons(QMessageBox.Ok)
            error_message.exec()
    finally:
        lock_file.unlock()
