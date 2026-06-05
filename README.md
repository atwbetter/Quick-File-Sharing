# Quick File Sharing

快速优雅的文件共享工具 - 类似华为 Huawei Share 功能

## 功能特点

✨ **核心功能**
- 📱 手机和电脑快速共享文件
- 🔄 支持WiFi和蓝牙双通道传输
- 📦 支持大文件传输 (2GB-5GB+)
- 🎯 无需复杂配置，开箱即用
- 🚀 高速传输，断点续传

## 系统要求

- Python 3.8+
- Windows 10/11 或 macOS
- 支持蓝牙和WiFi的设备

## 依赖项

```
PySide6>=6.0.0
PyBluez>=0.22  # 蓝牙支持（需要系统蓝牙驱动）
zeroconf>=0.50.0  # mDNS/DNS-SD 本地服务发现
asyncio-based networking
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

```bash
python main.py
```

## 项目架构

```
Quick-File-Sharing/
├── main.py                      # 应用入口
├── requirements.txt             # 依赖列表
├── config.py                    # 配置文件
├── ui/
│   ├── __init__.py
│   ├── main_window.py          # 主窗口UI
│   ├── styles.py               # UI样式
├── core/
│   ├── __init__.py
│   ├── network.py              # 网络通信核心
│   ├── bluetooth.py            # 蓝牙模块
│   ├── wifi.py                 # WiFi传输模块
│   ├── file_handler.py         # 文件处理
│   └── discovery.py            # 设备发现
├── services/
│   ├── __init__.py
│   ├── file_service.py         # 文件服务
│   ├── transfer_manager.py     # 传输管理
│   └── device_manager.py       # 设备管理
└── utils/
    ├── __init__.py
    ├── logger.py               # 日志工具
    ├── constants.py            # 常量定义
    └── helpers.py              # 辅助函数
```

## 使用说明

### 发送文件
1. 点击"选择文件"按钮
2. 选择要发送的文件
3. 选择目标设备
4. 点击"发送"开始传输

### 接收文件
1. 应用将自动监听传入文件
2. 收到传输请求时会弹出提示
3. 确认后文件将保存到默认路径

## 功能开发进度

- [x] 基础UI框架
- [x] WiFi本地发现 (mDNS)
- [x] 蓝牙设备发现框架
- [ ] 完整的蓝牙连接实现
- [ ] 文件传输引擎核心
- [ ] 断点续传
- [ ] 传输加密
- [ ] 设备管理界面优化
- [ ] 传输历史记录

## 开发者指南

### 蓝牙支持
- Windows: 需要安装 PyBluez (需要 BlueZ 或 WinRT)
- Linux: 使用 BlueZ
- macOS: 使用 IOBluetooth

### 编译成EXE
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**开发者**: atwbetter  
**最后更新**: 2026-06-05
