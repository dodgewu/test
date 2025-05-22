import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch, MagicMock
from snmp_get import MyGet
from error_statement import SNMPResultLogger
from dut import Dut

# FILE: test_snmp_get.py

class TestMyGet(IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock DUT object
        self.mock_dut = Dut(ip='192.168.1.1', cmts='192.168.1.2', mac='00:11:22:33:44:55', fw='TestFW', test_case='TestCase', wifi_24_ver=None, wifi_55_ver=None)
        self.my_get = MyGet(dut=self.mock_dut)

    @patch('snmp_get.get_cmd')
    @patch('snmp_get.SnmpEngine')
    @patch('error_statement.SNMPResultLogger')
    async def test_my_snmp_get(self, mock_snmp_result_logger, mock_snmp_engine, mock_get_cmd):
        # Mock SNMP response
        mock_get_cmd.return_value = AsyncMock(return_value=(None, None, None, [(None, 'MockedValue')]))
        
        # Mock SNMPResultLogger
        mock_logger_instance = MagicMock()
        mock_snmp_result_logger.return_value = mock_logger_instance

        # Call the method
        explanation = "Test explanation"
        result = await self.my_get.my_snmp_get(explanation)

        # Assertions
        self.assertEqual(result, 'MockedValue')  # Verify the returned value
        mock_snmp_result_logger.assert_called_once_with(self.mock_dut)  # Verify logger initialization
        mock_logger_instance.store_result.assert_called_once_with(self.mock_dut, mock_get_cmd.return_value, explanation)  # Verify result storage
        mock_snmp_engine.return_value.close_dispatcher.assert_called_once()  # Verify dispatcher closure