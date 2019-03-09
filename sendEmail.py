import smtplib
import sys
import getpass

def connect():
	print("Connectiong to server...")
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587) 	# Creating SMTP object
	if (smtpObj.ehlo()[0] == 250):					# Saying hello to the service
		print("Connection established.")									
	print("\n"+str(smtpObj.starttls()[1]))				# Encrypting connection

	# Login into your account
	email = input("\n\nLogin email address: ")
	password = getpass.getpass("Login password: ")

	smtpObj.login(email, password)						# Login into email account 
	return smtpObj, email

# Composing the subject title according to SMTP rules
def enterSubject():								
	subject = input("\nEnter subject of the email: ")

	subject += '\n'

	return subject

def composeBody():
	address = input("\nEnter addressing part: ")
	body = address+"\n"+input("\nEnter body here\n:")
	body += "\nThank you"

	return body

# Send email
def sendEmail(smtpObj, from_email, to_email, email):
	smtpObj.sendmail(from_email, to_email, email)

def main():
	smtpObj, from_email = connect()
	subject = enterSubject()
	body = composeBody()

	to_email = input("\n\nEnter recipient email: ")
	print("\nSending email...")
	email = subject + body

	sendEmail(smtpObj, from_email, to_email, email)

	print("\nSent")


if __name__ == '__main__':
	main()