import os
import pyodbc
from pyodbc import ProgrammingError

class SQLConnection():
    """
    Clase que se encarga de hacer la conexión a SQL
    ###
    connect_database():
    Crea database ---> si no existe
    Args: database name
    ###
    execute_ddl():
    ejecuta un ddl almacenados en la carpeta ddls
    Args: file name
    ### IN PROGRESS (cuestiones de decodificacion)

    """
    def __init__(self):
        self.conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost;"
                      "Database=master;"
                      "Trusted_Connection=yes;",
                      autocommit=True)
    
    def __del__(self):
        self.conn.close()

    def connect_database(self, database='platforms_database'):
        """
        Utiliza la conexión a master para validar que exita DB 
        (por default tenemos platforms_database), si no la encuentra
        la crea.
        Conecta a la DB y devuelve la conexión.
        """
        print ('### Connecting via ODBC ###\n')
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT name FROM master.dbo.sysdatabases where name=?;",(database,))
            data = cursor.fetchall()     
            if not data:
                cursor.execute(f"CREATE DATABASE {database}")
                cursor.commit()
                print(f'### Database created ---> {database} ###')
            else:
                print(f'### Database ----> {database} already exists (OK) ###')
        platforms_conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                        "Server=localhost;"
                                        f"Database={database};"
                                        "Trusted_Connection=yes;")
        return platforms_conn.cursor()
    
    def execute_ddl(self, filename: str):
        """
        IN PROGRESS: Recibe como Arg el nombre de un ddl
        y lo ejecuta (haciendo previamente la validación)
        en la carpeta de ddls.
        """
        default_ddl_directory = f'ddl_diagrama_sqlscripts\ddls\{filename}'
        actual_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        absolute_route = os.path.join(actual_directory, default_ddl_directory)
        assert os.path.exists(absolute_route), ('### Archivo ddl no encontrado, especificar con extensión '
                                                'y guardar en ddl_diagrama_sqlscripts\ddls ###')
        cursor = self.connect_database()
        with open(absolute_route,'r') as file:
            ddl = file.read()
        cursor.execute(ddl)
        cursor.close()
    
    def insert_into(self, df, database='platforms_database'):
        """
        Metodo que hace inserción (no tan eficiente, deberiamos usar sqlalchemy)
        de los registros en la base de datos
        """
        cursor = self.connect_database(database)
        # Insert Dataframe into SQL Server:
        print(f'### INSERTING DATA INTO TABLE {database} ###\n')
        for index, row in df.iterrows():
            try:
                cursor.execute("INSERT INTO contenidos (content_id,platform_name,"
                                "title,type,director,cast,country,date_added,year,rating,duration,"
                                "seasons,genres,description) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                                row.content_id, row.platform_name, row.title,
                                row.type, row.director, row.cast, 
                                row.country,row.date_added, row.year, 
                                row.rating, row.duration, row.seasons,
                                row.genres, row.description)
                cursor.commit()
            except ProgrammingError:
                continue
        cursor.close()
        print(f'### DATA INSERTED ###')
