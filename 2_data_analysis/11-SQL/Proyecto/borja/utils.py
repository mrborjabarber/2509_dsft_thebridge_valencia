import psycopg2
import pandas as pd
import random
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER") 
db_password = os.getenv("DB_PASSWORD") 
db_host = os.getenv("DB_HOST") 
db_name = os.getenv("DB_NAME")

def generar_email(nombre, apellido):
    return f"{nombre.lower()}.{apellido.lower()}@thebridge.com"

def asignar_campus(ciudad):
   campus_map = {
       'Madrid': 1,
       'Valencia': 2
       # Agrega más ciudades y sus correspondientes campusid aquí
   }
   return campus_map.get(ciudad, None)