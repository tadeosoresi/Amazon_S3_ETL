import s3fs
import pandas as pd
from keys import Keys

class ConsultsDB(): #S3 Connection
    """
    Realiza consultas a S3 una vez especificado bucket y archivo.
    """
    def __init__(self):
        self.storage_options = {}
        self.storage_options['key'] = Keys.return_access_key()
        self.storage_options['secret'] = Keys.return_secret_access_key()

    def find_file(self, bucket, path):
        """
        Método para descargar el archivo desde S3 utilizando Pandas.
        """
        if '.csv' in path:
            df = pd.read_csv(f's3://{bucket}/{path}', 
                                storage_options=self.storage_options, 
                                sep=None, 
                                engine='python')
        elif '.xlsx' in path:
            df = pd.read_excel(f's3://{bucket}/{path}', 
                                storage_options=self.storage_options, 
                                sep=None, 
                                engine='python')
        print(f" --- S3 -> Connected ---> {path} ----> To DF")
        return df

class GetDataFrame():
    """
    Clase que permite importar DataFrames de S3 a nuestro jupyter.
    Podemos crear distintos metodos estaticos como quisieramos, y dependiendo
    el tipo de archivo, cada metodo tendra su procesamiento distinto. En este
    caso .csv y .xlsx no hay grandes diferencias en su tratamiento, pero si queremos
    un .txt u otro tipo debemos tratarlo de distintas maneras.
    """
    @staticmethod
    def csv(bucket, filename):
        """
        Devuelve un df de S3 según el bucket y archivo csv que se le ingrese.
        Args:
            bucket (str) ---> nombre bucket
            filename (str) ---> nombre archivo (sin extensión)
        """
        if not all(isinstance(arg, str) for arg in [bucket, filename]):
            raise ValueError("One of the arguments isn't string type, please, write str type!")
        path = filename + '.csv'
        return ConsultsDB().find_file(bucket, path)
    
    @staticmethod
    def xlsx(bucket, filename):
        """
        Devuelve un df de S3 según el bucket y archivo xlsx que se le ingrese.
        Args:
            bucket (str) ---> nombre bucket
            filename (str) ---> nombre archivo (sin extensión)
        """
        if not all(isinstance(arg, str) for arg in [bucket, filename]):
            raise ValueError("One of the arguments isn't string type, please, write str type!")
        path = filename + '.xlsx'
        return ConsultsDB().find_file(bucket, path)
    
    @staticmethod
    def txt(bucket, filename):
        pass