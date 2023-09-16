import random

import PySide6
import requests
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QIcon
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
        self.name.setMaximumWidth(350)

        self.version = QLabel("Version: " + gmod.version)
        self.version.setMaximumWidth(350)

        self.imageLabel = QLabel()

        self.imageLabel.setMinimumHeight(80)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.version)
        self.layout.addWidget(self.imageLabel)


        style = "QPushButton {border: 2px solid rgb(52, 59, 72);border-radius: 5px;	background-color: rgb(52, 59, 72);}QPushButton:hover {background-color: rgb(57, 65, 80);border: 2px solid rgb(61, 70, 86);}QPushButton:pressed {	background-color: rgb(35, 40, 49);border: 2px solid rgb(43, 50, 61);}"

        if gmod.file != "":
            self.downloadButton = QPushButton("Download")
            self.downloadButton.setMaximumWidth(100)
            self.downloadButton.setStyleSheet(style)
            self.downloadButton.clicked.connect(lambda: self.save(self.downloadButton))

            self.icon1 = QIcon()
            self.icon1.addFile(u":/icons/icons/download.png", QSize(), QIcon.Normal, QIcon.Off)
            self.downloadButton.setIcon(self.icon1)

            self.layout_split.addWidget(self.downloadButton)

        if gmod.content != "":
            self.contentButton = QPushButton("Content")
            self.contentButton.setMaximumWidth(100)
            self.contentButton.setStyleSheet(style)

            self.icon2 = QIcon()
            self.icon2.addFile(u":/icons/icons/box.png", QSize(), QIcon.Normal, QIcon.Off)
            self.contentButton.setIcon(self.icon2)

            self.contentButton.clicked.connect(lambda: self.open_url(gmod.content))
            self.layout_split.addWidget(self.contentButton)

        if gmod.store != "":
            self.gmodStoreButton = QPushButton("GmodStore")
            self.gmodStoreButton.setMaximumWidth(100)
            self.gmodStoreButton.setStyleSheet(style)
            self.icon3 = QIcon()
            self.icon3.addFile(u":/icons/icons/shop.png", QSize(), QIcon.Normal, QIcon.Off)
            self.gmodStoreButton.setIcon(self.icon3)
            self.gmodStoreButton.clicked.connect(lambda: self.open_url(gmod.store))
            self.layout_split.addWidget(self.gmodStoreButton)


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
        self.pixmap = self.pixmap.scaledToWidth(350)
        self.imageLabel.setPixmap(self.pixmap)


