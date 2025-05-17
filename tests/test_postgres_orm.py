import asyncio
import unittest
from unittest.mock import mock_open, patch

from orm.postgres.driver.driver import PostgresDriver
from orm.postgres.driver.config.driver_config import PostgresDriverConfig


class TestDetectors(unittest.TestCase):
    
    def setUp(self) -> None:
        self.config = PostgresDriverConfig(
            host='localhost', 
            port=5432, 
            user='my_user', 
            database_name='myapp_db',
        )
        
        return super().setUp()
    
    
    def test_select_query(self) -> None:
        driver = PostgresDriver(self.config)
        query = "SELECT 1;"
        result = asyncio.run(driver.execute(query))
        self.assertEqual(result, '1')