import sys
import argparse
from storage import S3

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '%s: error: %s\n' % (self.prog, message))

if __name__ == '__main__':
    """
    main.py ---> Sirve para operar con distintos servicios de Amazon
    Hoy por hoy, unicamente interactua con la clase S3 descargando archivos que le pasamos via bash.
    Argumentos:
    . --bucket   bucket (o directorio) al que queremos acceder, en este caso esta defualt el del desafio.
    . --fileurl  url del archivo/objeto que queremos descargar
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', help = 'Repositorio del cual extraer datos', type=str, default='desafio-rkd')
    parser.add_argument('--fileurl', help = 'Path del archivo', type=str)
    #parser.add_argument('--resource', help = 'Servicio de Amazon', type=str, default='s3')
    args = parser.parse_args()
    if not args.fileurl:
        raise argparse.ArgumentError('Specify fileurl in str format!')
    S3(args.bucket, args.fileurl).download_file()