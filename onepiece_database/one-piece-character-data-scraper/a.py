from collections import defaultdict

import pandas as pd
import json
import sqlite3

from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QTableWidget, QVBoxLayout, QWidget, QApplication, \
    QTableWidgetItem, QStyledItemDelegate


# for search feature
class FilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.__searchedText = ''

    @property
    def searchedText(self):
        return self.__searchedText

    @searchedText.setter
    def searchedText(self, value):
        self.__searchedText = value
        self.invalidateFilter()


# for align text in every cell to center
class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        btn = QPushButton('Click')
        btn.clicked.connect(self.__load)

        self.__tableWidget = QTableWidget()

        lay = QVBoxLayout()
        lay.addWidget(btn)
        lay.addWidget(self.__tableWidget)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def __load(self):
        with open("data.json", 'r') as f:
            data = json.load(f)

        self.__tableWidget.setRowCount(len(data))
        self.__tableWidget.setColumnCount(1)

        new_lst = []

        for i in range(len(data)):
            new_dict = defaultdict(dict)
            d = data[i]
            for name, info in d.items():
                self.__tableWidget.setItem(i, 0, QTableWidgetItem(name))
                # print(f'Name: {name}')
                for info_header, info_body in info.items():
                    # print(f'Header: ', info_header)
                    # print(f'Body: ', info_body)
                    for info_attr_k, info_attr_v in info_body.items():
                        new_dict[('_'.join(info_header.split())+'_'+'_'.join(info_attr_k.split())).lower()] = info_attr_v
                new_lst.append(new_dict)
            print('')

        for _ in new_lst:
            print(_)

        # Create A DataFrame From the JSON Data
        df = pd.DataFrame(new_lst)

        conn = sqlite3.connect('data.db')

        df.to_sql('onepiece', conn)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

