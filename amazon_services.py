import os
import sys
import boto3
from keys import Keys
from botocore.exceptions import ClientError

class BotoConnection():
    """
    Clase base: Inicia sesion (boto3) pasandole nuestras keys.
    """
    def __init__(self):
        self.session = boto3.Session(
                        aws_access_key_id=Keys.return_access_key(),
                        aws_secret_access_key=Keys.return_secret_access_key())

class S3(BotoConnection):
    """
    Clase S3 hereda la sesion de la clase base,
    recibe bucket y objeto y los instancia.
    Tiene dos metodos de instancia: download_file y upload_file.
    """
    def __init__(self, bucket, object):
        super().__init__()
        self.bucket = bucket
        self.object = object
        self.s3 = self.session.resource('s3')
        print('\n### Connected to AmazonS3 ###\n')

    def download_file(self):
        '''
        Metodo recursivo.
        Usa la sesion para encontrar el bucket y objeto, si
        el bucket no se encuentra, pide que el usuario ingrese uno nuevo,
        a su vez, si el archivo tampoco, enumera una lista de objetos de los cuales
        el usuario puede elegir para seguir con el proceso.
        El archivo sera descargado en la carpeta S3Files, si no se encuentra, la crea.
        '''
        my_bucket = self.s3.Bucket(self.bucket)
        try:
            files = [bucket.key for bucket in my_bucket.objects.all()] 
        except ClientError:
            new_bucket = str(input('Unrecognized bucket, plase specify another name: '))
            self.bucket = new_bucket
            self.download_file()
        if self.object not in files:
            print('File directory not found! listing all files --->')
            for number, file in enumerate(files):
                print(f'{number+1}: {file}')
            selection = input('Please, select an index of the files listed below/exit to abort: ')
            if selection.isalpha() and selection.lower().strip() == 'exit':
                sys.exit(0)
            elif selection.isdigit():
                self.object = files[int(selection)-1]
                self.download_file()
            else:
                sys.exit('Wrong answer, aborting...')
        actual_directory = os.getcwd()
        folder = os.path.join(actual_directory, 'S3files')
        if not os.path.exists(folder):
            print('Folder not found, creating...')
            os.makedirs(folder)
            print('Folder created!')
            self.download_file()
        else:
            pass
        final_path = os.path.join(folder, self.object)
        my_bucket.download_file(self.object, final_path)
        print(f'{self.object} succesfully downloaded! :)')
  
    def upload_file(self):
        pass

class SQS(BotoConnection):
    """
    Clase SQS hereda la sesion de la clase base.
    """
    def __init__(self):
        super().__init__()
        self.s3 = self.session.resource('sqs')

class EC2(BotoConnection):
    """
    Clase EC2 hereda la sesion de la clase base.
    """
    def __init__(self):
        super().__init__()
        self.s3 = self.session.resource('ec2')
 
class DynamoDB(BotoConnection):
    """
    Clase DynamoDB hereda la sesion de la clase base.
    """
    def __init__(self):
        super().__init__()
        self.s3 = self.session.resource('dynamodb')
