"""
系统信息获取模块
"""
import platform
import psutil
from pathlib import Path
from utils.logger import get_logger

logger = get_logger("system_info")


class SystemInfo:
    """系统信息类"""
    
    @staticmethod
    def get_cpu_info() -> dict:
        """获取CPU信息"""
        try:
            return {
                "cpu_count": psutil.cpu_count(logical=False),
                "cpu_logical_count": psutil.cpu_count(logical=True),
                "cpu_percent": psutil.cpu_percent(interval=1),
            }
        except Exception as e:
            logger.error(f"Error getting CPU info: {e}")
            return {}
    
    @staticmethod
    def get_memory_info() -> dict:
        """获取内存信息"""
        try:
            mem = psutil.virtual_memory()
            return {
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent,
            }
        except Exception as e:
            logger.error(f"Error getting memory info: {e}")
            return {}
    
    @staticmethod
    def get_disk_info(path: str = "/") -> dict:
        """获取磁盘信息"""
        try:
            disk = psutil.disk_usage(path)
            return {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            }
        except Exception as e:
            logger.error(f"Error getting disk info: {e}")
            return {}
    
    @staticmethod
    def get_network_info() -> dict:
        """获取网络信息"""
        try:
            net = psutil.net_if_stats()
            return {
                "interfaces": list(net.keys()),
                "is_up": any(v.isup for v in net.values()),
            }
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {}
    
    @staticmethod
    def get_storage_available(path: str = None) -> int:
        """获取可用存储空间"""
        try:
            if not path:
                path = str(Path.home())
            disk = psutil.disk_usage(path)
            return disk.free
        except Exception as e:
            logger.error(f"Error getting available storage: {e}")
            return 0
