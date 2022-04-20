import pandas as pd

class Analysis():
    """
    Clase donde automatizamos ciertos metodos de analisis,
    para evitar la repetición de ellos en los distintos analisis 
    posteriores (siempre que la data sea simil)
    """
    @staticmethod
    def check_id_dups(df):
        """
        Metodo que recibe dataframe y hace
        un conteo de duplicados por id.

        Args:
            df (object): DataFrame de pandas.

        """
        campo = 'show_id'
        id_not_null = df[df[campo].notnull()]
        by_id = id_not_null[campo].duplicated().sum()
        pd.options.display.max_colwidth = 240
        print(f"\n ##### DUPLICADOS POR ID: ({by_id}) ##### \n")
        if by_id > 0:
            dup_ids = df[df[campo].duplicated()][campo].tolist()
            print('\n --- ANALISIS IDS DUPLICADOS --- \n')
            for id_ in dup_ids:
                print(df[df[campo] == id_][[campo, 'title', 'type', 'director']])
        else:
            print("DUPLICADOS: NO HAY DUPLICADOS \n")
        print("\n ####################### \n")  

    @staticmethod
    def check_title(df):
        """
        Método para analizar Title.

        - Revisa Titles duplicados.

        Args:
            df (object): DataFrame de pandas.
        """
        campo = 'title'
        print(f" ***** Análisis {campo} ***** ")
        if df[campo].isnull().all() == True:
            print(f'No hay ningun dato en el campo {campo}.')
        else:
            df = df[df[campo].notnull()]
            df[campo].apply(lambda title: title.strip().replace(r'\n', '').replace(r'\t', '')) # Homogeneizamos titles

            print("\n ##### DUPLICADOS: ##### \n")
            duplicates_titles = df[df[[campo, 'type']].duplicated(keep=False)].sort_values(by=campo, ascending=True)
            if len(duplicates_titles) > 0:
                for index, row in duplicates_titles.iterrows():
                    title = row[campo]
                    id_ = row['show_id']
                    count = (duplicates_titles[campo] == title).sum()
                    print(f"ID's: {id_} Title: {title} ---> {count} veces\n")
            else:
                print("DUPLICADOS: NO HAY DUPLICADOS \n")
            print("\n ####################### \n")  