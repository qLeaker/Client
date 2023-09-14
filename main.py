import json
import random
import sys
import urllib
from threading import Thread
from time import sleep

import PySide6
import orjson
from PySide6.QtCore import QObject, Slot, QThread, Signal
from PySide6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QListView, QWidget, QHBoxLayout, QLabel, QGridLayout, QVBoxLayout

import form
from classes.gmodObject import Gmod
from widgets.gmodItem import GmodItem
import requests

class gmodLayout(QWidget):
    def __init__(self, parent=None):
        super(gmodLayout, self).__init__(parent)
        self.layout_split = QHBoxLayout()
        self.setLayout(self.layout_split)

class GmodWorker(QObject):
    progress = Signal(Gmod, int)
    init = Signal(list)
    finish = Signal(int)

    downloadThread = Signal(form.Ui_MainWindow)
    def runThread(self, item, ui, number):
        try:
            jsonData = orjson.loads(requests.get(item).text)
            gmod = Gmod(**jsonData)
            gmod.image = urllib.request.urlopen(gmod.image).read()
            self.progress.emit(gmod, number)
        except:
            print("Ошибка загрузки: " + item)

    @Slot(Gmod)
    def run(self, ui: form.Ui_MainWindow):
        global gmodList
        list = orjson.loads(requests.get("https://github.com/qLeaker/Cloud/raw/main/gmod/list.json").text)
        self.init.emit(list["lists"])
        print("[Garry's mod] список аддонов загружен")
        threadNumber = 0
        for item in list["lists"]:
            new_thread = Thread(target=self.runThread, args=(item, ui, threadNumber))
            threadNumber = threadNumber + 1
            new_thread.start()
            sleep(0.21) # 12




class MainWindow(QMainWindow):
    gmod_requested = Signal(form.Ui_MainWindow)
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ll = gmodLayout()
        self.ui = form.Ui_MainWindow()
        self.ui.setupUi(self)
        self.children = []
        self.gmodList = []

        self.ui.listWidget.setSelectionMode(PySide6.QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.ui.gmodSearchButton.clicked.connect(lambda: self.search())

        # Threading
        self.gmodWorker = GmodWorker()
        self.gmod_thread = QThread()

        self.gmodWorker.progress.connect(self.update_progress_gmod)
        self.gmodWorker.init.connect(self.gmodInit)

        self.gmod_requested.connect(self.gmodWorker.run)

        # move worker to the worker thread
        self.gmodWorker.moveToThread(self.gmod_thread)

        # start the thread
        self.gmod_thread.daemon = True
        self.gmod_thread.start()
        self.gmod_requested.emit(self.ui)


    def search(self):
        self.ui.listWidget.clear()
        self.children = []
        self.ll = gmodLayout()
        for index in self.rows:
            gmod = self.rows.get(index)
            if self.ui.lineEdit.text() == "":
                item = QListWidgetItem()
                gmodItem = GmodItem(gmod)
                item.setSizeHint(gmodItem.minimumSizeHint())
                gmodItem.updateImage(gmod.image)
                self.ui.listWidget.insertItem(index, item)
                self.ui.listWidget.setItemWidget(item, gmodItem)
                pass
            else:
                if gmod.name.lower().__contains__(self.ui.lineEdit.text().lower()):
                    item = QListWidgetItem()
                    gmodItem = GmodItem(gmod)
                    item.setSizeHint(gmodItem.minimumSizeHint())
                    gmodItem.updateImage(gmod.image)
                    self.ui.listWidget.insertItem(index, item)
                    self.ui.listWidget.setItemWidget(item, gmodItem)




    rows = dict()
    def gmodInit(self, list):
        self.ui.tabWidget.setTabText(1, "Garry's mod [" + str(len(list)) + "]")
    def addToGmodList(self, gmod, row):
        item = QListWidgetItem()
        gmodItem = GmodItem(gmod)
        item.setSizeHint(gmodItem.minimumSizeHint())
        gmodItem.updateImage(gmod.image)
        self.ui.listWidget.insertItem(row, item)
        self.ui.listWidget.setItemWidget(item, gmodItem)
    def update_progress_gmod(self, gmod: Gmod, row):
        self.rows.update({
            row: gmod
        })
        if self.ui.lineEdit.text() == "":
            self.addToGmodList(gmod, row)
        else:
            if gmod.name.__contains__(self.ui.lineEdit.text()):
                self.addToGmodList(gmod, row)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()



    # window.updateGmod()
    appstatus = app.exec()
    sys.exit(appstatus)