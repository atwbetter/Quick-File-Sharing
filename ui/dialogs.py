"""
自定义对话框组件
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QListWidget, QListWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from utils.helpers import format_file_size, format_duration
from utils.logger import get_logger

logger = get_logger("dialogs")


class TransferProgressDialog(QDialog):
    """传输进度对话框"""
    
    def __init__(self, parent=None, transfer_info=None):
        """
        初始化进度对话框
        
        Args:
            parent: 父窗口
            transfer_info: 传输信息
        """
        super().__init__(parent)
        self.transfer_info = transfer_info or {}
        self.start_time = None
        
        self.setWindowTitle("文件传输")
        self.setGeometry(100, 100, 500, 300)
        self.setModal(True)
        
        self._create_ui()
        self._setup_timer()
    
    def _create_ui(self):
        """创建UI"""
        layout = QVBoxLayout(self)
        
        # 文件信息
        file_info = self.transfer_info.get("file_name", "Unknown")
        file_size = self.transfer_info.get("file_size", 0)
        
        info_label = QLabel(f"传输文件：{file_info} ({format_file_size(file_size)})")
        layout.addWidget(info_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("准备中...")
        layout.addWidget(self.status_label)
        
        # 速度和剩余时间
        self.speed_label = QLabel("速度：0 B/s | 剩余时间：--")
        layout.addWidget(self.speed_label)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.pause_btn = QPushButton("暂停")
        self.pause_btn.clicked.connect(self._on_pause)
        button_layout.addWidget(self.pause_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _setup_timer(self):
        """设置定时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_display)
    
    def update_progress(self, progress: float, bytes_transferred: int = 0,
                       total_bytes: int = 0):
        """更新进度"""
        self.progress_bar.setValue(int(progress))
        self.status_label.setText(f"正在传输... {int(progress)}%")
    
    def _update_display(self):
        """更新显示"""
        pass
    
    def _on_pause(self):
        """暂停按钮"""
        logger.info("Transfer paused")
    
    def _on_cancel(self):
        """取消按钮"""
        logger.info("Transfer cancelled")
        self.reject()


class DeviceSelectDialog(QDialog):
    """设备选择对话框"""
    
    def __init__(self, parent=None, devices=None):
        """
        初始化设备选择对话框
        
        Args:
            parent: 父窗口
            devices: 设备列表
        """
        super().__init__(parent)
        self.devices = devices or []
        self.selected_device = None
        
        self.setWindowTitle("选择目标设备")
        self.setGeometry(100, 100, 400, 300)
        self.setModal(True)
        
        self._create_ui()
    
    def _create_ui(self):
        """创建UI"""
        layout = QVBoxLayout(self)
        
        label = QLabel("选择要发送文件的设备：")
        layout.addWidget(label)
        
        # 设备列表
        self.device_list = QListWidget()
        self.device_list.itemClicked.connect(self._on_device_selected)
        
        for device in self.devices:
            device_name = device.get("device_name", "Unknown")
            device_type = device.get("device_type", "")
            transport = device.get("transport_mode", "")
            
            item_text = f"{device_name} ({transport})" if transport else device_name
            item = QListWidgetItem(item_text)
            item.setData(256, device)  # 存储设备信息
            self.device_list.addItem(item)
        
        layout.addWidget(self.device_list)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self._on_ok)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _on_device_selected(self, item: QListWidgetItem):
        """设备被选中"""
        self.selected_device = item.data(256)
    
    def _on_ok(self):
        """确定按钮"""
        if self.selected_device:
            self.accept()
        else:
            QMessageBox.warning(self, "提示", "请选择一个设备")
    
    def get_selected_device(self):
        """获取选中的设备"""
        return self.selected_device


class ReceiveDialog(QDialog):
    """接收确认对话框"""
    
    def __init__(self, parent=None, transfer_info=None):
        """
        初始化接收确认对话框
        
        Args:
            parent: 父窗口
            transfer_info: 传输信息
        """
        super().__init__(parent)
        self.transfer_info = transfer_info or {}
        
        self.setWindowTitle("接收文件")
        self.setGeometry(100, 100, 400, 250)
        self.setModal(True)
        
        self._create_ui()
    
    def _create_ui(self):
        """创建UI"""
        layout = QVBoxLayout(self)
        
        # 来源设备
        from_device = self.transfer_info.get("from_device", "Unknown Device")
        from_label = QLabel(f"来自设备：{from_device}")
        layout.addWidget(from_label)
        
        # 文件列表
        files_label = QLabel("接收的文件：")
        layout.addWidget(files_label)
        
        file_list = QListWidget()
        files = self.transfer_info.get("files", [])
        total_size = 0
        
        for file_info in files:
            file_name = file_info.get("file_name", "Unknown")
            file_size = file_info.get("file_size", 0)
            item = QListWidgetItem(f"{file_name} ({format_file_size(file_size)})")
            file_list.addItem(item)
            total_size += file_size
        
        layout.addWidget(file_list)
        
        # 总大小
        total_label = QLabel(f"总大小：{format_file_size(total_size)}")
        layout.addWidget(total_label)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        accept_btn = QPushButton("接受")
        accept_btn.clicked.connect(self.accept)
        button_layout.addWidget(accept_btn)
        
        decline_btn = QPushButton("拒绝")
        decline_btn.clicked.connect(self.reject)
        button_layout.addWidget(decline_btn)
        
        layout.addLayout(button_layout)
