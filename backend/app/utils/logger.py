"""
Módulo de configuración de logs
Gestión unificada de logs con salida a consola y archivo
"""

import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler


def _ensure_utf8_stdout():
    """
    Asegurar que stdout/stderr use codificación UTF-8
    Resolver problema de visualización en consola Windows
    """
    if sys.platform == 'win32':
        # Reconfigurar salida estándar a UTF-8 en Windows
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# Directorio de logs
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')


def setup_logger(name: str = 'mirofish', level: int = logging.DEBUG) -> logging.Logger:
    """
    Configurar logger
    
    Args:
        name: nombre del logger
        level: nivel de log
        
    Returns:
        Logger configurado
    """
    # Asegurar que el directorio de logs existe
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar propagación al root logger para no duplicar salida
    logger.propagate = False
    
    # No agregar handlers si ya existen
    if logger.handlers:
        return logger
    
    # Formato de log
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # 1. Handler de archivo - log detallado (nombrado por fecha, con rotación)
    log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, log_filename),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # 2. Handler de consola - log conciso (INFO y superior)
    # Asegurar codificación UTF-8 en Windows para evitar caracteres incorrectos
    _ensure_utf8_stdout()
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = 'mirofish') -> logging.Logger:
    """
    Obtener logger (crear si no existe)
    
    Args:
        name: nombre del logger
        
    Returns:
        Instancia del logger
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


# Crear logger predeterminado
logger = setup_logger()


# Métodos de conveniencia
def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)

