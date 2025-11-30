import pandas as pd
import numpy as np

def drop_columns(df, columnas):
    df.drop(columns=columnas, inplace=True)
    return df

def normalizar_snake_case(df):
    return df.columns.str.strip().str.lower().str.replace(' ', '_')

def conversor_nulos(df, tipos_nulos):
    df.replace(tipos_nulos, np.nan, inplace=True)
    return df

def comprobar_nulos(df, columna):
    nulos = df[columna].isnull().sum()
    return nulos

def eliminar_espacios(columna):
    return columna.str.lower().str.strip().str.replace(" ", "")

def comprobar_duplicados(df, columna, normalizar=False):
    serie = df[columna]
    if normalizar:
        serie = eliminar_espacios(serie)
    return serie.duplicated().sum()

def eliminar_duplicados_mas_nulos(df, columna):
    #Creamos la nueva columna con el total de nulos de fila
    df['nulos_fila'] = df.isna().sum(axis=1)
    #La ordenamos de menos a más nulos
    df_ordenado = df.sort_values('nulos_fila', ascending=True)
    df_ordenado['name_clean'] = eliminar_espacios(df_ordenado[columna])
    #df_dupes_ordenado = df_ordenado[df_ordenado['name_clean'].duplicated(keep=False)]
    df_sin_dupes = df_ordenado.drop_duplicates(subset='name_clean', keep='first').copy()
    df = drop_columns(df_sin_dupes, "name_clean")
    return df

def convert_type(df, columna, type):
    return df[columna].astype(type)

def filtrar_columna_type(df):
    tipos = df["type"].unique()
    print(tipos)
    df = df[df["type"] != "Music"]
    return df

def filtro_columna_status(df):
    status = df["status"].unique()
    print(f"Valores de status antes del cambio: {status}")
    df = df[df["status"] != "Not yet aired"].copy()
    #Finished Airing -> Finished  y Currently Airing -> Currently
    df.replace("Finished Airing", "Finished", inplace=True)
    df.replace("Currently Airing", "Currently", inplace=True)
    nuevo_status = df["status"].unique()
    print(f"Valores de status tras el cambio: {nuevo_status}")
    return df

def filtrar_columna_aired(df):
    #Separamos las dos partes de la columna aired, fecha inicio y fecha fin (despreciable)
    df['aired'] = df['aired'].astype('string')
    df['aired_start'] = df['aired'].str.split(' to ', n=1, expand=True)[0]
    df['aired_start'] = df['aired_start'].str.strip()

    #Construimos un mapa para convertir las siglas del mes a numérico
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
        'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
        'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    #Utilizamos regex para extraer las siglas del mes y añadir su valor numérico a una nueva columna auxiliar que utilizaremos para facilitar su implementación más adelante
    df['aired_month'] = (
        df['aired_start']
        .str.extract(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', expand=False)
        .map(month_map)
        .astype('Int64')   # para tener enteros con NaN
    )

    #Utilizamos regex para extraer el año de inicio del anime y añadirlo a una nueva columna aired_start
    df['aired_start'] = df['aired_start'].str.extract(r'(\d{4})')
    df['aired_start'] = df['aired_start'].astype('Int64')
    return df

def month_to_season(y, m):
    # Si año o mes son nulos -> devolver NA
    if pd.isna(y) or pd.isna(m):
        return pd.NA

    y = int(y)
    m = int(m)

    if 1 <= m <= 3:
        season = 'winter'
    elif 4 <= m <= 6:
        season = 'spring'
    elif 7 <= m <= 9:
        season = 'summer'
    else:
        season = 'fall'

    return f"{season} {y}" #Ejemplo: winter 2016

def completar_premiered(df):
    premiered_nulls = (df['premiered'].isna() & df['aired_month'].notna() & df['aired_start'].notna())
    df.loc[premiered_nulls, 'premiered'] = (df.loc[premiered_nulls, ['aired_start', 'aired_month']].apply(lambda row: month_to_season(row['aired_start'], row['aired_month']), axis=1))
    return df

def ordenar_columnas(df, columnas):
    return df[columnas]

def parsear_rating(df):
    return df['rating'].str.split(" - ", n=1, expand=True)[0]

def eliminar_nulos_cconcretos(df):
    df = df[~((df["anime_id"] == 55281) | (df["anime_id"] == 55282))]
    return df