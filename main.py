import threading

from Comenzi import Comanda
from Medicament import Medicament
from gui import Ui_MainWindow
from PyQt5 import QtWidgets
from database import database
import sys

from TipMedicament import Tip
from Furnizor import Furnizor
from Client import Client


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, db, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.database = db
        ui = Ui_MainWindow()
        ui.setupUi(self)

        self.tip = Tip(ui, database)
        self.furnizor = Furnizor(ui, database)
        self.clienti = Client(ui, database)
        self.medicament = Medicament(ui, database)
        self.comenzi=Comanda(ui,database)

        self.tip.show()
        self.furnizor.show()
        self.clienti.show()
        self.medicament.show()
        self.comenzi.show()


        self.tip.insert_btn.clicked.connect(self.tip.insert)
        self.tip.update_btn.clicked.connect(self.tip.update)
        self.tip.delete_btn.clicked.connect(self.tip.delete)
        self.tip.select_btn.clicked.connect(self.tip.selectare0)
        self.tip.select_btn1.clicked.connect(self.tip.selectare1)

        self.clienti.insert_btn.clicked.connect(self.clienti.insert)
        self.clienti.update_btn.clicked.connect(self.clienti.update)
        self.clienti.delete_btn.clicked.connect(self.clienti.delete_client)
        self.clienti.delete_card_btn.clicked.connect(self.clienti.delete_card)
        self.clienti.select_btn.clicked.connect(self.clienti.selectare0)
        self.clienti.select_btn1.clicked.connect(self.clienti.selectare1)

        self.furnizor.insert_btn.clicked.connect(self.furnizor.insert)
        self.furnizor.update_btn.clicked.connect(self.furnizor.update)
        self.furnizor.delete_btn.clicked.connect(self.furnizor.delete)
        self.furnizor.select_btn.clicked.connect(self.furnizor.selectare0)
        self.furnizor.select_btn1.clicked.connect(self.furnizor.selectare1)

        self.medicament.insert_btn.clicked.connect(self.medicament.insert)
        self.medicament.update_btn.clicked.connect(self.medicament.update)
        self.medicament.delete_btn.clicked.connect(self.medicament.delete)
        self.medicament.select_btn.clicked.connect(self.medicament.selectare0)
        self.medicament.select_btn1.clicked.connect(self.medicament.selectare1)

        self.comenzi.insert_btn_new.clicked.connect(self.comenzi.insert_new)
        self.comenzi.insert_btn_curr.clicked.connect(self.comenzi.insert_curr)
        self.comenzi.update_btn.clicked.connect(self.comenzi.update)
        self.comenzi.delete_btn.clicked.connect(self.comenzi.delete)
        self.comenzi.select_btn.clicked.connect(self.comenzi.selectare0)
        self.comenzi.select_btn1.clicked.connect(self.comenzi.selectare1)

        ui.btn_clienti.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_clienti))
        ui.btn_clienti.clicked.connect(self.clienti.show)
        ui.btn_furnizori.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_furnizori))
        ui.btn_furnizori.clicked.connect(self.furnizor.show)
        ui.btn_comenzi.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_comenzi))
        ui.btn_comenzi.clicked.connect(self.comenzi.show)
        ui.btn_tip_medicament.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_tip_medicament))
        ui.btn_tip_medicament.clicked.connect(self.tip.show)
        ui.btn_medicament.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_medicament))
        ui.btn_medicament.clicked.connect(self.medicament.show)
        ui.commit_btn.clicked.connect(self.database.con.commit)


if __name__ == "__main__":
    database = database()
    thread = threading.Thread(target=database.connect)
    thread.start()

    app = QtWidgets.QApplication(sys.argv)
    while database.success == 0:
        pass
    w = MainWindow(database)
    w.show()

    sys.exit(app.exec_())
