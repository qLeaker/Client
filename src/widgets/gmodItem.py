import random

import PySide6
import requests
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QRect
from PySide6.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout)
import urllib.request
import webbrowser

from orjson import orjson

from classes.gmodObject import Gmod


class GmodItem(QWidget):
    def __init__(self, gmod: Gmod, parent=None):
        super(GmodItem, self).__init__(parent)
        self.gmod = gmod

        self.layout_split = QHBoxLayout()
        self.layout = QFormLayout(self)
        self.layout.setObjectName(gmod.name)
        self.image = QtGui.QImage()
        self.name = QLabel(gmod.name)
        self.name.setMaximumWidth(400)

        self.version = QLabel("Version: " + gmod.version)
        self.version.setMaximumWidth(400)

        self.imageLabel = QLabel()

        self.imageLabel.setMinimumHeight(80)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.version)
        self.layout.addWidget(self.imageLabel)


        if gmod.file != "":
            self.downloadButton = QPushButton("Download")
            self.downloadButton.setMaximumWidth(80)
            self.downloadButton.clicked.connect(lambda: self.save(self.downloadButton))
            self.layout_split.addWidget(self.downloadButton)

        if gmod.content != "":
            self.contentButton = QPushButton("Content")
            self.contentButton.setMaximumWidth(80)
            self.contentButton.clicked.connect(lambda: self.open_url(gmod.content))
            self.layout_split.addWidget(self.contentButton)

        if gmod.store != "":
            self.contentButton = QPushButton("GmodStore")
            self.contentButton.setMaximumWidth(80)
            self.contentButton.clicked.connect(lambda: self.open_url(gmod.store))
            self.layout_split.addWidget(self.contentButton)


        self.layout.setLayout(3, PySide6.QtWidgets.QFormLayout.ItemRole.FieldRole.FieldRole, self.layout_split)

        self.setLayout(self.layout)
    def open_url(self, url):
        webbrowser.open(url)
    def save(self, button):
        with open(self.name.text() + ".zip", "wb") as binary_file:
            # Write bytes to file
            list = orjson.loads(requests.get(self.gmod.file).text)
            data = list["file"]
            binary_file.write(bytes.fromhex(data))
        pass
    def updateImage(self, url: str):
        data = urllib.request.urlopen(url).read()
        self.image.loadFromData(data, "PNG")
        self.pixmap = QtGui.QPixmap(self.image)
        self.pixmap = self.pixmap.scaled(350, 550, QtCore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(self.pixmap)
    def updateImage(self, data: bytes):
        self.image.loadFromData(data, "PNG")
        self.pixmap = QtGui.QPixmap(self.image)
        self.pixmap = self.pixmap.scaled(350, 85, QtCore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(self.pixmap)


