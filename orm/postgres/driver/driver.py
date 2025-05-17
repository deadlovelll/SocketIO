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
from utils import privatemethod, ProtectedClass


class PostgresDriver(ProtectedClass):
    
    def __init__ (
        self,
        driver_config: PostgresDriverConfig,
    ) -> None:
        
        self._host = driver_config.host
        self._port = driver_config.port
        self._user = driver_config.user
        self._password = driver_config.password
        self._database_name = driver_config.database_name
        
        self._connection = None
                
        self._message_builder = PostgresDriverMessageBuilder()
        self._message_handler = PostgresDriverMessageHandler()
        
    async def establish_connection (
        self,
    ) -> None:
        
        self._connection = socket.create_connection((self._host, self._port))
        self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        psql_message = self._message_builder.build_startup_message(
            self._user,
            self._database_name,
            self._password,
        )
        await self._send_message(psql_message)
        await self._consume_until_ready()
        
    async def close_connection (
        self,
    ) -> None:
        
        if self._connection is not None:
            self._connection.close()
            self._connection = None
     
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
        
        byte_message = await self._build_query_message(query)
        await self._send_message(byte_message)
        result = await self._consume_messages()
        return result 
      
    @privatemethod  
    async def _receive_message (
        self,
    ) -> Union[Optional[str], Optional[dict]]:
        
        header = self._connection.recv(5)
        if len(header) < 5:
            return None, None
        msg_type = header[0:1]
        length = struct.unpack('!I', header[1:5])[0]-4
        payload = self._connection.recv(length)
        return msg_type, payload
    
    @privatemethod
    async def _send_message (
        self,
        message: bytes,
    ) -> None:
        
        await self._ensure_connection()
        self._connection.sendall(message)
    
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
            msg_type, payload = await self._receive_message()
            if msg_type is None:
                break
            result = self._message_handler.handle (
                msg_type,
                payload,
                self._password,
                self._user,
            )

            if isinstance(result, bytes):
                self._connection.sendall(result)
            elif result == 'ready':
                rows = self._message_handler.get_data_rows()
                return rows
    
    @privatemethod       
    async def _consume_until_ready (
        self,
    ) -> None:
        
        while True:
            msg_type, payload = await self._receive_message()
            if msg_type is None:
                break
            
            result = self._message_handler.handle(
                msg_type,
                payload,
                self._password,
                self._user,
            )
            
            if isinstance(result, bytes):
                self._connection.sendall(result)
            elif result == 'break':  
                return
        
    @privatemethod
    async def _ensure_connection (
        self,
    ) -> None:
        
        if self._connection is None:
            await self.establish_connection()