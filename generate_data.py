import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Inicializa Faker
fake = Faker()

# --- Configuración de Generación ---
NUM_ROWS = 10000  # Número de filas que deseas generar
FILE_NAME = "mass_tran_data.csv"

# Listas de valores posibles para las columnas de categoría
REGIONS = ['North', 'South', 'East', 'West', 'Central']
CATEGORIES = ['Electronics', 'Clothing', 'Books', 'Home Goods', 'Food & Drink', 'Services']
# Define un rango de fechas para las transacciones (últimos 90 días)
START_DATE = datetime.now() - timedelta(days=90)

# --- Generación de Datos ---
data = {
    'transaction_id': [f'T{i:05d}' for i in range(1, NUM_ROWS + 1)],
    'timestamp': [],
    'region': [random.choice(REGIONS) for _ in range(NUM_ROWS)],
    'product_category': [random.choice(CATEGORIES) for _ in range(NUM_ROWS)],
    'value_column': [],
    'quantity': [random.randint(1, 5) for _ in range(NUM_ROWS)]
}

for i in range(NUM_ROWS):
    # Genera un timestamp aleatorio dentro del rango
    random_days = random.randint(0, 90)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    random_time = START_DATE + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
    data['timestamp'].append(random_time.strftime('%Y-%m-%d %H:%M:%S'))

    # Genera un valor de transacción realista (entre 5.00 y 5000.00)
    data['value_column'].append(round(random.uniform(5.00, 5000.00), 2))

# Crea el DataFrame de Pandas
df = pd.DataFrame(data)

# Guarda el DataFrame en un archivo CSV
df.to_csv(FILE_NAME, index=False)

print(f"✅ Archivo '{FILE_NAME}' generado con {NUM_ROWS} filas de datos.")
print("Las primeras 5 filas:")
print(df.head())