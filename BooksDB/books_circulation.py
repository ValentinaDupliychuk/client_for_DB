from PySide2 import QtWidgets, QtGui, QtCore
import pyodbc
from PySide2.QtCore import QSortFilterProxyModel, QRegExp, Qt

from authorization_form import Ui_Form as Authorization_Form
from books_circulation_form import Ui_Form


class Circulation_Form(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.resize(300, 600)
        self.setWindowTitle("Поиск книги")

        self.ui.comboBox.addItems(["ARABIC", "CHINESE", "ENGLISH", "FRENCH", "GERMAN", "JAPANESE", "KOREAN", "LATIN", "PORTUGES", "SPANISH"])
        self.ui.comboBox.setPlaceholderText("Выберите язык")

        self.ui.pushButton.clicked.connect(self.initTableViewModel)

        self.initUi()

        self.initTableViewModel()

        # self.ui1 = Authorization_Form()
        # self.ui1.setupUi(self)

        # self.initAuthorizationForm()

        self.initDB()

        # self.initTableViewModel()
        #
        # self.initListViewModel()

    def initUi(self):
        self.tableView = QtWidgets.QTableView()

        l = QtWidgets.QVBoxLayout()
        l.addWidget(self.tableView)

        self.setLayout(l)

    def initTableViewModel(self):
        sim = QtGui.QStandardItemModel()

        self.cursor.execute("SELECT BT.author, BT.title FROM Books.title AS BT")
        lst = self.cursor.fetchall()

        for elem in lst:
            item1 = QtGui.QStandardItem(str(elem[0]))
            item2 = QtGui.QStandardItem(str(elem[1]))
            sim.appendRow([item1, item2])

        sim.setHorizontalHeaderLabels(["Автор", "Заглавие"])

        self.tableView.setModel(sim)

        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # self.tableView.selectionModel().currentChanged.connect(self.cellChanged)




    def initAuthorizationForm(self):
        pass


    def initDB(self):
        server = 'tcp:vpngw.avalon.ru'
        database = 'library'
        username = 'tsqllogin'
        password = 'Pa$$w0rd'

        self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        self.cursor = self.conn.cursor()



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myWindow = Circulation_Form()
    myWindow.show()

    app.exec_()


