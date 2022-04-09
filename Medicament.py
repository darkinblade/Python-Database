from PyQt5 import QtWidgets, QtGui


class Medicament:
    def __init__(self, interface, db):
        self.interface = interface
        self.database = db
        self.rows = 50

    def show(self):
        self.table = self.interface.get_medicament_table()
        self.table.setRowCount(self.rows)

        self.nume,  self.stoc, self.um, self.pret, self.id_t, self.id_f, self.insert_btn = self.interface.get_medicament_insert()
        self.nume2, self.stoc2, self.um2, self.pret2, self.id_f2, self.id_t2, self.update_btn, self.select_btn = self.interface.get_medicament_update()
        self.nume3, self.stoc3, self.id3, self.um3, self.pret3, self.id_t3, self.id_f3, self.delete_btn, self.select_btn1 = self.interface.get_medicament_delete()
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
            self.nume2.setText(self.items[0])
            self.stoc2.setText(self.items[2])
            self.um2.setText(self.items[3])
            self.pret2.setText(self.items[4])
            self.id_t2.setCurrentText(self.items[5])
            self.id_f2.setCurrentText(self.items[6])

    def selectare1(self):
        self.items = []
        selected = self.table.selectedItems()
        if selected:
            for item in selected:
                self.items.append(item.data(0))
        if len(self.items):
            self.nume3.setText(self.items[0])
            self.id3.setText(self.items[1])
            self.stoc3.setText(self.items[2])
            self.um3.setText(self.items[3])
            self.pret3.setText(self.items[4])
            self.id_t3.setText(self.items[5])
            self.id_f3.setText(self.items[6])

    def add_table(self):
        query = "select id_tip from tip_medicament"
        self.rez = ""
        try:
            self.rez = self.database.execute_query(query)
        except Exception as err:
            print(err)
        list_id_t = []
        for id in self.rez:
            list_id_t.append(str(id[0]))
        self.id_t.clear()
        self.id_t.addItems(list_id_t)
        self.id_t2.clear()
        self.id_t2.addItems(list_id_t)

        query = "select id_furnizor from furnizor"
        self.rez = ""
        try:
            self.rez = self.database.execute_query(query)
        except Exception as err:
            print(err)
        list_id_f = []
        for id in self.rez:
            list_id_f.append(str(id[0]))
        self.id_f.clear()
        self.id_f.addItems(list_id_f)
        self.id_f2.clear()
        self.id_f2.addItems(list_id_f)

        query = "select nume_medicament,id_medicament,stoc,um,pret,tip_medicament_id_tip,furnizor_id_furnizor from medicament order by id_medicament"
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
                self.table.setItem(row, col, cell)
                col += 1
            row += 1
        self.table.setRowCount(row)

    def insert(self):
        self.nume_med = self.nume.text()
        self.stoc_med = self.stoc.text()
        self.um_med = self.um.text()
        self.pret_med = self.pret.text()
        self.id_tip_med = self.id_t.currentText()
        self.id_furnizor = self.id_f.currentText()

        try:
            query = "insert into medicament(nume_medicament,stoc,um,pret,tip_medicament_id_tip,furnizor_id_furnizor) " \
                    "values ('{}',{},'{}',{},{},{})".format(self.nume_med, self.stoc_med, self.um_med, self.pret_med, self.id_tip_med, self.id_furnizor)
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
            self.table.setRowCount(self.rows)
        self.add_table()

    def update(self):
        self.nume_med2 = self.nume2.text()
        self.stoc_med2 = self.stoc2.text()
        self.um_med2 = self.um2.text()
        self.pret_med2 = self.pret2.text()
        self.id_tip_med2 = self.id_t2.currentText()
        self.id_furnizor2 = self.id_f2.currentText()
        try:
            query = "update medicament set nume_medicament='{}',stoc={},um='{}',pret={},tip_medicament_id_tip={},furnizor_id_furnizor={} where id_medicament={}".format(
                self.nume_med2, self.stoc_med2, self.um_med2, self.pret_med2, self.id_tip_med2, self.id_furnizor2,
                self.items[1])
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
        self.add_table()

    def delete(self):
        try:
            query = "delete medicament where id_medicament={}".format(self.items[1])
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
