import os

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton, \
    QWidget, QTableWidget, QVBoxLayout, QTextBrowser, QDialog

from logWidget import LogDialog

from sqlalchemy import create_engine

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Database')

        btn = QPushButton('Get Characters Info')
        btn.clicked.connect(self.__crawl)

        lay = QHBoxLayout()
        lay.addWidget(QLabel('Table'))
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(btn)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        self.__logBrowser = QTextBrowser()
        self.__logBrowser.hide()

        tableWidget = QTableWidget()
        # tableView.setItemDelegate()

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(self.__logBrowser)
        lay.addWidget(tableWidget)

        self.setLayout(lay)

    def __crawl(self):
        logDialog = LogDialog()
        logDialog.setWindowTitle('Crawling...')
        os.chdir('./one-piece-character-data-scraper')
        command = 'python -m scrapy crawl char_info -o data.json'
        logWidget = logDialog.getLogWidget()
        logWidget.setCommand(command)
        reply = logDialog.exec()
        if reply == QDialog.Accepted:
            with open('data.json', 'r') as f:
                content = f.read()
        else:
            pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
