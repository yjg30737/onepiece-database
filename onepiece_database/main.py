import json
import os
import sqlite3
from collections import defaultdict
from typing import Union

import pandas as pd
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton, \
    QWidget, QVBoxLayout, QDialog, QFileDialog, QSplitter
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QPersistentModelIndex
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView, QTableView, QStyledItemDelegate

from logWidget import LogDialog


class SqlTableModel(QSqlTableModel):
    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


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
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__column_names = []
        self.__tableName = "onepiece"
        # for saving data frame to export
        self.__df = ''

    def __initUi(self):
        self.setWindowTitle('One Piece Database')

        crawlBtn = QPushButton('Get Characters Info')
        crawlBtn.clicked.connect(self.__getData)

        self.__exportBtn = QPushButton('Export')
        self.__exportBtn.clicked.connect(self.__export)

        # before data filled in the tableview
        self.__exportBtn.setEnabled(False)

        self.__totalLbl = QLabel('Total: 0')

        lay = QHBoxLayout()
        lay.addWidget(QLabel('Table'))
        lay.addWidget(self.__totalLbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(self.__exportBtn)
        lay.addWidget(crawlBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        # init the proxy model
        self.__proxyModel = FilterProxyModel()

        self.__headerTableView = QTableView()

        # set up the view
        self.__dataTableView = QTableView()
        self.__dataTableView.setModel(self.__proxyModel)

        # set selection/resize policy
        self.__dataTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.__dataTableView.resizeColumnsToContents()
        self.__dataTableView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # set sorting enabled
        self.__dataTableView.setSortingEnabled(True)

        # hide vertical header
        self.__dataTableView.verticalHeader().hide()

        topWidget.setMaximumHeight(topWidget.sizeHint().height())

        bottomWidget = QSplitter()
        bottomWidget.addWidget(self.__headerTableView)
        bottomWidget.addWidget(self.__dataTableView)
        bottomWidget.setChildrenCollapsible(False)
        bottomWidget.setHandleWidth(0)
        bottomWidget.setSizes([250, 750])

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(bottomWidget)

        self.setLayout(lay)

    def __crawlData(self):
        logDialog = LogDialog()
        logDialog.setWindowTitle('Crawling...')
        os.chdir(os.path.dirname(__file__))
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
            self.__df = df

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

        # get columns' name and convert them into usual capitalized words
        conn = sqlite3.connect('data.sqlite')
        cur = conn.cursor()
        table_info_result = cur.execute(f'PRAGMA table_info([{self.__tableName}])').fetchall()
        table_info_df = pd.DataFrame(table_info_result, columns=['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'])

        # [1:] for not include index
        self.__column_names = [' '.join(map(lambda chunk: chunk.capitalize(), columns_name.split('_')))
                       for columns_name in [col['name']
                       for col in table_info_df.iloc]][1:]

        # set columns' name as horizontal header
        for i in range(len(self.__column_names)):
            self.__model.setHeaderData(i, Qt.Horizontal, self.__column_names[i])

        # remove index column which doesn't need to show
        self.__model.removeColumn(0)

        # set the table model as source model to make it enable to feature sort and filter function
        self.__proxyModel.setSourceModel(self.__model)

        # get official english name to set as vertical header
        statistics_official_english_names = \
            cur.execute(f'SELECT statistics_romanized_name FROM {self.__tableName}').fetchall()

        # sort the table in ascending alphabetical order of statistics_romanized_name field by default
        # this is basically Qt way to execute the query with clause below
        # "ORDER BY statistics_romanized_name ASC"
        self.__dataTableView.sortByColumn(self.__model.fieldIndex('statistics_romanized_name'), Qt.AscendingOrder)

        vertical_header = list(map(lambda x: x[0], statistics_official_english_names))

        # set columns' name as vertical header (which doesn't work for some stupid reasons)
        for i in range(len(vertical_header)):
            self.__model.setHeaderData(i, Qt.Vertical, vertical_header[i])

        # align to center
        delegate = AlignDelegate()
        for i in range(self.__model.columnCount()):
            self.__dataTableView.setItemDelegateForColumn(i, delegate)

        # select and fetch every row
        self.__model.select()
        while self.__model.canFetchMore():
            self.__model.fetchMore()

        self.__totalLbl.setText(f'Total: {self.__model.rowCount()}')

        # set current index as first record
        self.__dataTableView.setCurrentIndex(self.__dataTableView.model().index(0, 0))

        # resize columns
        self.__dataTableView.resizeColumnsToContents()

        # after data filled in the tableview
        self.__exportBtn.setEnabled(True)

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

    def __export(self):
        filename = QFileDialog.getSaveFileName(self, 'Save', os.path.expanduser('~'), 'Excel File (*.xlsx);;CSV file (*.csv)')
        if filename[0]:
            filename = filename[0]
            file_extension = os.path.splitext(filename)[-1]
            df_copy = self.__df.copy()
            if file_extension == '.xlsx':
                df_copy.columns = self.__column_names
                df_copy.to_excel(filename, index=False, header=True)
            elif file_extension == '.csv':
                df_copy.to_csv(filename, index=False, encoding='utf-16')
            # todo database (sqlite, mysql)
            os.startfile(os.path.dirname(filename))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
