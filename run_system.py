import subprocess
import os

PATH = "./elfs"

subprocess.call('rm results.csv', shell=True)
for i in os.listdir(PATH):
	file = os.path.join(os.path.join(os.getcwd(), PATH), i)
	print(file)
	subprocess.call("python ELFMiner.py " + "'" + file + "'", shell=True)

subprocess.call("mv results.csv system/final.csv", shell=True)
subprocess.call("cd system && make", shell=True)