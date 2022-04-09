from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDate
import datetime
from datetime import datetime


class Client:
    def __init__(self, interface, db):
        self.interface = interface
        self.database = db
        self.rows = 15

    def show(self):
        self.table = self.interface.get_clienti_table()
        self.table.setRowCount(self.rows)

        self.nume, self.nr_tel, self.nr_card, self.gen, self.date, self.insert_btn = self.interface.get_clienti_insert()
        self.nume2, self.nr_tel2, self.nr_card2, self.gen2, self.id2, self.date2, self.update_btn, self.select_btn = self.interface.get_clienti_update()
        self.nume3, self.date3, self.nr_tel3, self.gen3, self.id3, self.nr_card3, self.delete_btn, self.delete_card_btn, self.select_btn1 = self.interface.get_clienti_delete()
        self.add_table()

        try:
            self.rows = self.table.rowCount()
        except Exception as err:
            print(err)

    def selectare0(self):
        self.items = []
        selected = self.table.selectedItems()
        if selected:
            for item in selected:
                self.items.append(item.data(0))

        if len(self.items):
            data = datetime.strptime(self.items[2][0:10], "%Y-%m-%d")
            self.d = QDate(int(data.year), int(data.month), int(data.day))
            self.nume2.setText(self.items[0])
            self.nr_tel2.setText(self.items[3])
            self.nr_card2.setText(self.items[4])
            self.gen2.setText(self.items[5])
            self.date2.setDate(self.d)
            self.id2.setCurrentText(self.items[1])

    def selectare1(self):
        self.items = []
        selected = self.table.selectedItems()
        if selected:
            for item in selected:
                self.items.append(item.data(0))
        if len(self.items):
            self.nume3.setText(self.items[0])
            self.nr_tel3.setText(self.items[3])
            self.nr_card3.setText(self.items[4])
            self.gen3.setText(self.items[5])
            self.date3.setText(self.items[2][0:10])
            self.id3.setText(self.items[1])

    def add_table(self):
        query = "select id_client from clienti"
        self.rez = ""
        try:
            self.rez = self.database.execute_query(query)
        except Exception as err:
            print(err)
        list_id = []
        for id in self.rez:
            list_id.append(str(id[0]))
        self.id2.clear()
        self.id2.addItems(list_id)

        query = "select nume_client,id_client,nvl(data_nasterii,null),nvl(nr_telefon,null),nvl(nr_card,null),nvl(gen,null) from clienti, date_card where id_client=clienti_id_client(+)"
        self.rez = ""
        try:
            self.rez = self.database.execute_query(query)
        except Exception as err:
            print(err)

        table_data = []
        for tip in self.rez:
            table_data.append(list(tip))

        row = 0
        for r in table_data:
            col = 0
            for item in r:
                cell = QtWidgets.QTableWidgetItem(str(item))
                cell.setBackground(QtGui.QColor(255,255,255))
                self.table.setItem(row, col, cell)
                col += 1
            row += 1
        self.table.setRowCount(row)

    def insert(self):
        self.name = self.nume.text()
        self.numar_telefon = self.nr_tel.text()
        self.numar_card = self.nr_card.text()
        self.gender = self.gen.text()
        self.data = self.date.text()[0:10]

        data_add = datetime.strptime(self.data, '%d-%m-%Y').strftime('%d-%b-%Y').upper()

        try:
            query = "insert into clienti(nume_client) values('{}')".format(self.name)
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
        if len(self.numar_card):
            query = "insert into date_card values ('{}','{}','{}',clienti_id_client_seq.currval,'{}')".format(
                data_add, self.numar_telefon, self.gender, self.numar_card)
        ok = 1
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
            ok = 0

        if ok:
            self.rows += 1
            self.table.setRowCount(self.rows)
        self.add_table()

    def update(self):
        self.name2 = self.nume2.text()
        self.numar_telefon2 = self.nr_tel2.text()
        self.numar_card2 = self.nr_card2.text()
        self.gender2 = self.gen2.text()
        self.id_c2 = self.id2.currentText()
        self.data2 = self.date2.text()[0:10]

        data_add = datetime.datetime.strptime(self.data, '%d-%m-%Y').strftime('%d-%b-%Y').upper()

        try:
            query = "update clienti set nume_client='{}' where id_client={}".format(self.name2, self.items[1])
            print(query)
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)

        try:
            if self.data2 is not self.items[2] or self.numar_telefon2 is not self.items[3] or self.numar_card2 is not \
                    self.items[4] or self.gender2 is not self.items[5]:
                query = "update date_card set data_nasterii='{}',nr_telefon='{}',nr_card={},gen='{}' where clienti_id_client={}".format(
                    data_add, self.numar_telefon2, self.numar_card2, self.gender2, self.items[1])
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
        self.add_table()

    def delete_client(self):
        try:
            query = "delete clienti where id_client={}".format(self.items[1])
        except Exception as err:
            print(err)
        ok = 1
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
            ok = 0
        if ok:
            self.rows -= 1
            self.table.setRowCount(self.rows)
        self.add_table()

    def delete_card(self):
        try:
            query = "delete date_card where clienti_id_client={}".format(self.items[1])
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
        self.add_table()
