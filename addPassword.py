#! /anaconda3/bin/python

'''
	Script to add passwords for any account into a CSV file.
'''
import os
import sys
import csv
import pandas as pd
import pyminizip
import getpass
import zipfile

# Check if zip folder exists
def checkZipFileExists(zip_file):
	if os.path.exists(zip_file):
		return True
	return False

def checkFileExists(file_name):
	if os.path.exists(file_name):
		if os.path.isfile(file_name):
			return True
		else:
			return False
	return False

def createFile(file_name):
	if checkFileExists(file_name):
		print("File already exists.")
		return
	file = open(file_name, 'w')
	row = ['account', 'password']
	writer = csv.writer(file)
	writer.writerow(row)
	file.close()

# Initialize the files if they don't exist.
def initialize(file_name, zip_file):
	if (not checkFileExists(file_name)) and (not checkZipFileExists(zip_file)):
		print("First time, creating new file.")
		createFile(file_name)

	if checkZipFileExists(zip_file):
		print("ZIP folder exists, uncompressing the folder.")
		pwd = bytes(getpass.getpass("Enter password for zip file: "), 'utf-8')
		zFile = zipfile.ZipFile(zip_file)
		zFile.extractall(pwd=pwd)

# Check and create if file_name file do not exists
def checkFileExistsAndCreate(file_name):
	if os.path.exists(file_name):
		if os.path.isfile(file_name):
			print("File already exists adding password.")
			return
		else:
			print("A folder exists with similar name, new file will be created.")
	file = open('passwords.csv', 'w')
	row = ['account', 'password']
	writer = csv.writer(file)
	writer.writerow(row)
	file.close()

# Check if account name already exists in the file.
def isAccountExists(file_name, pwField):
	account, password = pwField
	try:
		data  = pd.read_csv(file_name)
		print(data)
		accounts = list(data['account'])

		if account in accounts:
			#print("Account %s already exists. Do you want to overwrite the exisiting one?"%account)
			return True
	except:
		print("No data exists in the file, returning False.")
	return False

# If account exists in the file, chaneg the field to new password
def changeField(file_name, pwField):
	data = pd.read_csv(file_name)
	ind = list(data['account']).index(pwField[0])

	account, password = pwField

	if account != data.loc[ind]['account']:
		print("Accont names mismatch. Exiting program")
		exit(1)

	data.loc[ind]['password'] = pwField[1]  				# Chnaged existing password to new password

	#writing into CSV file again

	data.to_csv(file_name, index = False)

# Add password field into passwords file
def addPwField(file_name, pwField):
	checkFileExistsAndCreate(file_name)
	accountExists = isAccountExists(file_name, pwField)

	if accountExists:
		print("Account %s already exists. Do you want to overwrite the exisiting one (Y/y)?"%pwField[0])
		user_inp = input()

		if user_inp == 'Y' or user_inp == 'y':
			changeField(file_name, pwField)
			print("Password to exisiting account %s changed"%pwField[0])
		else:
			print('No changes done.')
			exit(1)
	else:
		file = open(file_name, 'a')
		writer = csv.writer(file)
		writer.writerow(pwField)
		file.close()
		print('Password to %s account added'%pwField[0])

def setPassword(file_name):
	print("Compressing file.")
	compress_level = 2
	password = getpass.getpass("Enter password for zip file: ")
	pyminizip.compress(file_name, './', 'passwordZip.zip', password, compress_level)

def main():
	zip_file = 'passwordZip.zip'
	file_name = 'passwords.csv'
	#checkFileExistsAndCreate(file_name)

	initialize(file_name, zip_file)

	if len(sys.argv) != 3:
		print("Usage command: addPassword.py account_name password")
		exit(1)
	else:
		pwField = [sys.argv[1], sys.argv[2]]
		#print("Please check the details and confirm. Enter 'ok' to add else enter 'check' to re-enter. Enter 'q' to quit.")
		print("Account: %s,\t Password: %s\n"%(sys.argv[1], sys.argv[2]))
		addPwField(file_name, pwField)
		print("Password field is added.")

	setPassword(file_name)

	# Now remove the file that's been zipped.
	os.remove(file_name)

if __name__ == '__main__':
	main()
		