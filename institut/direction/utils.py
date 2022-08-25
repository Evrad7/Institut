import string
import random

def getPassword(nb):
	password=""
	for _ in range(nb):
		password+=random.choice(string.ascii_letters+string.digits)
	return password

