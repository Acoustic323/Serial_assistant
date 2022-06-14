import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QGroupBox,
                             QGridLayout, QTextBrowser, QVBoxLayout, QFormLayout,
                             QLabel, QPushButton, QComboBox, QCheckBox, QTextEdit,
                             QLineEdit, QHBoxLayout)
from PyQt5.QtCore import QDateTime, QTimer, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator


class SerialUi(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化UI
        self.unit_ui()

    # 初始化UI
    def unit_ui(self):
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.set_serial_setting_groupbox(), 0, 0)
        grid_layout.addWidget(self.set_serial_state_groupbox(), 1, 0)
        grid_layout.addWidget(self.set_receive_groupbox(), 0, 1)
        grid_layout.addWidget(self.set_mul_sent_groupbpx(), 0, 2)
        grid_layout.addWidget(self.set_single_sent_groupbox(), 1, 1, 1, 2)
        self.setLayout(grid_layout)
        self.resize(760, 420)
        self.setWindowIcon(QIcon('title_icon.png'))
        self.center()
        self.setWindowTitle('串口助手')
        # self.setFixedSize(760, 450)
        self.show()

    # 串口设置 区
    def set_serial_setting_groupbox(self):
        # 设置一个 串口设置 分组框
        serial_setting_gb = QGroupBox('串口设置')
        # 创建 串口设置 分组框内的布局管理器
        serial_setting_formlayout = QFormLayout()

        # 检测串口 按钮
        self.sset_btn_detect = QPushButton('检测串口')
        serial_setting_formlayout.addRow('串口选择：', self.sset_btn_detect)

        # 选择串口 下拉菜单
        self.sset_cb_choose = QComboBox(serial_setting_gb)
        serial_setting_formlayout.addRow(self.sset_cb_choose)

        # 波特率 下拉菜单
        self.sset_cb_baud = QComboBox(serial_setting_gb)
        self.sset_cb_baud.addItems(['100', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
                          '38400', '56000', '57600', '115200', '128000', '256000'])
        # self.sset_cb_baud.setCurrentIndex(12)
        serial_setting_formlayout.addRow('波特率：', self.sset_cb_baud)

        # 数据位 下拉菜单
        self.sset_cb_data = QComboBox(serial_setting_gb)
        self.sset_cb_data.addItems(['8', '7', '6', '5'])
        # self.sset_cb_data.setCurrentIndex(0)
        serial_setting_formlayout.addRow('数据位：', self.sset_cb_data)

        # 校验位 下拉菜单
        self.sset_cb_parity = QComboBox(serial_setting_gb)
        self.sset_cb_parity.addItems(['N', 'E', 'O'])  # 校验位N－无校验，E－偶校验，O－奇校验
        # self.sset_cb_check.setCurrentIndex(0)
        serial_setting_formlayout.addRow('校验位：', self.sset_cb_parity)

        # 停止位 下拉菜单
        self.sset_cb_stop = QComboBox(serial_setting_gb)
        self.sset_cb_stop.addItems(['1', '1.5', '2'])
        # self.sset_cb_stop.setCurrentIndex(0)
        serial_setting_formlayout.addRow('停止位：', self.sset_cb_stop)

        # 窗口配色 下拉菜单
        self.sset_cb_color = QComboBox(serial_setting_gb)
        self.sset_cb_color.addItems(['whiteblack', 'blackwhite', 'blackgreen'])
        # self.sset_cb_color.setCurrentIndex(0)
        serial_setting_formlayout.addRow('窗口配色：', self.sset_cb_color)

        # 打开串口 按钮
        self.sset_btn_open = QPushButton('打开串口')
        self.sset_btn_open.setIcon(QIcon('open_button.png'))
        self.sset_btn_open.setEnabled(False)
        serial_setting_formlayout.addRow(self.sset_btn_open)

        serial_setting_formlayout.setSpacing(11)

        serial_setting_gb.setLayout(serial_setting_formlayout)
        return serial_setting_gb

    # 串口状态区
    def set_serial_state_groupbox(self):
        self.serial_state_gb = QGroupBox('串口状态', self)
        serial_state_formlayout = QFormLayout()

        # 已发送 标签
        self.sent_count_num = 0
        self.ssta_lb_sent = QLabel(str(self.sent_count_num))
        serial_state_formlayout.addRow('已发送：', self.ssta_lb_sent)

        # 已接收 标签
        self.receive_count_num = 0
        self.ssta_lb_receive = QLabel(str(self.receive_count_num))
        serial_state_formlayout.addRow('已接收：', self.ssta_lb_receive)

        # 当前时间 标签
        self.ssta_lb_timer = QLabel(self)
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()
        serial_state_formlayout.addRow(self.ssta_lb_timer)

        # 版本标签
        ssta_lb_version = QLabel('version：V1.0.0')
        serial_state_formlayout.addRow(ssta_lb_version)
        ssta_lb_coder = QLabel('author：wong')
        serial_state_formlayout.addRow(ssta_lb_coder)

        serial_state_formlayout.setSpacing(13)
        self.serial_state_gb.setLayout(serial_state_formlayout)
        return self.serial_state_gb

    def showtime(self):
        time_display = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd')
        self.ssta_lb_timer.setText(time_display)

    # 接收区
    def set_receive_groupbox(self):
        # 设置一个接收区分组框
        receive_gb = QGroupBox('接收区', self)
        # 添加显示接收日志的文本框
        self.receive_log_view = QTextBrowser(receive_gb)
        self.receive_log_view.setMinimumWidth(350)
        self.receive_log_view.append('Hello，欢迎使用串口助手！\n')
        # 设置布局并添加文本框
        vbox = QVBoxLayout()
        vbox.addWidget(self.receive_log_view)
        # 设置接收区分组框的布局
        receive_gb.setLayout(vbox)
        # receive_gb.setFixedWidth(300)
        return receive_gb

    # 单条发送区
    def set_single_sent_groupbox(self):
        single_sent_gb = QGroupBox('单条发送', self)
        sins_overall_hlayout = QHBoxLayout(single_sent_gb)
        vlayout_1 = QVBoxLayout()
        glayout_1 = QGridLayout()

        # 单行命令 文本框
        self.sins_te_send = QTextEdit()
        self.sins_te_send.setMinimumWidth(350)
        vlayout_1.addWidget(self.sins_te_send)

        # 循环发送 HEX发送 HEX接收 复选框
        self.sins_cb_loop_send = QCheckBox('循环发送')
        self.sins_le_loop_text = QLineEdit('1000')
        reg = QRegExp('^(?!0)(?:[0-9]{1,6}|1000000)$')  # ^(?!0)(?:[0-9]{1,4}|10000)$
        reg_validator = QRegExpValidator(reg)
        self.sins_le_loop_text.setValidator(reg_validator)
        sins_lb_loop_label = QLabel('ms/次')
        self.sins_cb_hex_receive = QCheckBox('HEX接收')
        self.sins_cb_hex_send = QCheckBox('HEX发送')

        glayout_1.addWidget(self.sins_cb_loop_send, 0, 0)
        glayout_1.addWidget(self.sins_le_loop_text, 0, 1)
        glayout_1.addWidget(sins_lb_loop_label, 0, 2)
        glayout_1.addWidget(self.sins_cb_hex_receive, 1, 0)
        glayout_1.addWidget(self.sins_cb_hex_send, 2, 0)

        # 保存窗口 清除发送 发送 按钮
        self.sins_btn_save = QPushButton('保存窗口')
        self.sins_btn_clear = QPushButton('清除发送')
        self.sins_btn_send = QPushButton('发送')
        glayout_1.addWidget(self.sins_btn_save, 1, 1, 1, 2)
        glayout_1.addWidget(self.sins_btn_clear, 2, 1, 1, 2)
        glayout_1.addWidget(self.sins_btn_send, 3, 0, 1, 3)

        sins_overall_hlayout.addLayout(vlayout_1)
        sins_overall_hlayout.addLayout(glayout_1)
        single_sent_gb.setLayout(sins_overall_hlayout)

        return single_sent_gb

    # 多条发送区
    def set_mul_sent_groupbpx(self):
        mul_send_gb = QGroupBox('多条发送', self)
        mul_send_vlayout = QVBoxLayout()
        mul_send_gridlayout1 = QGridLayout()
        mul_send_gridlayout2 = QGridLayout()

        # 清除接收 按钮
        self.muls_btn_clear = QPushButton('清除接收')
        mul_send_gridlayout1.addWidget(self.muls_btn_clear, 0, 0, 1, 3)

        # 多条循环发送
        self.mul_cb_loop_send = QCheckBox('多条循环')
        mul_send_gridlayout1.addWidget(self.mul_cb_loop_send, 1, 0)
        self.mul_le_loop_text = QLineEdit('1000')
        reg = QRegExp('^(?!0)(?:[0-9]{1,6}|1000000)$')  # ^(?!0)(?:[0-9]{1,4}|10000)$
        reg_validator = QRegExpValidator(reg)
        self.mul_le_loop_text.setValidator(reg_validator)
        mul_send_gridlayout1.addWidget(self.mul_le_loop_text, 1, 1)
        self.mul_lb_loop_lable = QLabel('ms/次')
        mul_send_gridlayout1.addWidget(self.mul_lb_loop_lable, 1, 2)

        # 多条发送 区域
        self.mul_btn_list = []
        for i in range(1, 8):
            for j in range(3):
                if j == 0:
                    self.checkbox = QCheckBox()
                    self.checkbox.setObjectName('mul_cb_{}'.format(i))
                    mul_send_gridlayout2.addWidget(self.checkbox, i, j)
                elif j == 1:
                    self.textedit = QLineEdit()
                    self.textedit.setObjectName('mul_le_{}'.format(i))
                    # print(self.textedit.objectName())
                    mul_send_gridlayout2.addWidget(self.textedit, i, j)
                else:
                    self.button = QPushButton(str(i))
                    self.button.setFixedSize(25, 22)
                    self.button.setObjectName('mul_btn_{}'.format(i))
                    self.mul_btn_list.append(self.button.objectName())
                    # print(self.mul_btn_list)
                    mul_send_gridlayout2.addWidget(self.button, i, j)

        mul_send_vlayout.addLayout(mul_send_gridlayout1)
        mul_send_vlayout.addLayout(mul_send_gridlayout2)
        mul_send_gb.setLayout(mul_send_vlayout)
        mul_send_gb.setFixedWidth(180)
        return mul_send_gb

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())