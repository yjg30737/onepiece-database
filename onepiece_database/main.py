import json
import os
import sqlite3
from collections import defaultdict
from typing import Union

import pandas as pd
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton, \
    QWidget, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QPersistentModelIndex
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView, QTableView, QStyledItemDelegate

from logWidget import LogDialog

class SqlTableModel(QSqlTableModel):

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags:
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return super().flags(index)

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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__tableName = "onepiece"

        self.setWindowTitle('Database')

        btn = QPushButton('Get Characters Info')
        btn.clicked.connect(self.__getData)

        lay = QHBoxLayout()
        lay.addWidget(QLabel('Table'))
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(btn)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        # init the proxy model
        self.__proxyModel = FilterProxyModel()

        # set up the view
        self.__tableView = QTableView()
        self.__tableView.setModel(self.__proxyModel)

        # set selection/resize policy
        self.__tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.__tableView.resizeColumnsToContents()
        self.__tableView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # sort (ascending order by default)
        self.__tableView.setSortingEnabled(True)
        self.__tableView.sortByColumn(0, Qt.AscendingOrder)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(self.__tableView)

        self.setLayout(lay)

    def __crawlData(self):
        logDialog = LogDialog()
        logDialog.setWindowTitle('Crawling...')
        # check data.json exists
        os.chdir('./one-piece-character-data-scraper')
        if os.path.exists('data.json'):
            return QDialog.Accepted
        else:
            command = 'python -m scrapy crawl char_info -o data.json'
            logWidget = logDialog.getLogWidget()
            logWidget.setCommand(command)
            reply = logDialog.exec()
            return reply

    def __getDatabase(self):
        try:
            with open("data.json", 'r') as f:
                data = json.load(f)

            new_lst = []

            for i in range(len(data)):
                new_dict = defaultdict(dict)
                d = data[i]
                for name, info in d.items():
                    # self.__tableWidget.setItem(i, 0, QTableWidgetItem(name))
                    # print(f'Name: {name}')
                    for info_header, info_body in info.items():
                        # print(f'Header: ', info_header)
                        # print(f'Body: ', info_body)
                        for info_attr_k, info_attr_v in info_body.items():
                            new_dict[('_'.join(info_header.split()) + '_' + '_'.join(
                                info_attr_k.split())).lower()] = info_attr_v
                    new_lst.append(new_dict)

            # Create A DataFrame From the JSON Data
            df = pd.DataFrame(new_lst)

            conn = sqlite3.connect('data.sqlite')
            c = conn.cursor()

            df.to_sql('onepiece', conn)
            return True
        # if database already exists
        except ValueError as ve:
            return True
        except Exception as e:
            print(e)
            return False

    def __createConnection(self):
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("data.sqlite")
        if not con.open():
            QMessageBox.critical(
                None,
                "QTableView Example - Error!",
                "Database Error: %s" % con.lastError().databaseText(),
            )
            return False
        return True

    def __showDatabase(self):
        self.__model = SqlTableModel(self)
        self.__model.setTable(self.__tableName)
        self.__model.select()

        # set the table model as source model to make it enable to feature sort and filter function
        self.__proxyModel.setSourceModel(self.__model)

        # align to center
        delegate = AlignDelegate()
        for i in range(self.__model.columnCount()):
            self.__tableView.setItemDelegateForColumn(i, delegate)

        # set current index as first record
        self.__tableView.setCurrentIndex(self.__tableView.model().index(0, 0))

    def __getData(self):
        reply = self.__crawlData()
        # finish to crawl successfully
        if reply == QDialog.Accepted:
            get_database_res = self.__getDatabase()
            if get_database_res:
                create_connection_res = self.__createConnection()
                if create_connection_res:
                    self.__showDatabase()
            else:
                pass
        # fail to crawl
        else:
            pass



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
