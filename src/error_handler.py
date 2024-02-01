import os


file_name = os.getcwd() + "/error_log.txt"

class Error():

	def reset():
		file = open(file_name, "w")
		file.write("Begin Error Log:\n")
		file.close()

	def debug(text):
		Error.log("%%DEBUT%%"+text+"\n")

	def logln(text):
		Error.log(text+"\n")

	def log(text):
		file = open(file_name, "a")
		file.write(text)
		file.close()
