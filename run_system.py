import subprocess
import os

PATH = "DATASET_MALWARE_BENIGN/anmolPaper/linux_clean"

for i in os.listdir(PATH):
	file = os.path.join(os.path.join(os.getcwd(), PATH), i)
	print(file)
	subprocess.call("python ELFMiner.py " + "'" + file + "'", shell=True)
