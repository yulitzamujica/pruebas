#! python3
from requests.auth import HTTPBasicAuth
import requests
import yaml
import json
import os
import sys

from RPA_Descargar_Bonos.bot_boletas import execute_principal_page
from main import extract_data
from time import sleep

class Registro_diario:
    def __init__(self):
        #self.ENV = ENV
        self.url_base="http://rpabonos.optasalud.cl/"


    def actualizar_estado_proceso(self, estado, pk):
        listo = False
        print("Metodo actualizar_estado_proceso")
        logging.debug('Actualizando el estado del proceso de las cuentas')
        try:
            #paht =
            url = self.url_base +"consultar-api/consultar/"+str(pk)
            headers = {'content-type': 'application/json','accept':'application/json'}

            #user = self.ENV['USER']
            #password = self.ENV['PASS']
            user = 'rpa'
            password = 'rpa123456'
            data = {'finalizo':estado

            }
            #req = requests.put(url,auth=HTTPBasicAuth(user, password),data = json.dumps(data),headers=headers)
            req = requests.put(url,data = json.dumps(data),headers=headers)
            if req.status_code == 200:
                data = req.json()
                print("data ->",data)
                listo = True
                print("estado actualizado")
            print("req.status_code: ", req.status_code)
        except Exception as error:
                print("ERROR PROCESANDO REGISTRO DIARIO --> {} ".format(error))
                logging.debug('ERROR PROCESANDO REGISTRO DIARIO --> %s', error)
        return listo

    def crear_estado_proceso(self):
        pk = -1
        print("Metodo crear_estado_proceso")
        logging.debug('Actualizando el estado del proceso de las cuentas')
        try:

            url = self.url_base +"consultar-api/consultar/"
            headers = {'content-type': 'application/json','accept':'application/json'}

            #user = self.ENV['USER']
            #password = self.ENV['PASS']
            user = 'rpa'
            password = 'rpa123456'
            data = {'finalizo':False

            }
            #req = requests.post(url,auth=HTTPBasicAuth(user, password),data = json.dumps(data),headers=headers)
            req = requests.post(url,data = json.dumps(data),headers=headers)
            if req.status_code == 200 or req.status_code == 201:
                data = req.json()
                print("data ->",data)
                pk = data['id']
                print("registro nuevo creado")
                print("pk: ", pk)
            print("req.status_code: ", req.status_code)
        except Exception as error:
                print("ERROR PROCESANDO REGISTRO DIARIO --> {} ".format(error))
                logging.debug('ERROR PROCESANDO REGISTRO DIARIO --> %s', error)
        return pk

    def procesar_registro_diario(self, registro_diario):
        listo = False
        print("Metodo procesar_registro_diario")
        logging.debug('PROCESANDO REGISTRO DIARIO')
        try:
            url = "http://rpabonos.optasalud.cl/desktop-api/procesar/"+registro_diario
            headers = {'content-type': 'application/json','accept':'application/json'}
            #user = self.ENV['USER']
            #password = self.ENV['PASS']
            user = 'rpabono'
            password = 'rpabono'
            data = {

            }
            #req = requests.post(url,auth=HTTPBasicAuth(user, password),data = json.dumps(data),headers=headers)
            req = requests.post(url,data = json.dumps(data),headers=headers)
            if req.status_code == 200:
                data = req.json()
                print("data ->",data)
                listo = True
        except Exception as error:
                print("ERROR PROCESANDO REGISTRO DIARIO --> {} ".format(error))
                logging.debug('ERROR PROCESANDO REGISTRO DIARIO --> %s', error)
        return listo

    def actualizar_registro_diario(self, registro_diario, rutPrestador):
        print("Metodo actualizar_registro_diario")
        logging.debug('ACTUALIZANDO REGISTRO DIARIO')
        try:
            url = "http://rpabonos.optasalud.cl/desktop-api/update/"+registro_diario
            headers = {'content-type': 'application/json','accept':'application/json'}
            #user = self.ENV['USER']
            #password = self.ENV['PASS']
            user = 'rpabono'
            password = 'rpabono'
            data = {'rut_prestador':rutPrestador

            }
            #req = requests.post(url,auth=HTTPBasicAuth(user, password),data = json.dumps(data),headers=headers)
            req = requests.post(url,data = json.dumps(data),headers=headers)
            if req.status_code == 200:
                data = req.json()
                print("data ->",data)

        except Exception as error:
                print("ERROR ACTUALIZANDO REGISTRO DIARIO --> {} ".format(error))
                logging.debug('ERROR ACTUALIZANDO REGISTRO DIARIO --> %s ', error)

