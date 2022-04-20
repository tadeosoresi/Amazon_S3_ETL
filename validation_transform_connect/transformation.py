import os
import re
import numpy as np
import pandas as pd
from datetime import date
from dateutil import parser

class ValidateTransform():
    """
    Esta clase se hizo a las apuradas por el tiempo (esta muy desprolija e ineficiente).
    Sirve para tranformar la data del la tabla contenidos, asi
    podemos insertar sus registros en SQL.
    """
    @staticmethod
    def parse_df(filename):
        '''
        Transforms dataframe
        '''
        default_ddl_directory = f'S3files\{filename}'
        actual_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        absolute_route = os.path.join(actual_directory, default_ddl_directory)
        df = pd.read_csv(absolute_route, sep=None, engine='python')
        input_len = len(df)
        print(f'### INPUT LEN {input_len} ###')
        ### First rename all columns
        df.rename(columns={'show_id': 'content_id', 
                        'release_year': 'year', 
                        'listed_in': 'genres'}, inplace=True)
        ### Create platform column
        if 'disney' in filename:
            df['platform_name'] = 'disneyplus'
        else:
            df['platform_name'] = 'netflix'
        ### Drop columns with NaNs in title/id
        df.dropna(subset=['content_id', 'title'], inplace=True)
        ### Drop columns with wrong ID
        df = df[df['content_id'].str.startswith('s')]
        ### Homogeneizamos types
        df['type'] = df['type'].str.lower()
        df['type'] = df['type'].apply(lambda row: row.replace('tv show', 'serie'))
        # Transformamos date_added
        df['date_added'] = df['date_added'].apply(lambda row: row.replace(',', '').lower() if type(row) != float else None)
        df['date_added'] = df['date_added'].apply(lambda row: parser.parse(row) if row else row)
        # Trasformamos year
        def return_int(x):
            try:
                return int(x)
            except ValueError:
                return None
        df['year'] = df['year'].apply(return_int)
        df = df[df['year'] <= date.today().year]
        df['seasons'] = df['duration']
        df['duration'] = df['duration'].apply(lambda row: re.findall(r'\d+', row)[0] if type(row) != float else None)
        df['duration'].astype(int, errors="ignore")
        def return_season(x):
            try:
                if 'min' not in x:
                    return x
                else:
                    return None
            except TypeError:
                return None
        df['seasons'] = df['seasons'].str.lower().apply(return_season)
        df['seasons'] = df['seasons'].apply(lambda row: re.findall(r'\d+', row)[0] if row else row)
        df['seasons'].astype(int, errors="ignore")
        ### Drop all np.nans
        df.replace({np.nan:None})
        output_len = len(df)
        print(f'### OUTPUT LEN {output_len} ###\n')
        
        return df