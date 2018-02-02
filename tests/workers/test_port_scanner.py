from vulnscanner.workers.port_scanner import PortScannerWorker
from vulnscanner import logger
logger.attach()

def test_PortScannerWorker():
    pw = PortScannerWorker({'timeout': 10})
    pw.processHostPort('google.de', 80)
