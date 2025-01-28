import logging
import os
from datetime import datetime


def setup_logger():
    """
    Sets up the logger for the application.
    Logfiles are stored in the logger/logs directory.
    Starting time of the application is included in the file name.
    """
    directory = './app/logger/logs'
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{directory}/controller_{timestamp}.log'

    logging.basicConfig(
        filename=filename,
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

    logging.info('Starting the GECCO2025-Optimizer API.')


# Set up logging and create logger for this module
setup_logger()
logger = logging.getLogger(__name__)
