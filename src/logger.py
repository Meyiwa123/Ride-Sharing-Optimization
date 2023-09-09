import logging
import datetime
import os

# Get the current date and time
current_datetime = datetime.datetime.now()

# Create the folder path for the "logs" folder (if it doesn't exist)
logs_folder = "logs"
os.makedirs(logs_folder, exist_ok=True)

# Use the date and time to create a unique log filename inside the "logs" folder
log_filename = os.path.join(
    logs_folder, f"{current_datetime.strftime('%Y%m%d_%H%M%S')}.log")

# Basic configuration for logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    filename=log_filename,
                    filemode='a',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Create a logger
logger = logging.getLogger(__name__)