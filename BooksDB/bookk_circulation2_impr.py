from PySide2 import QtWidgets, QtGui, QtCore
import pyodbc

from authorization_form import Ui_Form as Authorization_Form
from books_circulation_form import Ui_Form


class Authorization(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Authorization_Form()
        self.ui.setupUi(self)

        self.initAuthorization()
        self.initWindows_circ()

        self.initDB_auth()

    def initAuthorization(self):
        self.resize(500, 600)
        self.setWindowTitle("Авторизация")


        self.ui.pushButton_Enter.clicked.connect(self.open_child_window_circ)


    def initDB_auth(self):
        server = 'tcp:vpngw.avalon.ru'
        database = 'library'
        username = 'tsqllogin'
        password = 'Pa$$w0rd'

        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        self.cursor = self.conn.cursor()

        # self.cursor.execute("SELECT MM.lastname, MM.firstname, MM.member_no FROM Members.member AS MM")

    def initWindows_circ(self):
        self.child_window_circ = Circulation_Form()
        self.child_window_circ.send_data.connect(lambda x: print(f"Main {x}"))

    def open_child_window_circ(self):
        self.child_window_circ.select_data = self.get_data_from_db()

        if self.child_window_circ.select_data:
            return self.child_window_circ.show()
        else:
            return QtWidgets.QMessageBox.warning(self, "Предупреждение", "Такой читатель не зарегистрирован",
                                                  QtWidgets.QMessageBox.Ok)

    def get_data_from_db(self):
        self.cursor.execute(f"SELECT MM.lastname, MM.firstname, MM.member_no "
                            f"FROM Members.member AS MM "
                            f"WHERE MM.lastname LIKE '%{self.ui.lineEdit_Surname.text()}%' "
                            f"AND MM.firstname LIKE '{self.ui.lineEdit_Name.text()}%'"
                            f"AND MM.member_no LIKE '{self.ui.lineEdit_member_number.text()}%'")

        return self.cursor.fetchall()


class Circulation_Form(QtWidgets.QWidget):
    send_data = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initUi()
        self.initDB()
        self.initWindows()

    def initUi(self):
        self.resize(500, 600)
        self.setWindowTitle("Поиск книги")

        self.ui.comboBox.addItems(["ARABIC", "CHINESE", "ENGLISH", "FRENCH", "GERMAN", "JAPANESE", "KOREAN", "LATIN", "PORTUGES", "SPANISH"])
        self.ui.comboBox.setPlaceholderText("Выберите язык")
        self.ui.comboBox.setEditable(True)
        self.ui.comboBox.currentIndexChanged.connect(
            lambda: print(f"Установлено значение {self.ui.comboBox.currentText()}"))

        self.ui.pushButton.clicked.connect(self.open_child_window)
        # self.ui.lineEdit.editingFinished.connect(self.selectAuthor)
        # self.ui.lineEdit_2.editingFinished.connect(self.selectTitle)

    def initDB(self):
        server = 'tcp:vpngw.avalon.ru'
        database = 'library'
        username = 'tsqllogin'
        password = 'Pa$$w0rd'

        self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        self.cursor = self.conn.cursor()

    def initWindows(self):
        self.child_window = MyFirstWindow()

    def open_child_window(self):
        self.child_window.select_data = self.get_data_from_db()
        self.child_window.show()

    def get_data_from_db(self):

        self.cursor.execute(f"SELECT BT.title, BT.author "
                            f"FROM Books.title AS BT "
                            f"WHERE BT.author LIKE '%{self.ui.lineEdit.text()}%' AND BT.title LIKE '{self.ui.lineEdit_2.text()}%'")

        return self.cursor.fetchall()
        # print(self.cursor.fetchone())
        # self.cursor.execute(f"SELECT BT.author FROM Books.title AS BT WHERE BT.title LIKE '{self.ui.lineEdit_2.text()}%'")
        # print(self.cursor.fetchone())



class MyFirstWindow(QtWidgets.QWidget):
    send_data = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.select_data = None

        self.initUi()

        self.initDB()

        # self.initTableViewModel()

    def initUi(self):
        self.resize(1000, 600)

        self.tableView = QtWidgets.QTableView()

        l = QtWidgets.QVBoxLayout()

        l.addWidget(self.tableView)

        self.setLayout(l)

    def showEvent(self, event:QtGui.QShowEvent) -> None:

        if self.select_data is None:
            return print(f"Данные в базе данных отсутствуют")

        sim = QtGui.QStandardItemModel()

        for elem in self.select_data:
            item1 = QtGui.QStandardItem(str(elem[0]))
            item2 = QtGui.QStandardItem(str(elem[1]))
            # item3 = QtGui.QStandardItem(str(elem[2]))
            # item4 = QtGui.QStandardItem(str(elem[3]))
            sim.appendRow([item1, item2])

        sim.setHorizontalHeaderLabels(["title", "author"])

        self.tableView.setModel(sim)

        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.tableView.selectionModel().currentChanged.connect(self.cellChanged)

        return super(MyFirstWindow, self).showEvent(event)


    def initDB(self):
        server = 'tcp:vpngw.avalon.ru'
        database = 'library'
        username = 'tsqllogin'
        password = 'Pa$$w0rd'

        self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        self.cursor = self.conn.cursor()

    def cellChanged(self, cell):
        print(cell.row())
        print(cell.column())
        print(cell.data(0))



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myWindow1 = Authorization()
    myWindow1.show()

    # myWindow = MyFirstWindow()
    # myWindow.show()

    app.exec_()


