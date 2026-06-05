"""
设备管理服务 - 管理已连接的设备
"""
import asyncio
from typing import Dict, Optional, List
import config
from utils.logger import get_logger

logger = get_logger("device_manager")


class Device:
    """设备类"""
    
    def __init__(self, device_id: str, device_name: str, device_type: str,
                 transport_mode: str):
        """
        初始化设备
        
        Args:
            device_id: 设备ID
            device_name: 设备名称
            device_type: 设备类型
            transport_mode: 传输模式
        """
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type
        self.transport_mode = transport_mode
        self.is_connected = False
        self.last_seen = None
        self.metadata = {}


class DeviceManager:
    """设备管理器"""
    
    def __init__(self):
        """初始化设备管理器"""
        self.devices: Dict[str, Device] = {}
        self.connection_handlers: Dict[str, object] = {}
    
    def add_device(self, device_id: str, device_name: str, device_type: str,
                   transport_mode: str) -> Device:
        """添加设备"""
        if device_id not in self.devices:
            device = Device(device_id, device_name, device_type, transport_mode)
            self.devices[device_id] = device
            logger.info(f"Device added: {device_name} ({device_id})")
            return device
        return self.devices[device_id]
    
    def remove_device(self, device_id: str) -> bool:
        """移除设备"""
        if device_id in self.devices:
            device = self.devices.pop(device_id)
            if device_id in self.connection_handlers:
                del self.connection_handlers[device_id]
            logger.info(f"Device removed: {device.device_name} ({device_id})")
            return True
        return False
    
    def get_device(self, device_id: str) -> Optional[Device]:
        """获取设备"""
        return self.devices.get(device_id)
    
    def get_all_devices(self) -> List[Device]:
        """获取所有设备"""
        return list(self.devices.values())
    
    def get_connected_devices(self) -> List[Device]:
        """获取已连接的设备"""
        return [d for d in self.devices.values() if d.is_connected]
    
    async def connect_device(self, device_id: str) -> bool:
        """连接设备"""
        device = self.get_device(device_id)
        if not device:
            logger.error(f"Device not found: {device_id}")
            return False
        
        try:
            logger.info(f"Connecting to device: {device.device_name}")
            
            # TODO: 实现具体的连接逻辑
            device.is_connected = True
            logger.info(f"Connected to device: {device.device_name}")
            return True
        
        except Exception as e:
            logger.error(f"Error connecting to device: {e}")
            return False
    
    async def disconnect_device(self, device_id: str) -> bool:
        """断开设备连接"""
        device = self.get_device(device_id)
        if not device:
            logger.error(f"Device not found: {device_id}")
            return False
        
        try:
            logger.info(f"Disconnecting from device: {device.device_name}")
            
            # TODO: 实现具体的断开连接逻辑
            device.is_connected = False
            logger.info(f"Disconnected from device: {device.device_name}")
            return True
        
        except Exception as e:
            logger.error(f"Error disconnecting from device: {e}")
            return False
    
    def update_device_metadata(self, device_id: str, metadata: Dict) -> bool:
        """更新设备元数据"""
        device = self.get_device(device_id)
        if device:
            device.metadata.update(metadata)
            return True
        return False