import logging
from datetime import datetime
LOG_FILENAME = datetime.now().strftime('/tmp/logfile_%H_%M_%S_%d_%m_%Y.log')

if __name__ == "__main__":

    #ocrconf = yaml.load(open('OCR_Extractor_Datos_Bonos/conf/base.conf', "r"), Loader=yaml.FullLoader)['ENV']
    #ENV = yaml.load(open('OCR_Extractor_Datos_Bonos/conf/{}'.format(ocrconf), "r"), Loader=yaml.FullLoader) # carga el dicionario de ocr.conf en la variable ENV
    reg_diario = Registro_diario()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename=LOG_FILENAME, format=format, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")
    logging.debug('Iniciando logging')

    """
    ##################### cod_financiador #####################
        Banmedica : 82d169e8-f959-4143-9390-a932d90f5878
        VidaTres: 29fc89f0-a946-4859-a4a3-0632efc2de79
        Cruz Blanca: 36c8e611-e3b7-40c4-a7ab-75bb54cb3cfc
    ###########################################################
    """

    cod_financiador = '36c8e611-e3b7-40c4-a7ab-75bb54cb3cfc'

    rut = sys.argv[1]
    clave = sys.argv[2]
    clinica = sys.argv[3]
    numero_clinica = sys.argv[4]

    #TODO: crear un metodo que extraiga los datos de las tablas
    if numero_clinica == '1' or numero_clinica == '2':
        if numero_clinica == '1':
            name_clinica = "Indisa"
            cod_prestador = "cdd381be-637a-4af2-b125-05e4075eb5a2"
            cod_cliente = "a0a590d7-d527-49e0-8b76-38d3923a0060"
            rutPrestador = "920510000"
        elif numero_clinica == '2':
            name_clinica = "Vitacura"
            cod_prestador = "2de72f3d-054d-4852-baf7-565750c59ef8"
            cod_cliente = "4571c876-58de-496c-a843-08141ef87c6e"
            rutPrestador = "780535601"

        execute_principal_page(rut, clave, clinica, name_clinica)
        sleep(5)
        pk = reg_diario.crear_estado_proceso()
        print("Registro creado, pk: ", pk)
        sleep(5)
        registro_diario = extract_data(cod_financiador, name_clinica, cod_prestador, cod_cliente)
        print("registro_diario:", registro_diario)
        logging.debug('registro_diario: %s', registro_diario)
        sleep(5)
        reg_diario.procesar_registro_diario(registro_diario)
        sleep(5)
        reg_diario.actualizar_estado_proceso(True, pk)
        print("Registro actualizado")
        sleep(5)
        reg_diario.actualizar_registro_diario(registro_diario, rutPrestador)

    else:
        print(" Numero de clinica invalido...")

    """
        Linea de comandos para ejecutarlo:
        python bot_boletas.py rut clave clinica num_clinica

        Indisa : num_clinica = 1
        Vitacura : num_clinica = 2

        Ejecucion de Indisa: python executor.py 16016110-8 230385 92051000-0 1
        Ejecucion de Vitacura: python executor.py 17318575-8 123456 78053560-1 2
        TODO: cruzar el numero con la tabla cliente

    """
    """
    ######################################################### mensaje #################################################################
        Este archivo esta configurado para el servidor
    ###########################################################################################################################################
    """
