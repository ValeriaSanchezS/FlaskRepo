# gunicorn_config.py

bind = "0.0.0.0:5000"  # Escucha en todas las direcciones y puerto 5000
workers = 4               # Número de worker processes
timeout = 30              # Tiempo máximo de espera
loglevel = "info"         # Nivel de logs (info, error, debug, etc.)
