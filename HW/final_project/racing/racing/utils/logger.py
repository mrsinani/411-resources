import logging
import os
import sys

def configure_logger(logger_instance):
    """Configure the logger instance with standard settings.

    Args:
        logger_instance: The logger instance to configure.

    Returns:
        The configured logger instance.
    """
    # Only configure if no handlers exist
    if not logger_instance.handlers:
        level_str = os.getenv('LOG_LEVEL', 'INFO')
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        level = level_map.get(level_str, logging.INFO)

        logger_instance.setLevel(level)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger_instance.addHandler(handler)
    
    return logger_instance 