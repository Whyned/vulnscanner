import socket

from vulnscanner.workers.port_scanner import PortScannerWorker
from vulnscanner import logger
logger.attach()

original_logger_result = logger.result

def teardown_module():
    global logger
    logger.result = original_logger_result


def test_PortScannerWorker_1():
    host = '127.0.0.1'
    port = 9999
    test_PortScannerWorker_1.fetched = False
    def result_fetcher(worker_name, type, file, str):
        test_PortScannerWorker_1.fetched = True
        assert type == 'open'
        assert str == '%s:%s' %(host,port)

    logger.result = result_fetcher
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(1)

    pw = PortScannerWorker({'timeout': 10})
    pw.processHostPort(host, port)

    s.close()

    assert test_PortScannerWorker_1.fetched is True

def test_PortScannerWorker_2():
    test_PortScannerWorker_2.fetched = False
    def result_fetcher(worker_name, type, file, str):
        test_PortScannerWorker_2.fetched = True

    logger.result = result_fetcher

    pw = PortScannerWorker({'timeout': 10})
    pw.processHostPort('127.0.0.1', 9999)

    assert test_PortScannerWorker_2.fetched is False
