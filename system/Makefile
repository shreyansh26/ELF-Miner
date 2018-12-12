run:
	python postprocessing.py
	python feature_selection.py
	java -cp ".:./weka.jar" weka.core.converters.CSVLoader final_feature_selection.csv > final.arff
	javac -cp ".:./weka.jar" evaluate.java
	java -cp ".:./weka.jar" evaluate