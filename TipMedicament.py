from PyQt5 import QtWidgets, QtGui


class Tip:
    def __init__(self, interface, db):
        self.interface = interface
        self.database = db
        self.rows = 6

    def show(self):

        self.table = self.interface.get_tip_medicament_table()
        self.table.setRowCount(self.rows)

        self.nume_tip, self.insert_btn = self.interface.get_tip_medicament_insert()
        self.nume1, self.update_btn, self.select_btn = self.interface.get_tip_medicament_update()
        self.delete_btn, self.select_btn1, self.list = self.interface.get_tip_medicament_delete()
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
            self.nume1.setText(self.items[1])

    def selectare1(self):
        self.items = []
        selected = self.table.selectedItems()
        if selected:
            for item in selected:
                self.items.append(item.data(0))
        if len(self.items):
            self.list.setText(self.items[1])

    def add_table(self):
        query = "select * from tip_medicament order by id_tip"
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
        self.nume = self.nume_tip.text()

        try:
            query = "insert into tip_medicament (nume_tip) values ('{}')".format(self.nume)
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
        try:
            query = "update tip_medicament set nume_tip='{}' where id_tip={}".format(self.nume1.text(), self.items[0])
            print(query)
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
        self.add_table()

    def delete(self):
        try:
            query = "delete tip_medicament where id_tip={}".format(self.items[0])
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
