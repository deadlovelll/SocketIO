import unittest 

from utils.socketio_validators.socketio_port_validator.socketio_port_validator import SocketIOPortValidator

from exceptions.socketio_exceptions.socketio_exceptions import (
    SocketIOForbieddenPortError,
    SocketIOInproperPortError,
)


class TestPortValidator(unittest.TestCase):
    
    def __init__ (
        self, 
        methodName: str = "runTest",
    ) -> None:
        
        super().__init__(methodName)
    
    def test_valid_port_n1 (
        self,
    ) -> None:
        
        port = SocketIOPortValidator.verify_port_validity(4000)
        self.assertEqual(port, 4000)
        
    def test_valid_port_n2 (
        self,
    ) -> None:
        
        port = SocketIOPortValidator.verify_port_validity(5000)
        self.assertEqual(port, 5000)
        
    def test_valid_port_n3 (
        self,
    ) -> None:
        
        port = SocketIOPortValidator.verify_port_validity(6000)
        self.assertEqual(port, 6000)
        
    def test_invalid_port_n1 (
        self,
    ) -> None:
        
        expected_message = (
            "\n"
            + "#" * 80 + "\n"
            + f"#  ERROR: Port '900' is reserved by the system.                               #\n"
            + "#  Please use a port number higher than 1024. Default SocketIO port is 4000    #\n"
            + "#  System-reserved ports range: 0–1024.                                        #\n"
            + "#" * 80
        )
        
        with self.assertRaises(SocketIOForbieddenPortError) as cm:
            SocketIOPortValidator.verify_port_validity(900)
            
        self.assertEqual (
            str(cm.exception).strip(),
            expected_message.strip(),
        )
        
    def test_invalid_port_n2 (
        self,
    ) -> None:
        
        expected_message = (
            "\n"
            + "#" * 80 + "\n"
            + f"#  ERROR: Port '1000' is reserved by the system.                               #\n"
            + "#  Please use a port number higher than 1024. Default SocketIO port is 4000    #\n"
            + "#  System-reserved ports range: 0–1024.                                        #\n"
            + "#" * 80
        )
        
        with self.assertRaises(SocketIOForbieddenPortError) as cm:
            SocketIOPortValidator.verify_port_validity(1000)
            
        self.assertEqual (
            str(cm.exception).strip(),
            expected_message.strip(),
        )
        
    def test_invalid_port_n3 (
        self,
    ) -> None:
        
        expected_message = (
            "\n"
            + "#" * 80 + "\n"
            + f"#  ERROR: Port '1' is reserved by the system.                               #\n"
            + "#  Please use a port number higher than 1024. Default SocketIO port is 4000    #\n"
            + "#  System-reserved ports range: 0–1024.                                        #\n"
            + "#" * 80
        )
        
        with self.assertRaises(SocketIOForbieddenPortError) as cm:
            SocketIOPortValidator.verify_port_validity(1)
            
        self.assertEqual (
            str(cm.exception).strip(),
            expected_message.strip(),
        )
            
    def test_inproper_port_n1 (
        self,
    ) -> None:
        
        expected_message = (
            "\n"
            + "#" * 75 + "\n"
            + f"#  ERROR: Invalid port number 'abc'.                             #\n"
            + "#  Allowed port range: 0–65535. Default SocketIO port is 4000             #\n"
            + "#  Please specify a valid port within this range.                         #\n"
            + "#" * 75
        )
        
        with self.assertRaises(SocketIOInproperPortError) as cm:
            SocketIOPortValidator.verify_port_validity('abc')
            
        self.assertEqual (
            str(cm.exception).strip(),
            expected_message.strip(),
        )
        
    def test_inproper_port_n2 (
        self,
    ) -> None:
        
        expected_message = (
            "\n"
            + "#" * 75 + "\n"
            + f"#  ERROR: Invalid port number '-10000'.                             #\n"
            + "#  Allowed port range: 0–65535. Default SocketIO port is 4000             #\n"
            + "#  Please specify a valid port within this range.                         #\n"
            + "#" * 75
        )
        
        with self.assertRaises(SocketIOInproperPortError) as cm:
            SocketIOPortValidator.verify_port_validity(-10000)
            
        self.assertEqual (
            str(cm.exception).strip(),
            expected_message.strip(),
        )
        
    def test_inproper_port_n3 (
        self,
    ) -> None:
        
        expected_message = (
            "\n"
            + "#" * 75 + "\n"
            + f"#  ERROR: Invalid port number 'b'/x00/x00''.                             #\n"
            + "#  Allowed port range: 0–65535. Default SocketIO port is 4000             #\n"
            + "#  Please specify a valid port within this range.                         #\n"
            + "#" * 75
        )
        
        with self.assertRaises(SocketIOInproperPortError) as cm:
            SocketIOPortValidator.verify_port_validity(b'/x00/x00')
            
        self.assertEqual (
            str(cm.exception).strip(), 
            expected_message.strip(),
        )