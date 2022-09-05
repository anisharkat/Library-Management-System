from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import datetime
import sys
import MySQLdb
from xlsxwriter import * 
from xlrd import *

MainUI,_ = loadUiType('main.ui')

class Main (QMainWindow,MainUI):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Db_connect()
        self.Handel_Buttons()
        self.UI_Changes()
        self.Open_Login_Tab()
        self.Show_All_Categories()
        self.Show_Branches()
        self.Show_Author()
        self.Show_Publishers()
        self.Show_All_Books()
        self.Show_All_Clients()
        self.Retrive_Day_Work()
        self.Show_Employee()

    def UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)
        self.setFixedWidth(1040)
        self.setFixedHeight(575)

    def Db_connect(self):
        self.db = MySQLdb.connect(host='localhost',user='root', password='anisharkat2005',db='lb')
        self.cur = self.db.cursor()

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Open_daily_Mouvments_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_4.clicked.connect(self.Open_Dashboard_Tab)
        self.pushButton_6.clicked.connect(self.Open_History_Tab)
        self.pushButton_5.clicked.connect(self.Open_Reports_Tab)
        self.pushButton_7.clicked.connect(self.Open_Settings_Tab)
        self.pushButton_41.clicked.connect(self.Open_Reset_Password_Tab)
        self.pushButton_47.clicked.connect(self.Open_Login_Tab)
        self.pushButton_21.clicked.connect(self.Add_Branch)
        self.pushButton_22.clicked.connect(self.Add_Publisher)
        self.pushButton_23.clicked.connect(self.Add_Author)
        self.pushButton_25.clicked.connect(self.Add_Category)
        self.pushButton_28.clicked.connect(self.Add_Employee)
        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_17.clicked.connect(self.Add_New_Client)
        self.pushButton_14.clicked.connect(self.Edit_Book_Search)
        self.pushButton_13.clicked.connect(self.Edit_Book)
        self.pushButton_19.clicked.connect(self.Edit_Client_Search)
        self.pushButton_20.clicked.connect(self.Edit_Client)
        self.pushButton_15.clicked.connect(self.Delete_Book)
        self.pushButton_18.clicked.connect(self.Delete_Client)
        self.pushButton_8.clicked.connect(self.Handel_to_Day_Work)
        self.pushButton_9.clicked.connect(self.All_Books_Filter)
        self.pushButton_30.clicked.connect(self.Check_Employee)
        self.pushButton_29.clicked.connect(self.Edit_Employee_Data)
        self.pushButton_31.clicked.connect(self.Add_Employee_Permission)
        self.pushButton_32.clicked.connect(self.Books_Export_Report)
        self.pushButton_35.clicked.connect(self.Clients_Export_Report)
        self.pushButton_38.clicked.connect(self.User_Login_Permissions)

    def handel_login(self):
        pass

    def Handel_Reset_Password(self):
        pass

    def Handel_to_Day_Work(self):
        book_title = self.lineEdit.text()
        client_national_id = self.lineEdit_33.text()
        type = self.comboBox.currentIndex()
        from_date = str(datetime.date.today())
        to_date = str(datetime.date.today())
        #to_date = self.dateEdit_6.date()
        date = datetime.datetime.now()
        branch = 1
        employee = 2

        self.cur.execute ('''
        INSERT INTO daily_movements (book_id , client_id , type  , date , branch_id , book_from , book_to , employee_id)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        ''',(book_title,client_national_id,type,date,branch,from_date,to_date,employee))

        self.db.commit()
        self.Retrive_Day_Work()


    def Retrive_Day_Work (self):
        self.cur.execute('''
        SELECT book_id , type , client_id , book_from , book_to FROM daily_movements
        ''')
        data = self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row , form in enumerate (data):
            for colum , item in enumerate (form):
                if colum == 1:
                    if item == 0 :
                        self.tableWidget.setItem(row,colum,QTableWidgetItem(str("Rent")))
                    else :
                        self.tableWidget.setItem(row,colum,QTableWidgetItem(str("Retrive")))
                elif colum ==2 :
                    sql = ''' SELECT name FROM clients WHERE national_id = %s '''

                else :
                    self.tableWidget.setItem(row,colum,QTableWidgetItem(str(item)))
                colum += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)


    #####################################################

    def Show_All_Books(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        self.cur.execute ('''
        SELECT code,title,category_id,author_id,price FROM books
        ''')
        data = self.cur.fetchall()
        for row , form in enumerate(data):
            for col ,item in enumerate(form):
                if col == 2 :
                    sql =(''' SELECT category_name FROM category WHERE id = %s ''')
                    self.cur.execute(sql,[(item)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(category_name[0])))
                elif col == 3:
                    sql =(''' SELECT name FROM author WHERE id = %s ''')
                    self.cur.execute(sql,[(item+1)])
                    author_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(author_name[0])))
                else:
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(item)))
                col+= 1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)



    def All_Books_Filter(self):
        book_title = self.lineEdit_2.text()
        category = self.comboBox_2.currentIndex()

        sql = '''
            SELECT code , title , category_id , author_id , publisher_id FROM books WHERE title = %s
        '''
        self.cur.execute(sql,[(book_title)])

        data = self.cur.fetchall()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        for row , form in enumerate(data):
            for col ,item in enumerate(form):
                if col == 2 :
                    sql =''' SELECT category_name FROM category WHERE id = %s '''
                    self.cur.execute(sql,[(item)])
                    category_name = self.cur.fetchone()

                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(item)))
                else :
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(item)))
                col+= 1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)


    def Add_New_Book(self):
        book_title = self.lineEdit_3.text()
        category = self.comboBox_3.currentIndex()
        description = self.textEdit_2.toPlainText()
        price  = self.lineEdit_5.text()
        code = self.lineEdit_6.text()
        publisher = self.comboBox_4.currentIndex()
        author = self.comboBox_5.currentIndex()
        status = self.comboBox_6.currentIndex()
        part_order = self.lineEdit_17.text()
        date = datetime.datetime.now()
        barcode = self.lineEdit_11.text()


        self.cur.execute('''
            INSERT INTO books (title,description,category_id,code,barcode,part_order,price,author_id,publisher_id,status,date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(book_title,description,category,code,barcode,part_order,price,author,publisher,status,date))

        self.db.commit()
        QMessageBox.information(self,"Success !","Book Added Successfully")
        self.Show_All_Books()

    def Edit_Book_Search(self):
        book_code = self.lineEdit_15.text()

        sql = ('''
        SELECT * FROM books WHERE code = %s
        ''')

        self.cur.execute(sql,[(book_code)])

        data = self.cur.fetchone()

        self.lineEdit_12.setText(data[1])
        self.comboBox_7.setCurrentIndex(int(data[10]))
        self.lineEdit_13.setText(str(data[6]))
        self.comboBox_16.setCurrentIndex(int(data[11]))
        self.comboBox_15.setCurrentIndex(int(data[12]))
        self.comboBox_17.setCurrentIndex(int(data[8]))
        self.lineEdit_16.setText(str(data[5]))
        self.textEdit.setPlainText(data[2])

    def Edit_Book(self):
        book_title = self.lineEdit_12.text()
        category = self.comboBox_7.currentIndex()
        description = self.textEdit.toPlainText()
        price  = self.lineEdit_13.text()
        code = self.lineEdit_15.text()
        publisher = self.comboBox_16.currentIndex()
        author = self.comboBox_15.currentIndex()
        status = self.comboBox_17.currentIndex()
        part_order = self.lineEdit_16.text()

        self.cur.execute('''
        UPDATE books SET title = %s ,description = %s, code = %s,
        part_order = %s, price = %s, status = %s, category_id = %s,
        publisher_id = %s, author_id = %s WHERE code = %s
        ''',(book_title,description,code,part_order,price,status,category,publisher,author,code))

        self.db.commit()
        QMessageBox.information(self,"Success !","Book Edited Successfully")
        self.Show_All_Books()



        QMessageBox.information(self,"Success !","The book information has been modified successfully")

    def Delete_Book(self):
        book_code = self.lineEdit_15.text()
        delete_message = QMessageBox.warning(self ,"Delete Book", "Are you sure to delete the book ?" ,QMessageBox.Yes | QMessageBox.No)


        if delete_message.QMessageBox.Yes :
            sql = ('''
                DELETE FROM books WHERE code = %s
                ''')

            self.cur.execute(sql,[(book_code)])
            self.db.commit()
            QMessageBox.information(self,"Success !","Book Deleted Successfully")
            self.Show_All_Books()





    #####################################################

    def Show_All_Clients(self):
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)

        self.cur.execute ('''
        SELECT name,mail,phone,national_id,date FROM clients
        ''')
        data = self.cur.fetchall()
        for row , form in enumerate(data):
            for col ,item in enumerate(form):
                self.tableWidget_4.setItem(row,col,QTableWidgetItem(str(item)))
                col+= 1
            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)

    def Add_New_Client(self):
        client_name = self.lineEdit_20.text()
        client_mail = self.lineEdit_21.text()
        client_phone = self.lineEdit_22.text()
        client_national_id = self.lineEdit_23.text()
        date = datetime.datetime.now()

        self.cur.execute('''
        INSERT INTO clients (name,mail,phone,national_id,date)
        VALUES (%s,%s,%s,%s,%s)
        ''',(client_name,client_mail,client_phone,client_national_id,date))

        self.db.commit()
        QMessageBox.information(self,"Success !","Client Added Successfully")
        self.Show_All_Clients()


    def Edit_Client_Search(self):
        client_data = self.lineEdit_28.text()


        if self.comboBox_14.currentIndex() == 0 :
            sql = (''' SELECT * FROM clients WHERE name = %s ''')

            self.cur.execute(sql,[(client_data)])

            data = self.cur.fetchone()


        if self.comboBox_14.currentIndex() == 1 :
            sql = (''' SELECT * FROM clients WHERE mail = %s ''')

            self.cur.execute(sql,[(client_data)])

            data = self.cur.fetchone()


        if self.comboBox_14.currentIndex() == 2 :
            sql = (''' SELECT * FROM clients WHERE phone = %s ''')

            self.cur.execute(sql,[(client_data)])

            data = self.cur.fetchone()


        if self.comboBox_14.currentIndex() == 3 :
            sql = (''' SELECT * FROM clients WHERE national_id = %s ''')

            self.cur.execute(sql,[(client_data)])

            data = self.cur.fetchone()


        self.lineEdit_27.setText(data[1])
        self.lineEdit_24.setText(data[2])
        self.lineEdit_26.setText(data[3])
        self.lineEdit_25.setText(str(data[5]))




    def Edit_Client(self):
        client_name = self.lineEdit_27.text()
        client_mail = self.lineEdit_24.text()
        client_phone = self.lineEdit_26.text()
        client_national_id = self.lineEdit_25.text()


        self.cur.execute('''
            UPDATE clients SET name = %s , mail = %s , phone = %s ,national_id = %s
        ''' , (client_name,client_mail,client_phone,client_national_id))
        self.db.commit()


        QMessageBox.information(self,"Success !","The Client informations has been modified successfully")

        self.Show_All_Clients()

    def Delete_Client(self):
        client_data = self.lineEdit_28.text()

        delete_message = QMessageBox.warning(self ,"Delete Book", "Are you sure to delete the client ?" ,QMessageBox.Yes | QMessageBox.No)


        if delete_message.QMessageBox.Yes :

            if self.comboBox_14.currentIndex() == 0 :
                sql = (''' DELETE FROM clients WHERE name = %s ''')

                self.cur.execute(sql,[(client_data)])



            if self.comboBox_14.currentIndex() == 1 :
                sql = (''' DELETE FROM clients WHERE mail = %s ''')

                self.cur.execute(sql,[(client_data)])



            if self.comboBox_14.currentIndex() == 2 :
                sql = (''' DELETE FROM clients WHERE phone = %s ''')

                self.cur.execute(sql,[(client_data)])


            if self.comboBox_14.currentIndex() == 3 :
                sql = (''' DELETE FROM clients WHERE national_id = %s ''')

                self.cur.execute(sql,[(client_data)])


            self.db.commit()
            QMessageBox.information(self,"Success !","Client Deleted Successfully")
            self.Show_All_Clients()





    #####################################################

    def Show_History (self):
        pass

    #####################################################

    def All_Books_Report (self):
        pass

    def Books_Filter_Report (self):
        pass


    def Books_Export_Report(self):

        self.cur.execute('''
            SELECT code , title , category_id , author_id , price FROM books
        ''')

        data = self.cur.fetchall()
        excel_file = Workbook('Books_report.xlsx')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0,0,'Book Code')
        sheet1.write(0,1,'Book Title')
        sheet1.write(0,2,'Category')
        sheet1.write(0,3,'Author')
        sheet1.write(0,4,'Price')


        row_number = 1
        for row in data :
            column_number = 0
            for item in row :
                sheet1.write(row_number,column_number,str(item))
                column_number += 1
            row_number += 1

        excel_file.close()   
        QMessageBox.information(self,"Success !","Books Exported Successfully") 

    #####################################################

    def All_Clients_Report (self):
        pass

    def Clients_Filter_Report (self):
        pass

    def Clients_Export_Report(self):
        self.cur.execute('''
            SELECT name , mail , phone , national_id  FROM clients
        ''')

        data = self.cur.fetchall()
        excel_file = Workbook('Clients_report.xlsx')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0, 0, 'CLient Name')
        sheet1.write(0, 1, 'CLient Mail')
        sheet1.write(0, 2, 'CLient Phone')
        sheet1.write(0, 3, 'CLient National Id')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        excel_file.close()
        QMessageBox.information(self,"Success !","Clients Exported Successfully")

    #####################################################

    def Monthly_Report(self):
        pass

    def Monthly_Report_Export(self):
        pass

    #####################################################

    def Add_Branch(self):
        branch_name = self.lineEdit_14.text()
        branch_code = self.lineEdit_18.text()
        branch_location = self.lineEdit_19.text()

        self.cur.execute('''
            INSERT INTO branch(name , code , location)
            VALUES(%s,%s,%s)
            ''' , (branch_name,branch_code,branch_location))
        self.db.commit()


    def Add_Category(self):
        category_name = self.lineEdit_39.text()
        parent_category_text = self.comboBox_8.currentText()


        # query = ''' SELECT id FROM category WHERE category_name = %s '''
        # self.cur.execute(query,[(parent_category_text)])
        # data = self.cur.fetchone()
        # category_parent = data[0]

        self.cur.execute('''
            INSERT INTO category(category_name,category_parent)
            VALUES(%s,%s)
            ''' , (category_name,parent_category_text))
        self.db.commit()
        self.Show_All_Categories()


    def Add_Publisher(self):
        publisher_name = self.lineEdit_29.text()
        publisher_location = self.lineEdit_30.text()


        self.cur.execute('''
            INSERT INTO publisher(name , location)
            VALUES(%s,%s)
            ''' , (publisher_name,publisher_location))
        self.db.commit()




    def Add_Author(self):
        author_name = self.lineEdit_31.text()
        author_location = self.lineEdit_32.text()

        self.cur.execute('''
            INSERT INTO author(name , location)
            VALUES(%s,%s)
            ''' , (author_name,author_location))
        self.db.commit()

    ##########################################

    def Show_All_Categories (self):
        self.comboBox_8.clear()
        self.cur.execute('''
            SELECT category_name FROM category
            ''')
        catigories = self.cur.fetchall()

        for category in catigories :
            self.comboBox_8.addItem(str(category[0]))
            self.comboBox_3.addItem(str(category[0]))
            self.comboBox_7.addItem(str(category[0]))
            self.comboBox_2.addItem(str(category[0]))




    def Show_Branches(self):
        self.cur.execute ('''
            SELECT name FROM branch
            ''')

        branches = self.cur.fetchall()
        for branch in branches :
            self.comboBox_21.addItem(branch[0])
            self.comboBox_22.addItem(branch[0])


    def Show_Publishers(self):
        self.cur.execute('''
            SELECT name FROM publisher
            ''')

        publishers = self.cur.fetchall()
        for publisher in publishers :
            self.comboBox_4.addItem(publisher[0])
            self.comboBox_16.addItem(publisher[0])


    def Show_Author(self):
        self.cur.execute('''
            SELECT name FROM author
            ''')
        authors = self.cur.fetchall()
        for author in authors :
            self.comboBox_5.addItem(author[0])
            self.comboBox_15.addItem(author[0])



    def Show_Employee(self):
        self.cur.execute (''' SELECT name FROM employee ''')
        employees = self.cur.fetchall()
        for employee in employees :
            self.comboBox_11.addItem(employee[0])



    #####################################################

    def Add_Employee(self):
        employee_name = self.lineEdit_38.text()
        employee_mail = self.lineEdit_41.text()
        employee_phone = self.lineEdit_40.text()
        employee_branch = self.comboBox_21.currentIndex()
        national_id = self.lineEdit_42.text()
        priority = self.lineEdit_71.text()
        password = self.lineEdit_43.text()
        password2 = self.lineEdit_44.text()
        date = datetime.datetime.now()

        if password == password2 :
            self.cur.execute('''
            INSERT INTO employee (name,mail,phone,branch,national_id,date,priority,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(employee_name,employee_mail,employee_phone,employee_branch,national_id,date,priority,password))

            self.db.commit()
            self.lineEdit_38.setText('')
            self.lineEdit_41.setText('')
            self.lineEdit_40.setText('')
            self.lineEdit_42.setText('')
            self.lineEdit_71.setText('')
            self.lineEdit_43.setText('')
            self.lineEdit_44.setText('')
            QMessageBox.information(self,"Success !","Employee Added Successfully")
        else :
            QMessageBox.warning(self,"Warning","The two passwords are not equal")


    def Check_Employee (self):
        employee_name = self.lineEdit_51.text()
        employee_password = self.lineEdit_57.text()
        self.cur.execute(''' SELECT * FROM employee ''')
        data = self.cur.fetchall()

        for row in data :
            if row[1] == employee_name and row[7] == employee_password :
                self.groupBox_9.setEnabled(True)
                self.lineEdit_53.setText(row[2])
                self.lineEdit_52.setText(row[3])
                self.comboBox_22.setCurrentIndex(int(row[8]))
                self.lineEdit_54.setText(str(row[5]))
                self.lineEdit_72.setText(str(row[6]))
                self.lineEdit_56.setText(str(row[7]))



    def Edit_Employee_Data(self):
        employee_name = self.lineEdit_51.text()
        employee_password = self.lineEdit_57.text()
        employee_email = self.lineEdit_53.text()
        employee_phone = self.lineEdit_52.text()
        employee_branch = self.comboBox_22.currentIndex()
        employee_national_id = self.lineEdit_54.text()
        employee_property = self.lineEdit_72.text()
        employee_password2 = self.lineEdit_56.text()
        date = datetime.datetime.now()

        if employee_password == employee_password2 :
            self.cur.execute('''
                UPDATE employee SET mail = %s , phone = %s , national_id = %s , priority = %s , password = %s , branch = %s WHERE name = %s
            ''',(employee_email,employee_phone,employee_national_id,employee_property,employee_password2,employee_branch,employee_name))
            self.db.commit()
            self.lineEdit_51.setText('')
            self.lineEdit_57.setText('')
            self.lineEdit_53.setText('')
            self.lineEdit_52.setText('')
            self.lineEdit_51.setText('')
            self.lineEdit_54.setText('')
            self.lineEdit_72.setText('')
            self.lineEdit_56.setText('')
            self.comboBox_22.setCurrentIndex(0)
            self.groupBox_9.setEnabled(False)
            QMessageBox.information(self,"Success !","Employee Informations Edited Successfully")


    def Add_Employee_Permission(self):
        employee_name = self.comboBox_11.currentText()

        if self.checkBox_41.isChecked() == True:
            self.cur.execute('''
                INSERT INTO employee_permissions (employee_name,books_tab,clients_tab,dashboard_tab,history_tab,reports_tab,settings_tab ,
                                                   add_book,edit_book,delete_book,import_book,export_book  ,
                                                   add_client,edit_client,delete_client,import_client,export_client ,
                                                   add_branch,add_publisher,add_author,add_category,add_employee,edit_employee , is_admin)
                VALUES(%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s, %s , %s , %s , %s , %s, %s , %s , %s , %s , %s , %s , %s)
            ''', (employee_name, 1, 1, 1, 1, 1, 1 , 1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1 , 1))
            self.db.commit()
            QMessageBox.information(self,"Success !","Employee Is Now Admin")
   
        else :

            books_tab = 0
            clients_tab = 0
            dashboard_tab = 0
            history_tab = 0
            reports_tab = 0
            settings_tab = 0

            add_book = 0
            edit_book = 0
            delete_book = 0
            import_book = 0
            export_book = 0

            add_client = 0
            edit_client = 0
            delete_client = 0
            import_client = 0
            export_client = 0

            add_branch = 0
            add_publisher = 0
            add_author = 0
            add_category = 0
            add_employee = 0
            edit_employee = 0


            if self.checkBox_12.isChecked() == True :
                books_tab = 1
            if self.checkBox_6.isChecked() == True :
                clients_tab = 1
            if self.checkBox_8.isChecked() == True :
                dashboard_tab = 1
            if self.checkBox_10.isChecked() == True :
                history_tab = 1
            if self.checkBox_9.isChecked() == True :
                reports_tab = 1
            if self.checkBox_11.isChecked() == True :
                settings_tab = 1
            if self.checkBox.isChecked() == True :
                add_book = 1
            if self.checkBox_2.isChecked() == True :
                edit_book = 1
            if self.checkBox_3.isChecked() == True :
                delete_book = 1
            if self.checkBox_13.isChecked() == True :
                import_book = 1
            if self.checkBox_14.isChecked() == True :
                export_book = 1
            if self.checkBox_5.isChecked() == True :
                add_client = 1
            if self.checkBox_4.isChecked() == True :
                edit_client = 1
            if self.checkBox_7.isChecked() == True :
                delete_client = 1
            if self.checkBox_16.isChecked() == True :
                import_client = 1
            if self.checkBox_15.isChecked() == True :
                export_client = 1
            if self.checkBox_36.isChecked() == True :
                add_branch = 1
            if self.checkBox_37.isChecked() == True :
                add_publisher = 1
            if self.checkBox_35.isChecked() == True :
                add_author = 1
            if self.checkBox_38.isChecked() == True :
                add_category = 1
            if self.checkBox_39.isChecked() == True :
                add_employee = 1
            if self.checkBox_40.isChecked() == True :
                edit_employee = 1


        self.cur.execute('''
                INSERT INTO employee_permissions (employee_name,books_tab,clients_tab,dashboard_tab,history_tab,reports_tab,settings_tab ,
                                                   add_book,edit_book,delete_book,import_book,export_book  ,
                                                   add_client,edit_client,delete_client,import_client,export_client ,
                                                   add_branch,add_publisher,add_author,add_category,add_employee,edit_employee)
                                                   
                VALUES(%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s, %s , %s , %s , %s , %s, %s , %s , %s , %s , %s , %s)
            ''' , ( employee_name, books_tab ,clients_tab ,  dashboard_tab , history_tab ,reports_tab , settings_tab
                    , add_book , edit_book , delete_book , import_book , export_book ,
                    add_client , edit_client , delete_client , import_client , export_client ,
                    add_branch , add_publisher , add_author , add_category , add_employee , edit_employee))
        
        self.db.commit()
        QMessageBox.information(self,"Success !","Employee Permissions Edited Successfully")


    def Admin_Report(self):
        pass

    #####################################################

    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Reset_Password_Tab(self):
        self.tabWidget.setCurrentIndex(1)



    def Open_daily_Mouvments_Tab(self):
        self.tabWidget.setCurrentIndex(2)




    def Open_Books_Tab(self):
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(3)



    def Open_Clients_Tab(self):
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(4)


    def Open_Dashboard_Tab(self):
        self.tabWidget.setCurrentIndex(5)


    def Open_History_Tab(self):
        self.tabWidget.setCurrentIndex(6)


    def Open_Reports_Tab(self):
        self.tabWidget_5.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(7)



    def Open_Settings_Tab(self):
        self.tabWidget_4.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(8)


    def User_Login_Permissions(self):
        username = self.lineEdit_45.text()
        password = self.lineEdit_47.text()

        self.cur.execute(''' SELECT id , name , password , branch FROM employee ''')
        data = self.cur.fetchall()
        for row in data:
            if row[1] == username and row[2] == password:
                self.cur.execute('''
                    SELECT * FROM employee_permissions WHERE employee_name = %s
                ''', (username,))
                user_permissions = self.cur.fetchone()
                self.pushButton.setEnabled(True)
                self.groupBox_14.setEnabled(True)



                if user_permissions[2] == 1:
                    self.pushButton_2.setEnabled(True)
                if user_permissions[3] == 1:
                    self.pushButton_3.setEnabled(True)
                if user_permissions[4] == 1:
                    self.pushButton_4.setEnabled(True)

                if user_permissions[4] == 1:
                    self.pushButton_6.setEnabled(True)

                if user_permissions[5] == 1:
                    self.pushButton_5.setEnabled(True)
                
                if user_permissions[6] == 1:
                    self.pushButton_7.setEnabled(True)
                
                if user_permissions[8] == 1:
                    self.pushButton_10.setEnabled(True)   

                if user_permissions[9] == 1:
                    self.pushButton_13.setEnabled(True)
                
                if user_permissions[10] == 1:
                    self.pushButton_15.setEnabled(True)
                
                if user_permissions[11] == 1:
                    self.pushButton_33.setEnabled(True)
                
                if user_permissions[12] == 1:
                    self.pushButton_32.setEnabled(True)
                
                if user_permissions[13] == 1:
                    self.pushButton_17.setEnabled(True)
                
                if user_permissions[14] == 1:
                    self.pushButton_20.setEnabled(True)
                
                if user_permissions[15] == 1:
                    self.pushButton_18.setEnabled(True)
                
                if user_permissions[16] == 1:
                    self.pushButton_36.setEnabled(True)
                
                if user_permissions[17] == 1:
                    self.pushButton_35.setEnabled(True)
                
                



                if user_permissions[18] == 1:
                    self.pushButton_21.setEnabled(True)
                
                if user_permissions[19] == 1:
                    self.pushButton_22.setEnabled(True)
                
                if user_permissions[20] == 1:
                    self.pushButton_23.setEnabled(True)
                
                if user_permissions[21] == 1:
                    self.pushButton_25.setEnabled(True)
                
                if user_permissions[22] == 1:
                    self.pushButton_28.setEnabled(True)
                
                if user_permissions[23] == 1:
                    self.pushButton_28.setEnabled(True)
   
            













                ###################



                
                
                




def main() :
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()
