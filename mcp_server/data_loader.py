import pandas as pd

DATA_FILE = 'finanzas_personales.xlsx - in.csv'

def load_user_data():
    try:
        # Lee el archivo CSV
        df = pd.read_csv(DATA_FILE, encoding='latin1')
        
        # --- Limpieza de Datos Esencial ---
        # Convertir 'fecha' a objetos datetime
        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=False, errors='coerce')
        
        # Convertir 'monto' a numérico
        df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
        
        # Manejar filas con valores nulos si es necesario
        df = df.dropna(subset=['fecha', 'monto', 'tipo'])
        
        # Asegurar que los gastos sean negativos (un estándar común)
        # O podemos simplemente confiar en la columna 'tipo'
        
        print(f"Datos cargados y limpios: {df.shape[0]} transacciones.")
        return df

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {DATA_FILE}")
        return pd.DataFrame() # Retorna un DataFrame vacío en caso de error