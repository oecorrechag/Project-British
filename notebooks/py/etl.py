import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()


from auxiliares_functions import amount
from mypackage import dir


# Environment variables
project = 'british'
data = dir.make_dir(project) 
raw = data('raw')
processed = data('processed')
outputs = data('outputs')


# Función para cargar datos
def cargar_datos(table_name: str) -> pd.DataFrame:
    df = pd.read_csv(raw / f'{table_name}.csv', sep = ',', decimal = '.', header = 0)
    print(f'Loaded table: {table_name}')
    return df

# Función para transformar las startups
def transformar_startups(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df['categories'] = df['categories'].str.lower()
    df.rename(columns={'satus':'status', 
                       'y_combinator_year':'year',
                       'y_combinator_session':'session',
                       'amounts_raised_in_different_funding_rounds':'amounts_raised',
                       'office_address':'address',
                       'headquarters_(city)':'city',
                       'headquarters_(us_state)':'state',
                       'headquarters_(country)':'country',
                       },inplace=True)
    
    df['year'] = df['year'].astype(int)

    df['categories'] = df['categories'].fillna('otro')

    df['address'] = df['address'].fillna('no_address')
    df['city'] = np.where(df['address'] == 'Hong Kong, Asia', 'Hong Kong', df['city'])
    df['city'] = np.where(df['address'] == 'Usa, Kochi, JPN', 'Usa', df['city'])
    df['city'] = np.where(df['address'] == '5150 El Camino Real Suite A24 Los Altos, California 94022, Usa, Kochi, JPN', 'Los Altos', df['city'])
    df['city'] = np.where(df['city'] == 'New York City', 'New York', df['city'])
    df['city'] = np.where(df['city'] == 'Montréal', 'Montreal', df['city'])
    df['city'] = np.where(df['city'] == 'San Francisco, New York City', 'San Francisco', df['city'])
    df['state'] = np.where(df['address'] == 'Usa, Kochi, JPN', 'Kochi', df['state'])
    df['state'] = np.where(df['address'] == '5150 El Camino Real Suite A24 Los Altos, California 94022, Usa, Kochi, JPN', 'California', df['state'])
    df['state'] = np.where(df['city'] == 'London', 'London', df['state'])
    df['state'] = np.where(df['city'] == 'Toronto', 'Toronto', df['state'])
    df['state'] = np.where(df['state'] == 'California, New York', 'California', df['state'])
    df['country'] = np.where(df['address'] == 'Usa, Kochi, JPN', 'USA', df['country'])
    df['country'] = np.where(df['address'] == '5150 El Camino Real Suite A24 Los Altos, California 94022, Usa, Kochi, JPN', 'USA', df['country'])

    df_ciudades = cargar_datos('df_ciudades')
    df = df.merge(df_ciudades[['city', 'state', 'country']], on=['city'], how='left', suffixes=('', '_nuevo'))
    df['state'] = df['state'].fillna(df['state_nuevo'])
    df['country'] = df['country'].fillna(df['country_nuevo'])
    df.drop(columns=['state_nuevo', 'country_nuevo'], inplace=True)

    df['id'] = df.index
    df['id'] = df['id'].astype('str')

    df.drop(['mapping_location',
             'year_founded',
             'crunchbase_/_angel_list_profile',
             'seed-db_/_mattermark_profile'],axis=1,inplace=True)

    df = df.loc[:,['id', 'company', 'status', 'description', 'categories', 'founders', 'year',
                   'session', 'investors', 'amounts_raised', 'address', 'city', 'state',
                   'country', 'logo', 'website']]

    return df

# Función para crear dataset
def crear_dataset(df: pd.DataFrame) -> pd.DataFrame:

    max_date = df['year'].max() + 1
    df['territorio'] = df['city'] + ' - ' + df['state'] + ' - ' + df['country']
    df['territorio'] = label_encoder.fit_transform(df['territorio'])
    joblib.dump(label_encoder, outputs/'label_encoder.pkl')

    # new_categories = cargar_datos('new_categories')
    startups_tranformadas_new_cate = cargar_datos('new_categories_pivot')
    startups_tranformadas_new_cate['id'] = startups_tranformadas_new_cate['id'].astype(str)

    df = pd.merge(df, startups_tranformadas_new_cate, on=['id'])

    df['status'] = np.where(df['status'] == 'Exited', 'Operating', df['status'])
    df['status'] = np.where(df['status'] == 'Operating', 1, 0)
    df['session'] = np.where(df['session'] == 'Summer', 1, 0)
    df['tenure'] = max_date - df['year']

    df['amount'] = df['amounts_raised'].apply(amount)
    df[['total_amount', 'inversion_inicial', 'primera_inversion', 'numero_inversiones']] = df['amount'].apply(pd.Series)

    df.drop(['company', 'description', 'categories', 'founders', 'year', 'investors', 'amounts_raised', 'address', 'city', 'state', 'country', 'amount', 'logo', 'website'],axis=1,inplace=True)
    
    return df


# Función para cargar los datos en la base de datos
def cargar_en_db(df: pd.DataFrame, table_name: str) -> None:
    df.to_parquet(processed/f'{table_name}.parquet.gzip', compression='gzip')
    print(f'Saved table: {table_name}')


if __name__ == '__main__':

    # ETL startups
    startups = cargar_datos('Startups')
    startups_tranformadas = transformar_startups(startups)
    cargar_en_db(startups_tranformadas, 'startups')

    # Create dataset
    dataset = crear_dataset(startups_tranformadas)
    cargar_en_db(dataset, 'dataset')
