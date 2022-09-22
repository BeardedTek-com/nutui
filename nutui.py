#!/usr/bin/env python3
from app import app
from nut2 import PyNUTClient, PyNUTError
from threading import Thread
from time import sleep
import json
import requests
import logging
import argparse
class nutclient:
    def __init__(self,host='localhost',ups="",login=None,password=None,debug=False,timeout=5,interval=30,apiHost="localhost",apiPort=5000):
        if debug:
            # Print DEBUG messages to the console.
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        # Initialize PyNUTClient as nutclient
        try:
            self.nutclient = PyNUTClient(host=host,login=login,password=password,debug=debug,timeout=timeout)
        except PyNUTError as e:
            logging.info(f"An error has occured: {e}")
            logging.debug(f"host: {host}")
            logging.debug(f"ups: {ups}")
            logging.debug(f"login: {login}")
            logging.debug(f"password: {password}")
            logging.debug(f"debug: {debug}")
            logging.debug(f"timeout: {timeout}")
            logging.debug(f"interval: {interval}")
            logging.debug(f"apiHost: {apiHost}")
            logging.debug(f"apiPort: {apiPort}")
            quit()
        self.upslist = self.nutclient.list_ups()
        logging.info(self.upslist)
        self.interval = interval
        self.ups = ups
        self.apiHost = apiHost
        self.apiPort = apiPort
        logging.info("Initializing nutclient...")
        logging.debug(f"nutUI Host: {apiHost}:{apiPort}")

        # Setup threading
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        sleep(5)
        while True:
            for ups in self.upslist:
                logging.info(ups)
                try:
                    apiURL = f"http://{self.apiHost}:{self.apiPort}/api/data/add/{ups}"
                    logging.debug(f"API URL: {apiURL}")
                    data = self.nutclient.list_vars(ups)
                    logging.debug(json.dumps(data,indent=2))
                    request = requests.post(apiURL, json=data)
                    sleep(self.interval)
                except Exception as error:
                    logging.debug(f"An Error Has Occcured:")
                    logging.info(f"{error}")
                    sleep(5)


if __name__ == "__main__":
    cla = argparse.ArgumentParser(description="Starts nutclient and nutui flask server")
    cla.add_argument('-c','--clientonly',required=False,action='store_true',default=False,
                        help="Runs nutclient only.  Disables the flask server")
    cla.add_argument('-f','--flaskonly',required=False,action='store_true',default=False,
                        help="Runs the flask server only")
    cla.add_argument('-v','--verbose',required=False,action='store_true',default=False,
                        help="Verbose Output")
    cla.add_argument('-u','--uwsgi', required=False,action='store_true',default=False,
                        help="Launches web app with uwsgi instead of flask development server")
    cla.add_argument('-a','--all',required=False,action='store_true',default=True)
    cla.add_argument('-n','--nuthost',required=False,type=str,default='127.0.0.1',
                        help="ip/hostname of nut server (defaults to 127.0.0.1)")
    cla.add_argument('-ah','--apihost',required=False,type=str,default='localhost',
                        help="ip/hostname of nutUI api server")
    cla.add_argument('-ap','--apiport',required=False,type=int,default=5000,
                        help="port number of nutUI api server")
    cla.add_argument('-i','--interval',required=False,type=int,default=60,
                        help="number of seconds between polling nut-server")
    cla.add_argument('-l','--nutlogin',required=False,type=str,default=None,
                        help="nut-server login (default: None)")
    cla.add_argument('-p','--nutpassword',required=False,type=str,default=None,
                        help="nut-server login (default: None)")
    clArgs = vars(cla.parse_args())
    if clArgs['clientonly']:
        logging.info("[ nutUI | STARTUP ] Running in CLIENT ONLY mode")
        clArgs['all'] = False
    elif clArgs['flaskonly']:
        logging.info("[ nutUI | STARTUP ] Running in FLASK ONLY mode")
        clArgs['all'] = False
    else:
        logging.info("[ nutUI | STARTUP ] Running in CLIENT and FLASK")
        

    if clArgs['clientonly'] or clArgs['all']:
        nutclient(host=clArgs['nuthost'],login=clArgs['nutlogin'],password=clArgs['nutpassword'],debug=clArgs['verbose'],interval=clArgs['interval'],apiHost=clArgs['apihost'],apiPort=clArgs['apiport'])
    if clArgs['flaskonly'] or clArgs['all']:
        if not clArgs['uwsgi']:
            logging.info("[ nutUI | STARTUP ] Starting Flask Server")
            app.run(host='0.0.0.0',debug=True,port=5000)
        else:
            logging.info("[ nutUI | STARTUP ] uwsgi NOT READY YET")