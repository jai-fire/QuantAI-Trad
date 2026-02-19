import logging
import os

# Create a logger
logger = logging.getLogger('trading_system')
logger.setLevel(logging.DEBUG)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create file handler
file_handler = logging.FileHandler(os.path.join('logs', 'trading_system.log'))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example log messages
logger.debug('Debug message for trading system')
logger.info('Information message for trading system')
logger.warning('Warning message for trading system')
logger.error('Error message for trading system')
logger.critical('Critical message for trading system')
