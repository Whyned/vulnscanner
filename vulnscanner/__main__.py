from vulnscanner import logger
from vulnscanner.scanner import Scanner
from vulnscanner.waiters.random_ipv4 import RandomIPv4Waiter
from vulnscanner.waiters.range_file import RangeFileWaiter
from vulnscanner.workers.port_scanner import PortScannerWorker


def main():
    #logger.LOG_LEVELS_FILES['debug.txt'] = [
    #    logger.LOG_INFO,
    #    logger.LOG_WARN,
    #    logger.LOG_ERROR,
    #    logger.LOG_DEBUG,
    #    logger.LOG_SILLY
    #]
    logger.LOG_LEVELS_FILES['error.txt'] = [logger.LOG_ERROR]
    logger.LOG_LEVELS_FILES['warn.txt'] = [logger.LOG_WARN]
    logger.LOG_LEVELS_STDOUT = []

    logger.attach()

    waiters = [
        #RandomIPv4Waiter({'ports': (80,8080)})
        RangeFileWaiter({'ports': (80,8080), 'file': 'range.txt'})
    ]
    workers = [
        PortScannerWorker({'timeout': 3})
    ]

    s = Scanner(waiters, workers, 200)
    s.run()

if __name__ == "__main__":
    main() 
