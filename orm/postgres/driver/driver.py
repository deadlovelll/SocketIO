import asyncio
import socket
import struct

from typing import Optional, Union

from orm.postgres.driver.config.driver_config import PostgresDriverConfig
from orm.postgres.driver.message_builder.driver_message_builder import (
    PostgresDriverMessageBuilder,
)
from orm.postgres.driver.message_handlers.driver_message_handler import (
    PostgresDriverMessageHandler,
)
from utils.static.privacy.privacy import privatemethod


class PostgresDriver:
    
    def __init__ (
        self,
        driver_config: PostgresDriverConfig,
    ) -> None:
        
        self.host = driver_config.host
        self.port = driver_config.port
        self.user = driver_config.user
        self.password = driver_config.password
        self.database_name = driver_config.database_name
        
        self.connection = None
                
        self.message_builder = PostgresDriverMessageBuilder()
        self.message_handler = PostgresDriverMessageHandler()
        
    async def establish_connection (
        self,
    ) -> None:
        
        self.connection = socket.create_connection((self.host, self.port))
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        psql_message = self.message_builder.build_startup_message(
            self.user,
            self.database_name,
            self.password,
        )
        await self._send_message(psql_message)
        await self._consume_until_ready()
        
    async def close_connection (
        self,
    ) -> None:
        
        if self.connection is not None:
            await self.connection.close()
            self.connection = None
     
    async def reconnect (
        self,
    ) -> None:
        
        await self.close_connection()
        await self.establish_connection()
            
    async def __aenter__ (
        self,
    ) -> "PostgresDriver":
        
        await self._ensure_connection()
        return self

    async def __aexit__ (
        self, 
        exc_type, 
        exc_val, 
        exc_tb,
    ) -> None:
        
        await self.close_connection()
        
    async def execute (
        self,
        query,
    ) -> None:
        
        byte_message = self._build_query_message(query)
        await self._send_message(byte_message)
        result = await self._consume_messages()
        return result 
      
    @privatemethod  
    async def _receive_message (
        self,
    ) -> Union[Optional[str], Optional[dict]]:
        
        buf = bytearray(5)
        self.connection.recv_into(buf)
        header = bytes(buf)
        if len(header) < 5:
            return None, None
        msg_type = header[0:1]
        length = struct.unpack('!I', header[1:5])[0]-4
        payload = self.connection.recv_into(length)
        return msg_type, payload
    
    @privatemethod
    async def _send_message (
        self,
        message: bytes,
    ) -> None:
        
        await self._ensure_connection()
        self.connection.sendall(message)
    
    @privatemethod
    async def _build_query_message (
        self,
        query,
    ) -> bytes:
        
        query_bytes = query.encode('utf-8') + b'\x00'
        byte_length = len(query_bytes) + 4
        return b'Q' + struct.pack('!I', byte_length) + query_bytes
    
    @privatemethod
    async def _consume_messages (
        self,
    ) -> None:
        
        while True:
            msg_type, payload = self._receive_message()
            if msg_type is None:
                break
            result = self.message_handler.handle (
                msg_type,
                payload,
                self.password,
                self.user,
            )

            if isinstance(result, bytes):
                self.connection.sendall(result)
            elif result == 'ready':
                rows = self.message_handler.get_data_rows()
                return rows
    
    @privatemethod       
    async def _consume_until_ready (
        self,
    ) -> None:
        
        while True:
            msg_type, payload = self._receive_message()
            if msg_type is None:
                break
            
            result = self.message_handler.handle(
                msg_type,
                payload,
                self.password,
                self.user,
            )
            
            if isinstance(result, bytes):
                self.connection.sendall(result)
            elif result == 'break':  
                return
        
    @privatemethod
    async def _ensure_connection (
        self,
    ) -> None:
        
        if self.connection is None:
            await self.establish_connection()