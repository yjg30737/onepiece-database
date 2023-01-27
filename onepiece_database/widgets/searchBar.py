import os
import posixpath

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget, QLineEdit, \
    QGridLayout


class InstantSearchBar(QWidget):
    searched = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # search bar label
        self.__label = QLabel()

        self.__initUi()

    def __initUi(self):
        self.__searchLineEdit = QLineEdit()
        self.__searchIconLbl = QLabel()
        ps = QApplication.font().pointSize()
        self.__searchIconLbl.setFixedSize(ps, ps)

        self.__searchBar = QWidget()
        self.__searchBar.setObjectName('searchBar')

        lay = QHBoxLayout()
        lay.addWidget(self.__searchIconLbl)
        lay.addWidget(self.__searchLineEdit)
        self.__searchBar.setLayout(lay)
        lay.setContentsMargins(ps // 2, 0, 0, 0)
        lay.setSpacing(0)

        self.__searchLineEdit.setFocus()
        self.__searchLineEdit.textChanged.connect(self.__searched)

        self.setAutoFillBackground(True)

        lay = QGridLayout()
        lay.addWidget(self.__searchBar)
        lay.setContentsMargins(0, 0, 0, 0)

        self.__setStyle()

        self.setLayout(lay)

    # ex) searchBar.setLabel(True, 'Search Text')
    def setLabel(self, visibility: bool = True, text=None):
        if text:
            self.__label.setText(text)
        self.__label.setVisible(visibility)

    def __setStyle(self):
        cur_dirname = os.path.dirname(__file__)
        cur_filename = os.path.join(cur_dirname, '../ico/search.svg').replace(os.path.sep, posixpath.sep)
        self.__searchIconLbl.setPixmap(QPixmap(cur_filename))
        self.__searchIconLbl.setScaledContents(True)

        self.__searchLineEdit.setStyleSheet('''
            QLineEdit
            {
                background: transparent;
                color: #333333;
                border: none;
            }
        ''')
        self.__searchBar.setStyleSheet('QWidget#searchBar { border: 1px solid gray; }')
        # self.setStyleSheet('QWidget { padding: 5px; }')

    def __searched(self, text):
        self.searched.emit(text)

    def setSearchIcon(self, icon_filename: str):
        self.__searchIconLbl.setIcon(icon_filename)

    def setPlaceHolder(self, text: str):
        self.__searchLineEdit.setPlaceholderText(text)

    def getSearchBar(self):
        return self.__searchLineEdit

    def getSearchLabel(self):
        return self.__searchIconLbl

    def showEvent(self, e):
        self.__searchLineEdit.setFocus()