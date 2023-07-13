from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
import sqlite3
from get_faces_from_camera_tkinter import *
from features_extraction_to_csv import *
from face_reco_from_camera import *

class choose_widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("基于openCV+dlib人脸识别寝室门禁系统")
        self.lb_pic = QLabel()
        self.lb_pic.setFixedSize(QSize(640, 500))
        self.setWindowIcon(QIcon("F:/SHI_XUN/pythonProject2/day7/face_look2/xiaohui.jpg"))
        self.setStyleSheet("QLabel {color:yellow ; border-image:url(cover.jpg)}")
        self.bnt_start = QPushButton("人脸识别")
        self.bnt_stop = QPushButton("管理员登录")
        self.bnt_start.setStyleSheet("QPushButton {background-color : cornflowerblue; font:bold,20px}")
        self.bnt_stop.setStyleSheet("QPushButton {background-color : pink; font:bold,20px}")

        self.central_widget = QWidget(self)
        self.hb1 = QHBoxLayout()
        self.hb2 = QHBoxLayout()
        self.vb1 = QVBoxLayout()

        self.hb1.addWidget(self.lb_pic)
        self.hb2.addWidget(self.bnt_start)
        self.hb2.addWidget(self.bnt_stop)

        self.vb1.addLayout(self.hb1)
        self.vb1.addLayout(self.hb2)

        self.central_widget.setLayout(self.vb1)
        self.setCentralWidget(self.central_widget)

        self.bnt_start.clicked.connect(self.faceIdentify)
        self.bnt_stop.clicked.connect(self.go_to_register_window)

        self.widget = None

    def faceIdentify(self):
        # self.hide()
        img_to_csv()
        start_identify()

    def go_to_register_window(self):
        # self.hide()
        stacked_widget = QStackedWidget()
        login_window = LoginWindow(stacked_widget)
        stacked_widget.addWidget(login_window)

        stacked_widget.show()

class RegisterWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("注册")
        self.stacked_widget = stacked_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label_username = QLabel("用户名:")
        self.edit_username = QLineEdit()
        self.edit_username.setPlaceholderText("请输入用户名")
        layout.addWidget(label_username)
        layout.addWidget(self.edit_username)

        label_password = QLabel("密码:")
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setPlaceholderText("请输入密码")
        layout.addWidget(label_password)
        layout.addWidget(self.edit_password)

        btn_register = QPushButton("注册")
        btn_register.clicked.connect(self.register)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def register(self):
        username = self.edit_username.text()
        password = self.edit_password.text()

        if not username or not password:
            QMessageBox.critical(self, "错误", "用户名和密码不能为空！")
            return

        if self.is_username_taken(username):
            QMessageBox.critical(self, "错误", "用户名已被注册！")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT,
                           password TEXT)''')

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "成功", "注册成功！")
        self.stacked_widget.setCurrentIndex(0)

    def is_username_taken(self, username):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        conn.close()

        return result is not None


class LoginWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("公寓人员信息管理系统")
        self.setFixedSize(QSize(320,240))
        self.setWindowIcon(QIcon("F:/SHI_XUN/pythonProject2/day7/face_look2/xiaohui.jpg"))
        # self.setStyleSheet("QLabel {color:yellow ; border-image:url(F:/SHI_XUN/pythonProject2/day7/face_look2/xinkong.jpg)}")
        self.stacked_widget = stacked_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label_username = QLabel("用户名:")
        self.edit_username = QLineEdit()
        self.edit_username.setPlaceholderText("请输入用户名")
        layout.addWidget(label_username)
        layout.addWidget(self.edit_username)

        label_password = QLabel("密码:")
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setPlaceholderText("请输入密码")
        layout.addWidget(label_password)
        layout.addWidget(self.edit_password)


        btn_login = QPushButton("登录")
        btn_login.clicked.connect(self.login)
        btn_login.setStyleSheet("QPushButton {background-color : peachpuff; font:bold,20px}")
        layout.addWidget(btn_login)

        btn_register = QPushButton("注册")
        btn_register.clicked.connect(self.open_register_window)
        btn_register.setStyleSheet("QPushButton {background-color : lightblue; font:bold,20px}")
        layout.addWidget(btn_register)

        # btn_quit = QPushButton("返回")
        # btn_quit.clicked.connect(self.go_to_main_window)
        # btn_quit.setStyleSheet("QPushButton {background-color : lightsteelblue; font:bold,20px}")
        # layout.addWidget(btn_quit)

        self.setLayout(layout)

    # def go_to_main_window(self):
    #     self.hide()

    def open_register_window(self):
        register_window = RegisterWindow(self.stacked_widget)
        self.stacked_widget.addWidget(register_window)
        self.stacked_widget.setCurrentWidget(register_window)

    def login_redirect(self):
        self.hide()
        self.third_window = mywidget()
        self.third_window.show()

    def login(self):
        username = self.edit_username.text()
        password = self.edit_password.text()

        if not username or not password:
            QMessageBox.critical(self, "错误", "用户名和密码不能为空！")
            return

        # 在数据库中查是否有当前管理员

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()

        conn.close()

        if result is not None:
            QMessageBox.information(self, "成功", "登录成功！")
            self.login_redirect()
        else:
            QMessageBox.critical(self, "错误", "用户名或密码错误！")


class mywidget(QWidget):
    def __init__(self):
        super().__init__()
        self.work_info = {}
        self.setWindowTitle("数据库表格操作APP")
        # self.resize(500, 500)
        self.setWindowIcon(QIcon("F:/SHI_XUN/pythonProject2/day7/face_look2/xiaohui.jpg"))
        self.db_path = QLineEdit()
        self.table_name = QLineEdit()

        self.u_id_lineedit = QLineEdit()
        self.u_name_lineedit = QLineEdit()
        self.u_type_lineedit = QLineEdit()
        self.u_dorm_lineedit = QLineEdit()
        self.u_bed_lineedit = QLineEdit()
        self.face_image_lineedit = QLineEdit()

        self.table_name_lb = QLabel("表名:")
        self.u_id_lb = QLabel("用户ID:")
        self.u_name_lb = QLabel("用户名:")
        self.u_type_lb = QLabel("用户类型:")
        self.u_dorm_lb = QLabel("用户宿舍:")
        self.u_bed_lb = QLabel("用户床号:")
        self.face_image_lb = QLabel("用户人脸:")
        self.bnt_face_image = QPushButton("选择想要添加的图片路径")
        self.bnt_select_db = QPushButton("选择想要打开的数据库")
        self.bnt_insert = QPushButton("插入数据")
        self.bnt_delete = QPushButton("删除数据")
        self.bnt_change = QPushButton("修改数据")
        self.bnt_search = QPushButton("查询数据")
        self.bnt_search_student = QPushButton("查找学生")
        self.bnt_pic = QPushButton("录入人脸")
        self.bnt_quit = QPushButton("退出")
        self.bnt_face_image.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")
        self.bnt_select_db.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")
        self.bnt_insert.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")
        self.bnt_delete.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")
        self.bnt_change.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")
        self.bnt_search.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")
        self.bnt_search_student.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")
        self.bnt_pic.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")
        self.bnt_quit.setStyleSheet("QPushButton {background-color : lightsteelblue; font:bold,10px}")
        self.bnt_face_image.setStyleSheet("QPushButton {background-color : papayawhip; font:bold,20px}")

        self.show_table = QTableWidget()

        self.hb1 = QHBoxLayout()
        self.hb2 = QHBoxLayout()
        self.hb3 = QHBoxLayout()
        self.hb4 = QHBoxLayout()
        self.hb5 = QHBoxLayout()

        self.vb1 = QVBoxLayout()

        self.hb1.addWidget(self.db_path)
        self.hb1.addWidget(self.bnt_select_db)
        self.hb1.addWidget(self.bnt_pic)
        self.hb1.addWidget(self.bnt_quit)


        self.hb2.addWidget(self.table_name_lb)
        self.hb2.addWidget(self.table_name)
        self.hb2.addWidget(self.u_id_lb)
        self.hb2.addWidget(self.u_id_lineedit)
        self.hb2.addWidget(self.u_name_lb)
        self.hb2.addWidget(self.u_name_lineedit)
        self.hb2.addWidget(self.u_type_lb)
        self.hb2.addWidget(self.u_type_lineedit)

        self.hb3.addWidget(self.u_dorm_lb)
        self.hb3.addWidget(self.u_dorm_lineedit)
        self.hb3.addWidget(self.u_bed_lb)
        self.hb3.addWidget(self.u_bed_lineedit)
        self.hb3.addWidget(self.face_image_lb)
        self.hb3.addWidget(self.face_image_lineedit)
        self.hb3.addWidget(self.bnt_face_image)

        self.hb4.addWidget(self.bnt_insert)
        self.hb4.addWidget(self.bnt_delete)
        self.hb4.addWidget(self.bnt_change)
        self.hb4.addWidget(self.bnt_search)
        self.hb4.addWidget(self.bnt_search_student)
        self.hb5.addWidget(self.show_table)

        self.vb1.addLayout(self.hb1)
        self.vb1.addLayout(self.hb2)
        self.vb1.addLayout(self.hb3)
        self.vb1.addLayout(self.hb4)
        self.vb1.addLayout(self.hb5)

        self.setLayout(self.vb1)
        self.bnt_insert.clicked.connect(self.do_insert)
        self.bnt_delete.clicked.connect(self.do_delete)
        self.bnt_change.clicked.connect(self.do_change)
        self.bnt_select_db.clicked.connect(self.do_select_db)
        self.bnt_search.clicked.connect(self.do_search)
        self.bnt_search.clicked.connect(self.do_search)
        self.bnt_search_student.clicked.connect(self.do_search_student)
        self.bnt_face_image.clicked.connect(self.do_select_image)  # 修改这里的连接信号操作
        self.bnt_pic.clicked.connect(self.do_pic_image)
        self.bnt_quit.clicked.connect(self.go_to_register_window)

        self.show()
    
    def go_to_register_window(self):
        self.hide()
        stacked_widget = QStackedWidget()
        login_window = LoginWindow(stacked_widget)
        stacked_widget.addWidget(login_window)

        stacked_widget.show()
    def do_pic_image(self):
        mySaveRun()

    def do_select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择人脸照片", "", "JPEG Files (*.jpg *.jpeg);;PNG Files (*.png)")
        if file_path:
            self.face_image_lineedit.setText(file_path)

    def do_select_db(self):
        db_file = QFileDialog.getOpenFileName(self, "选择数据库文件", "D:/Tencent Files/353620210/FileRecv")
        print(db_file)
        self.db_path.setText(db_file[0])

    def do_getworkinfo(self):
        self.work_info['表名'] = self.table_name.text()
        self.work_info['用户ID'] = self.u_id_lineedit.text()
        self.work_info['用户名'] = self.u_name_lineedit.text()
        self.work_info['用户类型'] = self.u_type_lineedit.text()
        self.work_info['用户宿舍'] = self.u_dorm_lineedit.text()
        self.work_info['用户床号'] = self.u_bed_lineedit.text()
        self.work_info['用户人脸照片'] = self.face_image_lineedit.text()

    def do_search(self):
        self.do_getworkinfo()
        if self.work_info['表名'] != "":
            dbconn = sqlite3.connect(self.db_path.text())
            cursor = dbconn.cursor()
            cursor.execute("select * from " + self.table_name.text())
            dbconn.commit()
            ret = cursor.fetchall()
            row = len(ret)
            clo = 6

            # 设置表头

            self.show_table.setRowCount(row)
            self.show_table.setColumnCount(clo)
            header_labels = ['用户ID', '用户名', '用户类型', '用户宿舍', '用户床号', '用户图片']
            self.show_table.setHorizontalHeaderLabels(header_labels)
            for i in range(row):
                for j in range(len(ret[i])):
                    myitem = QTableWidgetItem(str(ret[i][j]))
                    self.show_table.setItem(i, j, myitem)
            dbconn.close()
        self.vb1.addWidget(self.show_table)

    def do_insert(self):
        self.do_getworkinfo()
        if self.work_info['表名'] != "":
            if self.work_info['用户ID'] == "":
                QMessageBox.warning(self, "错误信息", "用户ID不能为空，请输入用户ID！")
            elif self.work_info['用户名'] == "":
                QMessageBox.warning(self, "错误信息", "用户名不能为空，请输入用户名！")
            elif self.work_info['用户类型'] == "":
                QMessageBox.warning(self, "错误信息", "用户类型不能为空！")
            elif self.work_info['用户宿舍'] == "":
                QMessageBox.warning(self, "错误信息", "用户宿舍不能为空！")
            elif self.work_info['用户床号'] == "":
                QMessageBox.warning(self, "错误信息", "用户宿舍不能为空！")
            elif self.work_info['用户宿舍'] == "":
                QMessageBox.warning(self, "错误信息", "用户宿舍不能为空！")
            elif self.work_info['用户人脸照片'] == "":
                QMessageBox.warning(self, "错误信息", "用户人脸不能为空！")
            else:
                dbconn = sqlite3.connect(self.db_path.text())
                cursor = dbconn.cursor()
                cursor.execute("INSERT INTO " + self.table_name.text() + " VALUES ( ?, ?, ? ,? , ? ,? )",
                               (self.work_info['用户ID'], self.work_info['用户名'], self.work_info['用户类型'],
                                self.work_info['用户宿舍'], self.work_info['用户床号'], self.work_info['用户人脸照片']))
                dbconn.commit()
                dbconn.close()
                self.do_search()
        else:
            QMessageBox.warning(self, "错误信息", "没有指定插入的表名！")

    def do_delete(self):
        self.do_getworkinfo()
        if self.work_info['表名'] != "" and self.work_info['用户ID'] != "":
            dbconn = sqlite3.connect(self.db_path.text())
            cursor = dbconn.cursor()
            cursor.execute("DELETE FROM " + self.table_name.text() + " WHERE u_id=?", (self.work_info['用户ID'],))
            dbconn.commit()
            dbconn.close()
            self.do_search()

    def do_change(self):
        if self.table_name == "" or self.u_id_lineedit.text() == "":
            QMessageBox.warning(self, "错误信息", "用户ID不能为空，请输入用户ID！")
            return

        self.do_getworkinfo()
        dbconn = sqlite3.connect(self.db_path.text())
        cursor = dbconn.cursor()

        if self.work_info['用户名'] == '' or self.work_info['用户类型'] == '' or self.work_info['用户宿舍'] == '' or \
                self.work_info['用户床号'] == '' or self.work_info['用户人脸照片'] == '':
            QMessageBox.warning(self, "错误信息", "信息不能为空")
            return

        cursor.execute("UPDATE " + self.table_name.text() +
                       " SET u_name=?, u_type=?, u_dorm=?, u_bed=?, face_image=? WHERE u_id=?",
                       (self.work_info['用户名'], self.work_info['用户类型'], self.work_info['用户宿舍'],
                        self.work_info['用户床号'], self.work_info['用户人脸照片'], self.work_info['用户ID']))

        dbconn.commit()
        dbconn.close()
        self.do_search()

    def do_search_student(self):
        student_id = self.u_id_lineedit.text()
        if student_id != "":
            dbconn = sqlite3.connect(self.db_path.text())
            cursor = dbconn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name.text()} WHERE u_id=?", (student_id,))
            ret = cursor.fetchone()
            if ret is not None:
                self.u_id_lineedit.setText(str(ret[0]))
                self.u_name_lineedit.setText(str(ret[1]))
                self.u_type_lineedit.setText(str(ret[2]))
                self.u_dorm_lineedit.setText(ret[3])
                self.u_bed_lineedit.setText(ret[4])
                self.face_image_lineedit.setText(ret[5])
                # 清空表格内容
                self.show_table.clear()
                self.show_table.setColumnCount(6)  # 修改列数为6
                self.show_table.setRowCount(1)
                # 设置表头

                header_labels = ['用户ID', '用户名', '用户类型', '用户宿舍', '用户床号', '用户图片']
                self.show_table.setHorizontalHeaderLabels(header_labels)

                # 填充表格数据
                for i in range(6):
                    item = QTableWidgetItem(str(ret[i]))
                    self.show_table.setItem(0, i, item)
            else:
                QMessageBox.warning(self, "错误信息", "找不到对应的学生信息")
            dbconn.close()
        else:
            QMessageBox.warning(self, "错误信息", "请输入学生ID")

if __name__ == "__main__":
    app = QApplication([])
    main_window = choose_widget()
    main_window.show()
    sys.exit(app.exec())

