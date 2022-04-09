from PyQt5 import QtWidgets, QtGui


class Furnizor:
    def __init__(self, interface, db):
        self.interface = interface
        self.database = db
        self.rows = 6

    def show(self):

        self.table = self.interface.get_furnizor_table()
        self.table.setRowCount(self.rows)

        self.nume_furnizor,self.insert_btn=self.interface.get_furnizor_insert()
        self.nume1, self.update_btn, self.select_btn = self.interface.get_furnizor_update()
        self.nume_list,self.id_list,self.delete_btn, self.select_btn1 = self.interface.get_furnizor_delete()
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
            self.id_list.setText(self.items[0])
            self.nume_list.setText(self.items[1])

    def add_table(self):
        query = "select * from furnizor order by id_furnizor"
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
        self.nume = self.nume_furnizor.text()

        try:
            query = "insert into furnizor (nume_furnizor) values ('{}')".format(self.nume)
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
            query = "update furnizor set nume_furnizor='{}' where id_furnizor={}".format(self.nume1.text(), self.items[0])
        except Exception as err:
            print(err)
        try:
            self.database.execute_query(query)
        except Exception as err:
            print(err)
        self.add_table()

    def delete(self):
        try:
            query = "delete furnizor where id_furnizor={}".format(self.items[0])
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