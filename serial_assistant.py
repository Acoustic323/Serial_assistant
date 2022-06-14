import os
import sys
import time
import configparser
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import (QApplication, QMessageBox, QFileDialog, QPushButton, QLineEdit, QCheckBox)
from PyQt5.QtGui import QColor, QIcon, QTextCursor
from PyQt5.QtCore import QTimer
from ui_design import SerialUi


class SerialAssistant(SerialUi):
    def __init__(self):
        super().__init__()
        # 初始化serial对象 用于串口通信
        self.ser = serial.Serial()
        # 初始化串口配置文件
        self.serial_cfg()
        # 初始化串口 绑定槽
        self.unit_serial()

    # 初始化串口配置 定义串口设置信息 保存和读取
    def serial_cfg(self):
        self.cfg_serial_dic = {}  # 用于保存串口设置信息的字典
        self.cfg_command_dic = {}
        self.cfg_single_dic = {}
        self.current_path = os.path.dirname(os.path.realpath(__file__))  # 当前目录
        self.cfg_path = ''  # 配置文件的路径
        self.cfg_dir = 'settings'  # 配置文件目录
        self.cfg_file_name = 'cfg.ini'  # 配置文件名
        self.conf_parse = configparser.ConfigParser()  # 配置文件解析ConfigParser对象

        # 读取串口配置
        self.read_cfg()
        # 将读取到的串口配置信息显示到界面上
        self.display_cfg()

    # 读取串口配置————配置文件和section是否存在
    def read_cfg(self):
        self.cfg_path = os.path.join(self.current_path, self.cfg_dir, self.cfg_file_name)  # 获取配置文件路径 join用于连接两个或更多的路径
        # 判断读取配置文件是否正常 如果读取文件正常
        if self.conf_parse.read(self.cfg_path):
            # 判断读取section是否正常
            try:
                # 获取serial_setting section  返回一个配置字典
                serial_items = self.conf_parse.items('serial_setting')
                self.cfg_serial_dic = dict(serial_items)
                print(self.cfg_serial_dic)
            # 如果没有找到section
            except configparser.NoSectionError:
                self.conf_parse.add_section('serial_setting')  # 添加section
                self.conf_parse.write(open(self.cfg_path, 'w'))  # 保存到配置文件
            try:
                command_items = self.conf_parse.items('mul_sent_command')
                self.cfg_command_dic = dict(command_items)
                print(self.cfg_command_dic)
            except configparser.NoSectionError:
                self.conf_parse.add_section('mul_sent_command')
                self.conf_parse.write(open(self.cfg_path, 'w'))
            try:
                command_items = self.conf_parse.items('single_sent_command')
                self.cfg_single_dic = dict(command_items)
                print(self.cfg_single_dic)
            except configparser.NoSectionError:
                self.conf_parse.add_section('single_sent_command')
                self.conf_parse.write(open(self.cfg_path, 'w'))
        # 读取文件异常
        else:
            # 判断setting目录是否存在 不存在的话新建目录
            if not os.path.exists(os.path.join(self.current_path, self.cfg_dir)):
                os.mkdir(os.path.join(self.current_path, self.cfg_dir))
            self.conf_parse.add_section('serial_setting')  # 添加section
            self.conf_parse.set('serial_setting', 'baudrate', '')
            self.conf_parse.set('serial_setting', 'data', '')
            self.conf_parse.set('serial_setting', 'stopbits', '')
            self.conf_parse.set('serial_setting', 'parity', '')
            self.conf_parse.add_section('mul_sent_command')
            for i in range(1, 8):
                self.conf_parse.set('mul_sent_command', 'command_{}'.format(i), '')
            self.conf_parse.add_section('single_sent_command')
            self.conf_parse.set('single_sent_command', 'command', '')
            self.conf_parse.write(open(self.cfg_path, 'w'))  # 保存到配置文件

    # 保存串口配置信息
    def save_cfg(self):
        self.conf_parse.set('serial_setting', 'baudrate', str(self.ser.baudrate))
        self.conf_parse.set('serial_setting', 'data', str(self.ser.bytesize))
        self.conf_parse.set('serial_setting', 'stopbits', str(self.ser.stopbits))
        self.conf_parse.set('serial_setting', 'parity', self.ser.parity)

        for i in range(1, 8):
            self.conf_parse.set('mul_sent_command', 'command_{}'.format(i),
                                self.findChild(QLineEdit, 'mul_le_{}'.format(i)).text())

        self.conf_parse.set('single_sent_command', 'command', self.sins_te_send.toPlainText())
        self.conf_parse.write(open(self.cfg_path, 'w'))

    # 将读取到的串口配置信息显示到界面上
    def display_cfg(self):
        self.sset_cb_baud.setCurrentText(self.conf_parse.get('serial_setting', 'baudrate'))
        self.sset_cb_data.setCurrentText(self.conf_parse.get('serial_setting', 'data'))
        self.sset_cb_stop.setCurrentText(self.conf_parse.get('serial_setting', 'stopbits'))
        self.sset_cb_parity.setCurrentText(self.conf_parse.get('serial_setting', 'parity'))

        for i in range(1, 8):
            command = self.conf_parse.get('mul_sent_command', 'command_{}'.format(i))
            if command:
                self.findChild(QLineEdit, 'mul_le_{}'.format(i)).setText(command)

        self.sins_te_send.setText(self.conf_parse.get('single_sent_command', 'command'))

    # 初始化串口 给各个信号绑定槽
    def unit_serial(self):
        # 串口检测按钮
        self.sset_btn_detect.clicked.connect(self.port_detect)
        # 打开/关闭串口 按钮
        self.sset_btn_open.clicked.connect(self.port_open_close)
        # 更改窗口颜色下拉菜单
        self.sset_cb_color.currentTextChanged.connect(self.change_color)
        # 单行发送数据 按钮
        self.sins_btn_send.clicked.connect(self.single_send)
        # 清除接收按钮
        self.muls_btn_clear.clicked.connect(self.clear_receive)
        # 清除发送按钮
        self.sins_btn_clear.clicked.connect(self.clear_send)
        # 保存窗口
        self.sins_btn_save.clicked.connect(self.save_receive_to_file)

        # 循环发送数据——单条
        self.loop_single_send_timer = QTimer()
        self.loop_single_send_timer.timeout.connect(self.single_send)
        self.sins_cb_loop_send.stateChanged.connect(self.single_loop_send)

        # 多行发送数据 按钮
        for i in range(1, 8):
            self.child_button = self.findChild(QPushButton, 'mul_btn_{}'.format(i))
            self.child_button.clicked.connect(self.multi_send_general)

        # 循环发送数据——多条
        self.loop_mul_sent_timer = QTimer()
        self.loop_mul_sent_timer.timeout.connect(self.multi_send_special)
        self.mul_cb_loop_send.stateChanged.connect(self.mul_loop_send)

        # 定时器接受数据
        self.serial_receive_timer = QTimer(self)
        self.serial_receive_timer.timeout.connect(self.data_receive)

    # 串口检测
    def port_detect(self):
        # 检测所有存在的串口 将信息存在字典中
        self.port_dict = {}
        port_list = list(serial.tools.list_ports.comports())
        print(port_list)
        self.sset_cb_choose.clear()
        for port in port_list:
            self.port_dict["%s" % port[0]] = "%s" % port[1]
            self.sset_cb_choose.addItem(port[0] + '：' + port[1])
        if len(self.port_dict) == 0:
            self.sset_cb_choose.addItem('无串口')
        print(self.port_dict)
        self.sset_btn_open.setEnabled(True)

    # 获取端口号（串口选择界面想显示完全 但打开串口只需要串口号COMX）
    def get_port_name(self):
        full_name = self.sset_cb_choose.currentText()
        com_name = full_name[0:full_name.rfind('：')]
        return com_name

    # 打开/关闭 串口
    def port_open_close(self):
        if (self.sset_btn_open.text() == '打开串口') and self.port_dict:
            self.ser.port = self.get_port_name()  # 设置端口
            self.ser.baudrate = int(self.sset_cb_baud.currentText())  # 波特率
            self.ser.bytesize = int(self.sset_cb_data.currentText())  # 数据位
            self.ser.parity = self.sset_cb_parity.currentText()  # 校验位
            self.ser.stopbits = int(self.sset_cb_stop.currentText())  # 停止位
            try:
                self.ser.open()
            except serial.SerialException:
                QMessageBox.critical(self, 'Open Port Error', '此串口不能正常打开！')
                return None

            # 打开串口接收定时器 周期为2ms
            self.serial_receive_timer.start(2)

            if self.ser.isOpen():
                self.sset_btn_open.setText('关闭串口')
                self.sset_btn_open.setIcon(QIcon('close_button.png'))
                self.serial_state_gb.setTitle('串口状态（已开启）')
                self.set_setting_enable(False)

        elif (self.sset_btn_open.text() == '打开串口') and (self.sset_cb_choose.currentText() == '无串口'):
            QMessageBox.warning(self, 'Open Port Warning', '没有可打开的串口！')
            return None
        elif self.sset_btn_open.text() == '关闭串口':
            self.serial_receive_timer.stop()
            try:
                self.ser.close()
            except:
                QMessageBox.critical(self, 'Open Port Error', '此串口不能正常关闭！')
                return None
            self.sset_btn_open.setText('打开串口')
            self.sset_btn_open.setIcon(QIcon('open_button.png'))
            self.serial_state_gb.setTitle('串口状态')
            self.set_setting_enable(True)

            # 更改已发送和已接收标签
            self.sent_count_num = 0
            self.ssta_lb_sent.setText(str(self.sent_count_num))
            self.receive_count_num = 0
            self.ssta_lb_receive.setText(str(self.receive_count_num))

    # 改变窗口颜色
    def change_color(self):
        if self.sset_cb_color.currentText() == 'whiteblack':
            self.receive_log_view.setStyleSheet("QTextEdit {color:black;background-color:white}")
            # self.receive_log_view.setTextColor(QColor())
            # print('白底黑字')
        elif self.sset_cb_color.currentText() == 'blackwhite':
            self.receive_log_view.setStyleSheet("QTextEdit {color:white;background-color:black}")
            # print('黑底白字')
        elif self.sset_cb_color.currentText() == 'blackgreen':
            self.receive_log_view.setStyleSheet("QTextEdit {color:rgb(0,255,0);background-color:black}")
            self.receive_log_view.setTextColor(QColor('red'))
            # print('黑底绿字')

    # 设置 串口设置区 可用与禁用
    def set_setting_enable(self, enable):
        self.sset_cb_choose.setEnabled(enable)
        self.sset_cb_baud.setEnabled(enable)
        self.sset_cb_data.setEnabled(enable)
        self.sset_cb_parity.setEnabled(enable)
        self.sset_cb_stop.setEnabled(enable)

    # 发送
    def send_text(self, send_string):
        if self.ser.isOpen():
            # 非空字符串
            if send_string != '':
                # 如果勾选了HEX发送 则以HEX发送 String到Int再到Byte
                if self.sins_cb_hex_send.isChecked():
                    # 移除头尾的空格或换行符
                    send_string = send_string.strip()
                    sent_list = []
                    while send_string != '':
                        # 检查是否是16进制 如果不是则抛出异常
                        try:
                            num = int(send_string[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'Wrong Data', '请输入十六进制数据，以空格分开！')
                            self.sins_cb_hex_send.setChecked(False)
                            return None
                        else:
                            send_string = send_string[2:].strip()
                            # 将需要发送的字符串保存在sent_list里
                            sent_list.append(num)
                    # 转化为byte
                    single_sent_string = bytes(sent_list)
                # 否则ASCII发送
                else:
                    single_sent_string = (send_string + '\r\n').encode('utf-8')

                sent_num = self.ser.write(single_sent_string)
                self.sent_count_num += sent_num
                self.ssta_lb_sent.setText(str(self.sent_count_num))

        else:
            QMessageBox.warning(self, 'Port Warning', '没有可用的串口，请先打开串口！')
            return None

    # 单行发送
    def single_send(self):
        # 获取已输入的字符串
        single_sent_string = self.sins_te_send.toPlainText()
        self.send_text(single_sent_string)

    # 多行发送————普通 涉及sender 点击数字按钮发送对应的命令
    def multi_send_general(self):
        sent = self.sender().text()
        mul_te_sent = self.findChild(QLineEdit, 'mul_le_{}'.format(sent))
        multi_sent_string = mul_te_sent.text()
        # print('1' + multi_sent_string)
        self.send_text(multi_sent_string)

    # 多行发送————特殊 不用点击按钮 根据勾选发送
    def multi_send_special(self):
        self.send_list = self.get_mul_send_list()
        for string in self.send_list:
            self.send_text(string)

    # 循环发送——单条
    def single_loop_send(self):
        if self.sins_te_send.toPlainText():
            if self.ser.isOpen():
                if self.sins_cb_loop_send.isChecked():
                    if self.sins_le_loop_text.text():
                        self.loop_single_send_timer.start(int(self.sins_le_loop_text.text()))
                        self.sins_le_loop_text.setEnabled(False)
                        self.sset_btn_open.setEnabled(False)
                    else:
                        QMessageBox.warning(self, 'Value Error', '请输入1-1000000的值！')
                        self.sins_le_loop_text.setText('1000')
                        self.sins_cb_loop_send.setChecked(False)
                else:
                    self.loop_single_send_timer.stop()
                    self.sins_le_loop_text.setEnabled(True)
                    self.sset_btn_open.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Port Warning', '没有可用的串口，请先打开串口！')
                self.sins_cb_loop_send.setChecked(False)

    # 获取一个多条发送列表 里面包含所有打钩的命令
    def get_mul_send_list(self):
        self.mul_send_list = []
        for i in range(1, 8):
            mul_te_sent = self.findChild(QLineEdit, 'mul_le_{}'.format(i))
            multi_sent_string = mul_te_sent.text()
            mul_cb_check = self.findChild(QCheckBox, 'mul_cb_{}'.format(i))
            if multi_sent_string and mul_cb_check.isChecked():
                self.mul_send_list.append(multi_sent_string)
                # print(self.mul_send_list)
        return self.mul_send_list

    # 循环发送——多条
    def mul_loop_send(self):
        if self.ser.isOpen():
            if self.mul_cb_loop_send.isChecked():
                if self.mul_le_loop_text.text():
                    self.loop_mul_sent_timer.start(int(self.mul_le_loop_text.text()))
                    self.mul_le_loop_text.setEnabled(False)
                    self.sset_btn_open.setEnabled(False)
                else:
                    QMessageBox.warning(self, 'Value Error', '请输入1-1000000的值！')
                    self.mul_le_loop_text.setText('1000')
                    self.mul_cb_loop_send.setChecked(False)
            else:
                self.loop_mul_sent_timer.stop()
                self.mul_le_loop_text.setEnabled(True)
                self.sset_btn_open.setEnabled(True)
        else:
            QMessageBox.warning(self, 'Port Warning', '1没有可用的串口，请先打开串口！')
            self.mul_cb_loop_send.setChecked(False)

    # 接收数据
    def data_receive(self):
        try:
            # inWaiting()：返回接收缓存中的字节数
            num = self.ser.inWaiting()
        except:
            pass
        else:
            if num > 0:
                data = self.ser.read(num)
                receive_num = len(data)
                # HEX显示
                if self.sins_cb_hex_receive.isChecked():
                    receive_string = ''
                    for i in range(0, len(data)):
                        # {:X}16进制标准输出形式 02是2位对齐 左补0形式
                        receive_string = receive_string + '{:02X}'.format(data[i]) + ' '
                    self.receive_log_view.append(receive_string)
                    self.receive_log_view.moveCursor(QTextCursor.End)
                else:
                    self.receive_log_view.insertPlainText(data.decode(encoding='gbk', errors='replace'))
                    self.receive_log_view.moveCursor(QTextCursor.End)

                self.receive_count_num += receive_num
                self.ssta_lb_receive.setText(str(self.receive_count_num))
            else:
                pass

    # 清除发送
    def clear_send(self):
        self.sins_te_send.setText('')

    # 清除接收
    def clear_receive(self):
        self.receive_log_view.setText('')

    # 保存窗口
    def save_receive_to_file(self):
        file_name = QFileDialog.getSaveFileName(self, '保存窗口为txt文件','SaveWindow' +
                                                time.strftime('%Y_%m_%d_%H-%M-%S', time.localtime()) + '.txt')
        if file_name[1]:
            with open(file_name[0], 'w') as file:
                my_text = self.receive_log_view.toPlainText()
                file.write(my_text)
        else:
            pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "确定要退出吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if reply == QMessageBox.Yes:
            self.save_cfg()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    su = SerialAssistant()
    sys.exit(app.exec_())