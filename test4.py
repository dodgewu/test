import logging 
my_logger=logging.getLogger(__name__)
logging.basicConfig(filename='log/test_log.txt',filemode='a',datefmt='%Y-%m-%d %H:%M:%S',format='[%(asctime)s] %(message)s')
my_logger.info("sdfs")
my_logger.critical("dsadsadsa")