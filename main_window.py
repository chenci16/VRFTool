import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils.config_tools import cf

running = False


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

    def setupUi(self):
        self.setObjectName("Main_Window")
        # 隐藏边框并始终在最顶层×
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置透明度
        self.setWindowOpacity(1)

        # 根据屏幕分辨率设置窗口大小和位置
        desktop = QApplication.desktop()
        width = int(desktop.width() / 4)
        height = int(desktop.height() / 2)
        location = (int(desktop.width() / 3), int(desktop.height() / 4))
        # 设置位置
        self.move(location[0], location[1])
        # 固定大小
        self.resize(width, height)

        widget = QWidget()

        self.mainLayout = QGridLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.formLayout = QGridLayout()
        self.formLayout.setAlignment(Qt.AlignTop)
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

        # 目录配置按钮
        self.selectInputLabel = QLabel()
        self.selectInputLabel.setObjectName("selectInputLabel")
        self.selectInputLabel.setText(cf.get("PATH", "input-path"))
        self.selectInputBtn = QPushButton(self, text="选择输入目录")
        self.selectInputBtn.clicked.connect(self.select_input_root)
        self.selectOutLabel = QLabel()
        self.selectOutLabel.setObjectName("selectOutLabel")
        self.selectOutLabel.setText(cf.get("PATH", "out-path"))
        self.selectOutBtn = QPushButton(self, text="选择输出目录")
        self.selectOutBtn.clicked.connect(self.select_out_root)

        self.pbar = QProgressBar(self)
        self.startBtn = QPushButton(self, text="开始")
        self.startBtn.clicked.connect(self.start_format)
        self.stopBtn = QPushButton(self, text="停止")
        self.stopBtn.clicked.connect(self.stop_format)

        self.tips = QLabel()
        self.tips.setObjectName("tips")
        self.tips.setText("如果程序卡死，可能是因为选择的目录下文件过多导致")

        self.formLayout.addWidget(self.selectInputLabel, 0, 0, 1, 3)
        self.formLayout.addWidget(self.selectInputBtn, 0, 4)
        self.formLayout.addWidget(self.selectOutLabel, 1, 0, 1, 3)
        self.formLayout.addWidget(self.selectOutBtn, 1, 4)
        self.formLayout.addWidget(self.pbar, 2, 0, 1, 2)
        self.formLayout.addWidget(self.startBtn, 2, 3)
        self.formLayout.addWidget(self.stopBtn, 2, 4)
        self.formLayout.addWidget(self.tips, 3, 0)

        self.mainLayout.addLayout(self.formLayout, 0, 0)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "VRFTool"))

    def select_input_root(self):
        # 当前配置的目录
        inputRoot = QFileDialog.getExistingDirectory(self, '选择输入目录', cf.get("PATH", "input-path"))
        self.selectInputLabel.setText(inputRoot)
        cf.set("PATH", "input-path", inputRoot)
        cf.write(open("conf/config.ini", "w"))

    def select_out_root(self):
        # 当前配置的目录
        outRoot = QFileDialog.getExistingDirectory(self, '选择输出目录', cf.get("PATH", "out-path"))
        self.selectOutLabel.setText(outRoot)
        cf.set("PATH", "out-path", outRoot)
        cf.write(open("conf/config.ini", "w"))

    def start_format(self):
        setRunning(True)
        self.startBtn.setEnabled(False)
        # 创建线程
        self.backend = WorkThread()
        # 连接信号
        self.backend.process.connect(self.process_change)
        self.backend.complete.connect(self.format_complete)
        # 开始线程
        self.backend.start()

    def stop_format(self):
        setRunning(False)
        self.startBtn.setEnabled(True)

    def process_change(self, value):
        self.pbar.setValue(value)

    def format_complete(self, value):
        if value:
            setRunning(False)
            self.startBtn.setEnabled(True)

    def exit(self):
        exit()


def getRunning():
    global running
    return running


def setRunning(b):
    global running
    running = b


# 全局任务
class WorkThread(QThread):
    # 通过类成员对象定义信号
    process = pyqtSignal(int)
    complete = pyqtSignal(bool)

    # 初始化线程
    def __int__(self):
        super(WorkThread, self).__init__()

    # 线程运行函数
    def run(self):
        # 总进度
        input_path = cf.get("PATH", "input-path")
        base_name = os.path.basename(input_path)
        out_path = cf.get("PATH", "out-path") + "\\" + base_name
        total = sum([1 for _, _, _ in os.walk(input_path)])
        completed = 0
        for filepath, dirnames, filenames in os.walk(input_path):
            # print(filepath.replace(input_path, out_path))
            os.system(".\Decompiler.exe -i " + filepath + " -o " + filepath.replace(input_path, out_path))
            completed = completed + 1
            self.process.emit(int(completed * 100 / total))
            if not getRunning():
                break
        self.complete.emit(True)
