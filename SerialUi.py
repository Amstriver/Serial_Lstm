from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import QWidget, QGridLayout, QDesktopWidget, QGroupBox, QFormLayout \
    , QPushButton, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QTextBrowser
from Throw_errs import Throw_errs
from qwt import QwtPlot, QwtLegend

class SerialUi(QWidget, Throw_errs):
    """_summary_

    Args:
        None
    """
    def __init__(self) -> None:
        super().__init__()

        self.__initUi()

    # 初始化UI界面
    def __initUi(self) -> None:
        grid_layout = QGridLayout()  # 设置网格布局3行3列
        # 添加组件
        grid_layout.addWidget(self.set_serial_setting_groupbox(), 0, 0)
        grid_layout.addWidget(self.set_serial_send(), 1, 0)
        grid_layout.addWidget(self.set_project_info(), 2, 0)
        grid_layout.addWidget(self.set_sensor_curve(), 0, 1)
        grid_layout.addWidget(self.set_operate_grid(), 1, 1)
        grid_layout.addWidget(self.set_serial_status(), 2, 1)
        grid_layout.addWidget(self.set_sensor_setting(), 0, 2)
        grid_layout.addWidget(self.set_check_status(), 1, 2)
        grid_layout.addWidget(self.set_now_time(), 2, 2)
        # 设置布局grid_layout
        self.setLayout(grid_layout)
        # 设置窗口大小
        self.resize(900, 500)
        # 设置窗口图标
        self.setWindowIcon(QIcon("./icon/window_gas.png"))
        # 窗口显示在中心
        self.__center()
        # 设置窗口名称
        self.setWindowTitle("智感微辨监测平台")
        # 显示
        self.show()

    def __center(self):
        """
            控制窗口显示在屏幕中心
        """
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showtime(self):
        """
            显示当前时间
        """
        time_display = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd')
        self.set_timer.setText(time_display)

    
    # 串口设置区
    def set_serial_setting_groupbox(self) -> QGroupBox:
        # 设置一个 串口设置 分组框
        serial_setting_gb = QGroupBox('串口设置')
        # 设置宽度高度
        # serial_setting_gb.setFixedSize(200, 280)
        # 创建 串口设置 分组框内的布局管理器
        serial_setting_formlayout = QFormLayout()
        
        # 检测串口 按钮  创建一个按钮
        self.set_btn_detect = QPushButton('检测串口')
        serial_setting_formlayout.addRow('串口选择  ', self.set_btn_detect)
        
        # 选择串口 下拉菜单  创建一个下拉列表
        self.set_cb_choose = QComboBox(serial_setting_gb)
        # 添加一个下拉列表 由于没有标签 直接省略即可
        serial_setting_formlayout.addRow(self.set_cb_choose)
        
        # 波特率 下拉菜单
        self.set_baud_rate = QComboBox(serial_setting_gb)
        self.set_baud_rate.addItems(['100', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
                            '38400', '56000', '57600', '115200', '128000', '256000']) 
        self.set_baud_rate.setCurrentText("115200")
        serial_setting_formlayout.addRow('波特率  ', self.set_baud_rate)
        
        # 停止位 下拉菜单
        self.set_stop_bit = QComboBox(serial_setting_gb)    
        self.set_stop_bit.addItems(['1', '1.5', '2'])
        serial_setting_formlayout.addRow('停止位  ', self.set_stop_bit)
        
        # 数据位 下拉菜单
        self.set_data_bit = QComboBox(serial_setting_gb)
        self.set_data_bit.addItems(['8', '7', '6', '5'])
        serial_setting_formlayout.addRow('数据位  ', self.set_data_bit)
        
        # 奇偶校验 下拉菜单
        self.set_odd_check = QComboBox(serial_setting_gb)
        self.set_odd_check.addItems(['N', 'O', 'E'])
        serial_setting_formlayout.addRow('校验位  ', self.set_odd_check)
        
        # 串口操作 按钮
        self.set_serial_operate = QPushButton('打开串口')
        self.set_serial_operate.setIcon(QIcon('./icon/serial_down.png'))
        self.set_serial_operate.setEnabled(False)  # 设置按钮可用
        serial_setting_formlayout.addRow('串口操作  ', self.set_serial_operate)

        # 串口日志 显示框
        self.receive_log_view = QTextBrowser()
        self.receive_log_view.setMinimumWidth(200)
        self.receive_log_view.append('串口日志')
        self.receive_log_view.append('')

        vbox = QVBoxLayout()
        vbox.addWidget(self.receive_log_view)
        serial_setting_formlayout.addRow(vbox)
        self.receive_log_view.setStyleSheet("QTextEdit {color:black;background-color:white}")

        # 设置控件的间隔距离
        serial_setting_formlayout.setSpacing(10)
        # 设置分组框的布局格式
        serial_setting_gb.setLayout(serial_setting_formlayout)
        
        return serial_setting_gb

    def set_serial_send(self) -> QGroupBox:
        # 设置传感器数据显示布局
        serial_send_gp = QGroupBox('显示调整')
        serial_send_vlayout = QVBoxLayout()
        serial_send_gridlayout = QGridLayout()
        # 最大值输入
        self.serial_send_maxlabel = QLabel('最大值')
        serial_send_gridlayout.addWidget(self.serial_send_maxlabel, 0, 0)

        self.serial_max_content = QLineEdit()
        # reg1 = QRegExp('^(?:[1-9][0-9]{0,2}|1000)$')  # 0-1000
        # reg1_validator = QRegExpValidator(reg1, self.serial_max_content)
        # self.serial_max_content.setValidator(reg1_validator)
        serial_send_gridlayout.addWidget(self.serial_max_content, 0, 1)

        self.serial_send_max = QPushButton('设置')
        serial_send_gridlayout.addWidget(self.serial_send_max, 0, 2)
        # 最小值输入
        self.serial_send_minlabel = QLabel('最小值')
        serial_send_gridlayout.addWidget(self.serial_send_minlabel, 1, 0)

        self.serial_min_content = QLineEdit()
        # reg2 = QRegExp('^(?:[1-9][0-9]{0,2}|1000)$')  # 0-1000
        # reg2_validator = QRegExpValidator(reg2, self.serial_min_content)
        # self.serial_min_content.setValidator(reg2_validator)
        serial_send_gridlayout.addWidget(self.serial_min_content, 1, 1)

        self.serial_send_min = QPushButton('设置')
        serial_send_gridlayout.addWidget(self.serial_send_min, 1, 2)

        # 比较大小
        # self.serial_send_max.clicked.connect(lambda: self.validate_serial_range(self.serial_max_content, self.serial_min_content))
        # self.serial_send_min.clicked.connect(lambda: self.validate_serial_range(self.serial_max_content, self.serial_min_content))

        # 时间范围
        self.serial_send_timelabel = QLabel('时间范围')
        serial_send_gridlayout.addWidget(self.serial_send_timelabel, 2, 0)

        self.serial_time_content = QLineEdit()
        serial_send_gridlayout.addWidget(self.serial_time_content, 2, 1)

        self.serial_send_time = QPushButton('设置')
        serial_send_gridlayout.addWidget(self.serial_send_time, 2, 2)

        self.sins_cb_hex_receive = QCheckBox('HEX接收')
        self.sins_cb_hex_send = QCheckBox('HEX发送')
        self.clear_data_view = QPushButton('清空')
        serial_send_gridlayout.addWidget(self.sins_cb_hex_receive, 3, 0)
        serial_send_gridlayout.addWidget(self.sins_cb_hex_send, 3, 1)
        serial_send_gridlayout.addWidget(self.clear_data_view, 3, 2)

        serial_send_gridlayout.setSpacing(15)
        serial_send_vlayout.addLayout(serial_send_gridlayout)
        serial_send_gp.setLayout(serial_send_vlayout)
        # serial_send_gp.setFixedWidth(250)  # 设置固定宽度

        return serial_send_gp
    
    def set_project_info(self) -> QGroupBox:
        # 设置项目信息
        project_info_gp = QGroupBox()
        project_info_hlayout = QHBoxLayout()
        project_info_gridlayout = QGridLayout()

        self.icon_label = QLabel()
        self.icon = QIcon('./icon/author.png')
        self.icon_label.setPixmap(self.icon.pixmap(20, 20))

        self.project_author = QLabel('Author: XiaoShuai')
        self.project_version = QLabel('Version: 2.0.0')

        project_info_gridlayout.addWidget(self.icon_label, 0, 0)
        project_info_gridlayout.addWidget(self.project_author, 0, 1)
        project_info_gridlayout.addWidget(self.project_version, 0, 2)
        project_info_gridlayout.setSpacing(10)  # 设置网格布局的间距

        project_info_hlayout.addLayout(project_info_gridlayout)
        project_info_gp.setLayout(project_info_hlayout)

        return project_info_gp
        
    def set_sensor_setting(self) -> QGroupBox:
        # 设置传感器设置
        sensor_setting_gp = QGroupBox('传感器设置')
        sensor_setting_vlayout = QVBoxLayout()
        sensor_setting_gridlayout = QGridLayout()

        # for i in range(1, 9):
        #     sensor_checkbox = QCheckBox(f'Sensor {i}')
        #     sensor_edit = QLineEdit()
        #     sensor_edit.setText('0')

        #     sensor_setting_gridlayout.addWidget(sensor_checkbox, i - 1, 0)   
        #     sensor_setting_gridlayout.addWidget(sensor_edit, i - 1, 1)
        # 修改了布局，方便调用
        self.sensor_check1 = QCheckBox('Sensor 1')
        self.sensor_editone = QLineEdit()
        sensor_setting_gridlayout.addWidget(self.sensor_check1, 0, 0)   
        sensor_setting_gridlayout.addWidget(self.sensor_editone, 0, 1)

        self.sensor_check2 = QCheckBox('Sensor 2')
        self.sensor_edittwo = QLineEdit()
        sensor_setting_gridlayout.addWidget(self.sensor_check2, 1, 0)
        sensor_setting_gridlayout.addWidget(self.sensor_edittwo, 1, 1)

        self.sensor_check3 = QCheckBox('Sensor 3')
        self.sensor_editthree = QLineEdit()
        sensor_setting_gridlayout.addWidget(self.sensor_check3, 2, 0)
        sensor_setting_gridlayout.addWidget(self.sensor_editthree, 2, 1)

        self.sensor_check4 = QCheckBox('Sensor 4')
        self.sensor_editfour = QLineEdit()
        sensor_setting_gridlayout.addWidget(self.sensor_check4, 3, 0)
        sensor_setting_gridlayout.addWidget(self.sensor_editfour, 3, 1)

        self.sensor_check5 = QCheckBox('Sensor 5')
        self.sensor_editfive = QLineEdit()
        sensor_setting_gridlayout.addWidget(self.sensor_check5, 4, 0)
        sensor_setting_gridlayout.addWidget(self.sensor_editfive, 4, 1)

        self.sensor_check6 = QCheckBox('Sensor 6')
        self.sensor_editsix = QLineEdit()
        sensor_setting_gridlayout.addWidget(self.sensor_check6, 5, 0)
        sensor_setting_gridlayout.addWidget(self.sensor_editsix, 5, 1)

        self.sensor_check7 = QCheckBox('Sensor 7')
        self.sensor_editseven = QLineEdit()
        sensor_setting_gridlayout.addWidget(self.sensor_check7, 6, 0)
        sensor_setting_gridlayout.addWidget(self.sensor_editseven, 6, 1)

        self.sensor_check8 = QCheckBox('Sensor 8')
        self.sensor_editeight = QLineEdit()
        sensor_setting_gridlayout.addWidget(self.sensor_check8, 7, 0)
        sensor_setting_gridlayout.addWidget(self.sensor_editeight, 7, 1)
        
        self.sensor_check_all = QCheckBox('All')
        sensor_setting_gridlayout.addWidget(self.sensor_check_all, 8, 0)

        sensor_setting_vlayout.addLayout(sensor_setting_gridlayout)
        sensor_setting_vlayout.setSpacing(12)  # 设置网格布局的间距
        sensor_setting_gp.setLayout(sensor_setting_vlayout)

        return sensor_setting_gp
    
    def set_check_status(self) -> QGroupBox:
        # 设置查看信息一栏
        check_status_gp = QGroupBox('传感器状态')
        check_status_vlayout = QVBoxLayout()
        check_status_gridlayout = QGridLayout()
        # 查看传感器状态
        self.check_gasLabel = QLineEdit()
        check_status_gridlayout.addWidget(self.check_gasLabel, 0, 0)
        self.symbol_gasLabel = QLabel('气体')
        check_status_gridlayout.addWidget(self.symbol_gasLabel, 0, 1)
        self.check_gasLabel_button = QPushButton('查看')
        check_status_gridlayout.addWidget(self.check_gasLabel_button, 0, 2)
        # 传感器温度查看一栏
        self.check_temperature_value = QLineEdit()
        check_status_gridlayout.addWidget(self.check_temperature_value, 1, 0)
        self.symbol_temperature = QLabel('℃')
        check_status_gridlayout.addWidget(self.symbol_temperature, 1, 1)
        self.check_button_tem = QPushButton('查看')
        check_status_gridlayout.addWidget(self.check_button_tem, 1, 2)
        # 传感器湿度查看一栏
        self.check_humidity_value = QLineEdit()
        check_status_gridlayout.addWidget(self.check_humidity_value, 2, 0)
        self.symbol_humidity = QLabel('%')
        check_status_gridlayout.addWidget(self.symbol_humidity, 2, 1)
        self.check_button_hum = QPushButton('查看')
        check_status_gridlayout.addWidget(self.check_button_hum, 2, 2)

        self.clear_send_data = QPushButton('清空发送数据')
        check_status_gridlayout.addWidget(self.clear_send_data, 3, 0, 1, 3)

        check_status_vlayout.addLayout(check_status_gridlayout)
        check_status_vlayout.setSpacing(10)  # 设置网格布局的间距
        check_status_gp.setLayout(check_status_vlayout)
        
        return check_status_gp

    def set_now_time(self) -> QGroupBox:
        # 当前时间查看一栏
        now_time_gp = QGroupBox()
        now_time_formlayout = QFormLayout()
        # 当前时间 标签
        self.set_timer = QLabel(self)
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()
        now_time_formlayout.addRow(self.set_timer)

        now_time_gp.setLayout(now_time_formlayout)
        
        return now_time_gp

    def set_operate_grid(self) -> QGroupBox:
        # 操作一栏
        operate_gp = QGroupBox('操作栏')
        operate_gridlayout = QGridLayout()
        # 操作按钮
        self.open_collect_button = QPushButton('开始采集')
        operate_gridlayout.addWidget(self.open_collect_button, 0, 0)
        # 设置按钮的长宽
        self.open_collect_button.setFixedSize(100, 65)

        self.close_collect_button = QPushButton('停止采集')
        operate_gridlayout.addWidget(self.close_collect_button, 0, 1)
        self.close_collect_button.setFixedSize(100, 65)

        self.clear_data_button = QPushButton('清空数据')
        operate_gridlayout.addWidget(self.clear_data_button, 0, 2)
        self.clear_data_button.setFixedSize(100, 65)

        self.save_data_button = QPushButton('保存数据')
        operate_gridlayout.addWidget(self.save_data_button, 0, 3)
        self.save_data_button.setFixedSize(100, 65)

        operate_gp.setLayout(operate_gridlayout)

        return operate_gp

    def set_serial_status(self) -> QGroupBox:
        # 状态一栏
        status_gp = QGroupBox()
        status_layout = QHBoxLayout()  # 垂直布局，用于包含两个水平布局  
    
        # 已发送 一行  
        sent_hbox = QHBoxLayout()  # 水平布局  
        self.sent_count_num = 0  
        self.serial_send_label = QLabel("已发送：")  
        self.serial_send = QLabel(str(self.sent_count_num))  
        sent_hbox.addWidget(self.serial_send_label)  
        sent_hbox.addWidget(self.serial_send)  
        sent_hbox.addStretch()  # 可选，用于添加一些空白间距  
    
        # 已接收 一行  
        receive_hbox = QHBoxLayout()  # 另一个水平布局  
        self.receive_count_num = 0  
        self.serial_receive_label = QLabel("已接收：")  
        self.serial_receive = QLabel(str(self.receive_count_num))  
        receive_hbox.addWidget(self.serial_receive_label)  
        receive_hbox.addWidget(self.serial_receive)  
        receive_hbox.addStretch()  # 可选，用于添加一些空白间距  
    
        # 将两个水平布局添加到垂直布局中  
        status_layout.addLayout(sent_hbox)  
        status_layout.addLayout(receive_hbox)  
    
        status_gp.setLayout(status_layout)  # 设置组框的布局 

        return status_gp

    def set_sensor_curve(self) -> QGroupBox:
        # 传感器实时曲线
        sensor_curve_gp = QGroupBox()
        sensor_curve_formlayout = QGridLayout()

        self.sensor_curve = QwtPlot()
        self.sensor_curve.setMinimumSize(600, 320)
        self.sensor_curve.setFont(QFont("Times New Roman"))
        self.sensor_curve.setTitle("传感器实时曲线")
        self.sensor_curve.setAxisTitle(QwtPlot.xBottom, "Time/s")
        self.sensor_curve.setAxisFont(QwtPlot.xBottom, QFont("Times New Roman", 10))
        self.sensor_curve.setAxisTitle(QwtPlot.yLeft, "Value/KΩ")
        self.sensor_curve.setAxisFont(QwtPlot.yLeft, QFont("Times New Roman", 10))
        self.sensor_curve.insertLegend(QwtLegend(), QwtPlot.BottomLegend)
        
        sensor_curve_formlayout.addWidget(self.sensor_curve, 0, 0)
        sensor_curve_gp.setLayout(sensor_curve_formlayout)
        
        return sensor_curve_gp