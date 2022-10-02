#!/usr/bin/env python3
from nut2 import PyNUTClient, PyNUTError
from threading import Thread
from time import sleep, time
import json
import requests
import logging
import argparse
class nutui:
    def __init__(self,client=True,nutHost='localhost',ups="",login=None,password=None,debug=False,timeout=5,interval=30,apiHost="localhost",apiPort=5000):
        if debug:
            # Print DEBUG messages to the console.
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        # Initialize PyNUTClient as nutclient
        try:
            self.nutclient = PyNUTClient(host=nutHost,login=login,password=password,debug=debug,timeout=timeout)
        except PyNUTError as e:
            logging.info(f"An error has occured: {e}")
            logging.debug(f"host: {nutHost}")
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
        self.client = client
        logging.info("Initializing nutclient...")
        logging.debug(f"nutUI Host: {apiHost}:{apiPort}")
        self.start()

    def start(self):
        logging.debug("Starting Up Client")
        if self.client:
            logging.debug("Client Enabled")
            # Setup nutclient threading
            clientThread = Thread(target=self.nutClient, args=())
            clientThread.daemon = True
            clientThread.start()

    def nutClient(self):
        sleep(5)
        while True:
            for ups in self.upslist:
                logging.info(ups)
                try:
                    apiURL = f"http://{self.apiHost}:{self.apiPort}/api/data/add/{ups}"
                    logging.debug(f"API URL: {apiURL}")
                    data = self.nutclient.list_vars(ups)
                    logging.debug(f"UPS Data Returned: {json.dumps(data)}")
                    request = requests.post(apiURL, json=data)
                    logging.debug(f"RESPONSE: {request.text}")
                except Exception as error:
                    logging.debug(f"An Error Has Occcured:")
                    logging.info(f"{error}")
            logging.debug(self.upslist)
            sleep(self.interval)

    def initialize(self):
        init = requests.get('https://localhost/api/init')
        return init

class flaskserver:
    def __init__(self,cla):
        self.cla = cla

def commandLineArgs():
        cla = argparse.ArgumentParser(description="Starts nutclient and nutui flask server")
        cla.add_argument('-v','--verbose',required=False,action='store_true',default=False,
                            help="Verbose Output")
        cla.add_argument('-c','--client',required=False,action='store_true',default=False,
                            help="Runs nutclient only.  Disables the flask server")
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
        return vars(cla.parse_args())

if __name__ == "__main__":
    clArgs = commandLineArgs()

    nutui(client=clArgs['client'],
        nutHost=clArgs['nuthost'],
        login=clArgs['nutlogin'],
        password=clArgs['nutpassword'],
        debug=clArgs['verbose'],
        interval=clArgs['interval'],
        apiHost=clArgs['apihost'],
        apiPort=clArgs['apiport']
        )
    while True:
        sleep(5)
        logging.debug(f"Heartbeat: {time()}")