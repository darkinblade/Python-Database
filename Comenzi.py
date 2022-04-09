from PyQt5 import QtWidgets, QtGui
import datetime
from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor


class Comanda:
    def __init__(self, interface, db):
        self.interface = interface
        self.database = db
        self.rows = 50
        self.rows2 = 200

    def show(self):
        self.table1 = self.interface.get_comenzi_table1()
        self.table1.setRowCount(self.rows)

        self.table2 = self.interface.get_comenzi_table2()
        self.table2.setRowCount(self.rows2)

        self.id, self.id_c, self.can, self.data, self.insert_btn_new, self.insert_btn_curr = self.interface.get_comenzi_insert()
        self.id2, self.id_c2, self.can2, self.data2, self.update_btn, self.select_btn = self.interface.get_comenzi_update()
        self.data3, self.id3, self.id_c3, self.can3, self.nr_bon, self.delete_btn, self.select_btn1 = self.interface.get_comenzi_delete()

        self.add_table()

        try:
            self.rows = self.table1.rowCount()
        except Exception as err:
            print(err)

    def selectare0(self):
        self.items = []
        selected = self.table1.selectedItems()
        if selected:
            for item in selected:
                self.items.append(item.data(0))

        if len(self.items):
            data = datetime.strptime(self.items[0][0:10], "%Y-%m-%d")
            self.d = QDate(int(data.year), int(data.month), int(data.day))
            self.data2.setDate(self.d)
            self.id2.setCurrentText(self.items[1])
            self.id_c2.setCurrentText(self.items[2])
            self.can2.setCurrentText(self.items[4])

    def selectare1(self):
        self.items = []
        selected = self.table1.selectedItems()
        if selected:
            for item in selected:
                self.items.append(item.data(0))
        if len(self.items):
            self.data3.setText(self.items[0][0:10])
            self.id3.setText(self.items[1])
            self.id_c3.setText(self.items[2])
            self.can3.setText(self.items[4])
            self.nr_bon.setText(self.items[3])

    def add_table(self):
        query = "select id_medicament from medicament"
        self.rez = ""
        try:
            self.rez = self.database.execute_query(query)
        except Exception as err:
            print(err)
        list_id_t = []
        for id in self.rez:
            list_id_t.append(str(id[0]))
        self.id.clear()
        self.id.addItems(list_id_t)
        self.id2.clear()
        self.id2.addItems(list_id_t)

        query = "select id_client from clienti"
        self.rez = ""
        try:
            self.rez = self.database.execute_query(query)
        except Exception as err:
            print(err)
        list_id_f = []
        for id in self.rez:
            list_id_f.append(str(id[0]))
        self.id_c.clear()
        self.id_c.addItems(list_id_f)
        self.id_c2.clear()
        self.id_c2.addItems(list_id_f)

        query = "select * from bon_fiscal order by nr_bon"
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
                cell.setBackground(QtGui.QColor(255, 255, 255))
                self.table1.setItem(row, col, cell)
                col += 1
            row += 1
        self.table1.setRowCount(row)

        query = "with pret_bon as(select distinct nr_bon,id_medicament,pret,cantitate,pret*cantitate*case nvl(" \
                "nr_card,null) when null then 1 else 0.9 end pret_aux from medicament, bon_fiscal b,date_card d, " \
                "clienti where id_medicament=medicament_id_medicament and b.clienti_id_client=id_client) select " \
                "distinct nr_bon \"Nr Bon\",(select sum(pret_aux) from pret_bon p where p.nr_bon=pp.nr_bon) Pret_Bon " \
                "from pret_bon pp group by nr_bon,pret_aux order by nr_bon"
        self.rez = ""
        try:
            self.rez = self.database.execute_query(query)
        except Exception as err:
            print(err)

        table_data1 = []
        for tip1 in self.rez:
            table_data1.append(list(tip1))

        row = 0
        for r in table_data1:
            col = 0
            for item in r:
                cell = QtWidgets.QTableWidgetItem(str(item))
                cell.setBackground(QtGui.QColor(255, 255, 255))
                self.table2.setItem(row, col, cell)
                col += 1
            row += 1
        self.table2.setRowCount(row)

    def insert_new(self):
        self.id_n = self.id.currentText()
        self.id_c_n = self.id_c.currentText()
        self.can_n = self.can.currentText()
        self.data_n = self.data.text()[0:10]

        data_add = datetime.strptime(self.data_n, '%d-%m-%Y').strftime('%d-%b-%Y').upper()

        try:
            query = "INSERT INTO bon_fiscal(data_achizitie,medicament_id_medicament,clienti_id_client,cantitate) " \
                    "VALUES ('{}',{},{},{})".format(data_add, self.id_n, self.id_c_n, self.can_n)
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)

        try:
            query = "update medicament set stoc=stoc-{} where id_medicament={}".format(self.can_n, self.id_n)
        except Exception as err:
            print(err)

        ok = 1
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
            ok = 0

        if ok:
            self.rows += 1
            self.table1.setRowCount(self.rows)
        self.add_table()

    def insert_curr(self):
        self.id_n = self.id.currentText()
        self.id_c_n = self.id_c.currentText()
        self.can_n = self.can.currentText()
        self.data_n = self.data.text()[0:10]

        data_add = datetime.strptime(self.data_n, '%d-%m-%Y').strftime('%d-%b-%Y').upper()

        try:
            query = "INSERT INTO bon_fiscal VALUES ('{}',{},{},bon_fiscal_nr_bon_seq.currval,{})".format(data_add,
                                                                                                         self.id_n,
                                                                                                         self.id_c_n,
                                                                                                         self.can_n)
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)

        try:
            query = "update medicament set stoc=stoc-{} where id_medicament={}".format(self.can_n, self.id_n)
        except Exception as err:
            print(err)

        ok = 1
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
            ok = 0

        if ok:
            self.rows += 1
            self.table1.setRowCount(self.rows)
        self.add_table()

    def update(self):
        self.id2_n = self.id2.currentText()
        self.id_c2_n = self.id_c2.currentText()
        self.can2_n = self.can2.currentText()
        self.data2_n = self.data2.text()[0:10]
        diff = int(self.can2_n) - int(self.items[4])
        data_add = datetime.strptime(self.data2_n, '%d-%m-%Y').strftime('%d-%b-%Y').upper()

        try:
            query = "update bon_fiscal set data_achizitie='{}',medicament_id_medicament={},clienti_id_client={}," \
                    "cantitate={} where nr_bon={} and medicament_id_medicament={}".format(data_add, self.id2_n,
                                                                                          self.id_c2_n, self.can2_n,
                                                                                          self.items[3], self.items[1])
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)

        try:
            query = "update medicament set stoc=stoc-({}) where id_medicament={}".format(diff, self.id2_n)
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)

        self.add_table()

    def delete(self):
        try:
            query = "delete bon_fiscal where medicament_id_medicament={} and nr_bon={}".format(self.items[1],
                                                                                               self.items[3])
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
            self.table1.setRowCount(self.rows)
        self.add_table()
