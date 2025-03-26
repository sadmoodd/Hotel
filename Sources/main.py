import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QMessageBox
from PyQt5 import QtWidgets
import MainWindow, EmployerForm, AddHotel, HotelRew
import RegForm
import sqlite3
import hashlib

def hash_ps(password):
    return hashlib.sha256(password.encode()).hexdigest()

class HotelReviewer(HotelRew.Ui_Form):
    def setupUi(self, Form):
        super().setupUi(Form)
        

class AddHotelForm(AddHotel.Ui_HotelAddForm):
    def setupUi(self, HotelAddForm):
        super().setupUi(HotelAddForm)
        self.buttonBox.accepted.connect(lambda: self.get_info(HotelAddForm))
        self.buttonBox.rejected.connect(HotelAddForm.reject)
        self.DBConnector = DBConnector('HotelSystem.db')
        
    
    def get_info(self, AddHotelForm):
        hotelName = self.hotelName.text()
        try:
            # roomCount = int(self.roomCount.text())
            self.DBConnector.addHotel(hotelName)
            AddHotelForm.accept()
        except Exception as e:
            QMessageBox.warning(AddHotelForm, "Ошибка", f"Неверный ввод данных!\n {e}")

    
class DBConnector():
    def __init__(self, database):
        self.db = database
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = self.cursor.fetchone()
        
        return user # (id, username, password, status)
    
    def close(self):
        self.conn.close()
        self.cursor.close()


    def addUser(self, username: str, password: str, status: int):
        hashed_password = hash_ps(password)
        try:
            self.cursor.execute('INSERT INTO users (username, password, status) VALUES (?, ?, ?)', 
                                (username, hashed_password, status))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Пользователь с таким именем уже существует")
            return False
        except Exception as e:
            print(f'Произошла ошибка {e}')
            return False
        finally:
            self.conn.close()

    def addHotel(self, hotelName: str):
        try:
            self.cursor.execute('INSERT INTO hotels (hotelName) VALUES (?)', 
                                (hotelName, ))
            self.conn.commit()
        except Exception as e:
            print(f"Произошла ошибка {e}")
            return False
        finally:
            self.conn.close()

    def get_all_hotels(self):
        try:
            self.cursor.execute('SELECT hotelName FROM hotels')
            hotels = self.cursor.fetchall()
            hotels_strings = []
            for hotel in hotels:
                hotel_name = hotel[0]  
                hotels_strings.append(hotel_name) 
            return hotels_strings
        except Exception as e:
            print(f"Ошибка при извлечении отелей: {e}")
            return []
        finally:
            self.conn.close()

    def delHotel(self, hotelName):
        pass #TODO


class Register(RegForm.Ui_Dialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        self.buttonBox.accepted.connect(lambda: self.on_ok(Dialog))
        self.buttonBox.rejected.connect(Dialog.reject)
        self.DbConnector = DBConnector('HotelSystem.db')

    def on_ok(self, Dialog):
        username = self.username.text()      
        passwd = self.password.text()    
        if self.comboBox.currentIndex() == 0:
            print("Вы ничего не выбрали")
            QMessageBox.warning(Dialog, "Ошибка", "Пожалуйста, проверьте правильность ввода данных и корректность выбора из списка.")
        else:    
            status = self.comboBox.currentIndex()
            print(status)
            self.addUser(username, passwd, status)
            Dialog.accept()  # Закрываем диалог после успешного добавления

    def addUser(self, username, password, status):
        self.DbConnector.addUser(username, password, status)
        

class EmployerForm_(EmployerForm.Ui_AdminForm):
    def setupUi(self, AdminForm, username: str):
        super().setupUi(AdminForm)
        self.addHotelBtn.clicked.connect(self.openHotelAdder)
        self.lineEdit.setText(username)
        # self.pushButton_4.clicked.connect(self.exit)
        self.addHotelBtn.clicked.connect(self.openAddHotelForm)
        self.DBConnector = DBConnector('HotelSystem.db')
        self.updateBtn.clicked.connect(self.loadHotels)
        self.seeHotelBtn.clicked.connect(self.openHotelForm)

        # self.loadHotels()

    def delHotel(self):
        curHotel = self.comboBox.itemText(self.comboBox.currentIndex())




    def openHotelForm(self):
        w = QtWidgets.QDialog()
        ui = HotelReviewer()
        ui.setupUi(w)
        w.exec_()


    def openAddHotelForm(self):
        w = QtWidgets.QDialog()
        ui = AddHotelForm()
        ui.setupUi(w)
        w.exec_()
        
    def loadHotels(self):
        hotels = self.DBConnector.get_all_hotels()  # Получаем названия отелей
        if hotels:
            # for i in hotels:
            self.comboBox.clear()
            self.comboBox.addItems(hotels)  # Добавляем названия отелей в comboBox
        

    def openHotelAdder(self):
        pass

    def set_current_user(self, username):
        self.lineEdit.setText(username)

    def exit(self):        
        self.hide()
        

class MainWin(MainWindow.Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.exitBtn.clicked.connect(self.exit)
        # self.clientRB.toggled.connect(self.unlockFields)
        # self.workerRB.toggled.connect(self.unlockFields)
        self.regBtn.clicked.connect(self.openRegisterForm)
        self.loginField.textChanged.connect(self.unlockLogin)
        self.passwdField.textChanged.connect(self.unlockLogin)
        self.loginBtn.clicked.connect(self.get_data)
        self.DbConnector = DBConnector('HotelSystem.db')

    def get_data(self):
        username = self.loginField.text()
        password = hash_ps(self.passwdField.text())
        self.Login(username, password)
        

    def exit(self):
        QtWidgets.QApplication.quit()
    
    def unlockFields(self):
        if self.workerRB.isChecked() or self.clientRB.isChecked():
            self.loginField.setEnabled(True)
            self.passwdField.setEnabled(True)
        else:
            self.loginField.setEnabled(False)
            self.passwdField.setEnabled(False)

    def openRegisterForm(self):
        w = QtWidgets.QDialog()  # Создаем новое диалоговое окно
        ui = Register()  # Создаем экземпляр вашего окна регистрации
        ui.setupUi(w)  # Настраиваем интерфейс регистрации
        w.exec_()  # Показываем диалоговое окно как модальное

    def unlockLogin(self):
        if self.loginField.text() != "" and self.passwdField.text() != "":
            self.loginBtn.setEnabled(True)
        else:
            self.loginBtn.setEnabled(False)

    def Login(self, username, password):
        user = self.DbConnector.get_user(username)
        if user and user[2] == password:
            #print("OK")   
            if user[3] == 0:
                w = QtWidgets.QDialog()
                ui = EmployerForm_()
                ui.setupUi(w, user[1])
                w.exec_()
        else:
            pass

        
if __name__ == "__main__":
    # print(hash_ps("admin"))
    
    app = QApplication(sys.argv)  # Создание экземпляра приложения

    # Создание и инициализация главного окна
    w = QMainWindow()  # Создаем экземпляр QMainWindow
    ui = MainWin()  # Создание экземпляра вашего класса из MainWindow
    ui.setupUi(w)  # Настройка интерфейса пользователя на окне

    w.show()  # Отображение окна

    sys.exit(app.exec_())  # Запуск приложения

    

