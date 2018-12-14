import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QProgressBar
from PIL import Image
import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QBasicTimer
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1174, 672)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(250, 120, 400, 400))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.set = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.set.setContentsMargins(0, 0, 0, 0)
        self.set.setObjectName("set")

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(250, 80, 200, 25)

        self.timer = QBasicTimer()
        self.step = 0

        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(280, 30, 131, 31))
        self.time.setObjectName("time")

        self.loa = QtWidgets.QPushButton(self.centralwidget)
        self.loa.setGeometry(QtCore.QRect(980, 90, 131, 31))
        self.loa.setObjectName("loa")

        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(580, 30, 131, 41))
        self.next.setObjectName("next")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1174, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.time.setText(_translate("MainWindow", "время на исходе"))
        self.loa.setText(_translate("MainWindow", "загрузить свое фото"))
        self.next.setText(_translate("MainWindow", "следующий уровень"))

class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.image = QScrollArea(self)
        self.image.setGeometry(0, 0, 200, 200)
        self.image.setWidgetResizable(True)

        self.loa.clicked.connect(self.dialog)
        self.m = []

    def dialog(self):
        photo, ok = QInputDialog.getText(
            self, 'своя игра', 'Ведите путь до фотографии'
        )
        if ok:
            rang, sok = QInputDialog.getText(
                self, 'сложность', 'укажите желаемые размеры игры\nнапример: 4X4, X - латиница'
            )
            if sok:
                self.make_fotos(photo, rang)

    def timerEvent(self, e):

        if self.step >= 6000:
            self.timer.stop()
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def make_fotos(self, foto, rang):
        self.timer.start(6000, self)
        lbl = QLabel(self)
        pixmap = QPixmap(foto)
        pixmap = pixmap.scaledToWidth(200)
        lbl.setPixmap(pixmap)
        self.image.setWidget(lbl)

        rang = rang.split('X')
        x1, y1 = int(rang[0]), int(rang[1])

        basewidth = 600
        img = Image.open(foto)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)

        image = np.asarray(img)
        x = len(image) // x1
        y = len(image[0]) // y1
        self.m = []
        for i in range(x1):
            for j in range(y1):
                if i != x1 - 1 or j != y1 - 1:
                    name = 'image{}{}.bmp'.format(i + 1, j + 1)
                    Image.fromarray(np.uint8(image[x * i:x * (i + 1), y * j:y * (j + 1)])).save(name)
                    self.m.append(name)
        self.rand(x, y, x1, y1)

    def rand(self, x, y, x1, y1):
        new = []
        while len(self.m):
            t = random.randint(0, len(self.m) - 1)
            new.append(self.m.pop(t))

        self.gridLayoutWidget.setGeometry(QtCore.QRect(250, 120, y * y1, x * x1))
        for i in range(x1):
            for j in range(y1):
                if i != x1 - 1 or j != y1 - 1:
                    poz = (i * y1) + j
                    self.but = QPushButton(self)
                    self.but.setIcon(QIcon(new[poz]))
                    self.but.setIconSize(QSize(y, x))
                    self.but.setFixedSize(y, x)
                    self.but.cord = i, j, x1, y1
                    self.but.clicked.connect(self.chan)
                    self.set.addWidget(self.but, i, j)

    def chan(self):
        i, j, x1, y1 = self.sender().cord
        x, y = self.read(i, j, x1, y1)
        if x != -2 and y != -2:
            self.sender().cord = x, y, x1, y1
            self.set.addWidget(self.sender(), x, y)

    def read(self, i, j, x1, y1):
        if j - 1 > -1:
            if self.set.itemAtPosition(i, j - 1) is None:
                return i, j - 1
        if j + 1 < y1:
            if self.set.itemAtPosition(i, j + 1) is None:
                return i, j + 1
        if i - 1 > -1:
            if self.set.itemAtPosition(i - 1, j) is None:
                return i - 1, j
        if i + 1 < x1:
            if self.set.itemAtPosition(i + 1, j) is None:
                return i + 1, j
        return -2, -2

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
