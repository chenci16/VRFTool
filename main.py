import sys

from PyQt5.QtWidgets import QApplication

import main_window
from utils.log import log

if __name__ == '__main__':
    try:
        myapp = QApplication(sys.argv)
        mainUI = main_window.Ui_MainWindow()
        mainUI.setupUi()
        mainUI.show()
        sys.exit(myapp.exec_())
    except Exception as e:
        log.error(e)
