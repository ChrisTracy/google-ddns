import logging
logging.basicConfig(filename='googledyndns.log',level=logging.INFO)

import requests
import socket
import time
import os

username = os.environ['USER']
password = os.environ['PASS']
host = os.environ['URL']
try:
    sleep = os.environ['WAIT']
    sleep = int(sleep)
    logging.info("Sleep set to %s" %(sleep))
except:
    sleep = 120
    logging.info("Sleep not set. default is %s" %(sleep))

PubIP = ""
resolve = ""
base_url = ""

def run():
    def GetPubIP():
        try:
            global PubIP
            global base_url
            PubIP = requests.get('https://domains.google.com/checkip').text
            base_url = f'https://{username}:{password}@domains.google.com/nic/update?hostname={host}&myip={PubIP}'
        except Exception:
            logging.warning("Unable to get public IP. Check internet connection")
            time.sleep(sleep)
            GetPubIP()

    def GetHost():
        try:
            global resolve
            resolve = (socket.gethostbyname(host))
        except Exception:
            logging.info("Setting DNS record for the first time.")
            global base_url
            requests.get(base_url)
            time.sleep(sleep)

            def checkSet():
                try:
                    resolve = (socket.gethostbyname(host))
                except Exception:
                    logging.info("Wating for DNS replication. Verify that the DNS record is set to your public IP in Google Domains. This could take 15 minutes...")
                    time.sleep(sleep)
                    checkSet()
            checkSet()

    def ChangeIP():
        if PubIP == resolve:
            logging.info("IP check passed")
        else:
            logging.info("Changing Public IP to", PubIP)
            global base_url
            requests.get(base_url)

    GetPubIP()
    GetHost()
    ChangeIP()
    time.sleep(sleep)

while True:
    run()