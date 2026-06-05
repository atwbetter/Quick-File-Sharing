"""
文件传输引擎 - 完整的传输逻辑实现
"""
import asyncio
import hashlib
from typing import Optional, Callable, Dict, Tuple
from pathlib import Path
import config
from core.network import Packet, Message
from core.file_handler import FileHandler
from utils.helpers import format_file_size, calculate_transfer_speed
from utils.logger import get_logger

logger = get_logger("transfer_engine")


class TransferEngine:
    """文件传输引擎"""
    
    def __init__(self):
        """初始化传输引擎"""
        self.file_handler = FileHandler()
        self.active_transfers: Dict[str, dict] = {}
        self.on_progress: Optional[Callable] = None
        self.on_complete: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
    
    async def send_files_wifi(self, transfer_id: str, files_info: list,
                             reader: any, writer: any) -> bool:
        """
        通过WiFi发送文件
        
        Args:
            transfer_id: 传输ID
            files_info: 文件信息列表
            reader: 异步读取流
            writer: 异步写入流
        
        Returns:
            是否成功
        """
        try:
            self.active_transfers[transfer_id] = {
                "status": "sending",
                "start_time": asyncio.get_event_loop().time(),
                "total_files": len(files_info),
                "transferred_files": 0,
                "total_bytes": sum(f["file_size"] for f in files_info),
                "transferred_bytes": 0,
            }
            
            for file_index, file_info in enumerate(files_info):
                file_path = file_info["file_path"]
                file_size = file_info["file_size"]
                file_name = file_info["file_name"]
                
                logger.info(f"Sending file: {file_name} ({format_file_size(file_size)})")
                
                # 发送文件头
                header = Message.create_file_transfer_start(
                    transfer_id,
                    [file_info],
                    file_size
                )
                packet = Packet(config.MessageType.FILE_TRANSFER_START.value, header)
                writer.write(packet.serialize())
                await writer.drain()
                
                # 发送文件内容
                offset = 0
                chunk_index = 0
                
                while offset < file_size:
                    chunk_size = min(config.CHUNK_SIZE, file_size - offset)
                    chunk_data = await self.file_handler.read_file_chunk(
                        file_path, offset, chunk_size
                    )
                    
                    if not chunk_data:
                        raise Exception(f"Failed to read file chunk: {file_path}")
                    
                    # 发送数据包
                    msg_data = Message.create_file_transfer_data(
                        transfer_id, file_index, chunk_index,
                        chunk_data.hex()  # 转换为16进制字符串
                    )
                    packet = Packet(config.MessageType.FILE_TRANSFER_DATA.value, msg_data)
                    writer.write(packet.serialize())
                    await writer.drain()
                    
                    # 更新进度
                    offset += chunk_size
                    chunk_index += 1
                    self.active_transfers[transfer_id]["transferred_bytes"] += chunk_size
                    
                    if self.on_progress:
                        progress = (self.active_transfers[transfer_id]["transferred_bytes"] / 
                                  self.active_transfers[transfer_id]["total_bytes"]) * 100
                        self.on_progress({
                            "transfer_id": transfer_id,
                            "progress": progress,
                            "file_index": file_index,
                            "chunk_index": chunk_index,
                        })
                
                self.active_transfers[transfer_id]["transferred_files"] += 1
            
            # 发送传输结束消息
            end_msg = Message.create_file_transfer_end(transfer_id)
            packet = Packet(config.MessageType.FILE_TRANSFER_END.value, end_msg)
            writer.write(packet.serialize())
            await writer.drain()
            
            if self.on_complete:
                self.on_complete({
                    "transfer_id": transfer_id,
                    "files_count": len(files_info),
                    "total_size": self.active_transfers[transfer_id]["total_bytes"],
                })
            
            logger.info(f"Transfer completed: {transfer_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending files: {e}")
            if self.on_error:
                self.on_error({"transfer_id": transfer_id, "error": str(e)})
            return False
        finally:
            if transfer_id in self.active_transfers:
                del self.active_transfers[transfer_id]
    
    async def receive_files_wifi(self, transfer_id: str, save_dir: str,
                                reader: any, writer: any) -> bool:
        """
        通过WiFi接收文件
        
        Args:
            transfer_id: 传输ID
            save_dir: 保存目录
            reader: 异步读取流
            writer: 异步写入流
        
        Returns:
            是否成功
        """
        try:
            self.active_transfers[transfer_id] = {
                "status": "receiving",
                "start_time": asyncio.get_event_loop().time(),
                "total_files": 0,
                "received_files": 0,
                "total_bytes": 0,
                "received_bytes": 0,
            }
            
            temp_files: Dict[int, str] = {}  # file_index -> temp_path
            
            while True:
                # 读取数据包头
                header_data = await reader.readexactly(64)
                if not header_data:
                    break
                
                # 解析包头获取体长度
                import struct
                _, _, msg_type, _, body_len, _ = struct.unpack(
                    '!7sBHBI4s', header_data
                )
                
                # 读取包体
                body_data = await reader.readexactly(body_len)
                
                # 解析消息类型
                if msg_type == config.MessageType.FILE_TRANSFER_START.value:
                    # 文件开始
                    logger.info("Starting to receive file...")
                
                elif msg_type == config.MessageType.FILE_TRANSFER_DATA.value:
                    # 文件数据
                    import json
                    msg = json.loads(body_data.decode())
                    file_index = msg.get("file_index", 0)
                    chunk_data = bytes.fromhex(msg.get("chunk_data", ""))
                    
                    # 写入临时文件
                    if file_index not in temp_files:
                        temp_path = await self.file_handler.create_temp_file("received_file")
                        temp_files[file_index] = temp_path
                    
                    await self.file_handler.write_file_chunk(
                        temp_files[file_index],
                        msg.get("offset", 0),
                        chunk_data
                    )
                    
                    self.active_transfers[transfer_id]["received_bytes"] += len(chunk_data)
                    
                    if self.on_progress:
                        progress = (self.active_transfers[transfer_id]["received_bytes"] / 
                                  max(self.active_transfers[transfer_id]["total_bytes"], 1)) * 100
                        self.on_progress({
                            "transfer_id": transfer_id,
                            "progress": progress,
                        })
                
                elif msg_type == config.MessageType.FILE_TRANSFER_END.value:
                    # 传输结束
                    logger.info("File transfer completed")
                    break
            
            logger.info(f"Receive completed: {transfer_id}")
            if self.on_complete:
                self.on_complete({
                    "transfer_id": transfer_id,
                    "files_count": len(temp_files),
                    "save_dir": save_dir,
                })
            
            return True
        
        except Exception as e:
            logger.error(f"Error receiving files: {e}")
            if self.on_error:
                self.on_error({"transfer_id": transfer_id, "error": str(e)})
            return False
