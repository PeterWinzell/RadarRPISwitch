import os
import time
import urllib3

# testing connection to the internet
# currently against google com
URL = "http://www.google.com"

def has_internetconnection():
    while True:
        http = urllib3.PoolManager()
        try:
            http.request('GET',URL,retries=False)
        except urllib3.exceptions.NewConnectionError as e:
            print(e)
            print("not connected to the internet")
            return False
        else:
            print("connected to the internet")
            return True
