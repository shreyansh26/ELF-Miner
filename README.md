ELF Miner
=========

This is an approximate implementation of the ELF Miner framework as described in [this paper](https://link.springer.com/article/10.1007/s10115-011-0393-5). The difference being that this model aims to classify a given ELF as Malware or Benign but does not classify the Malware into the the five types as described in the paper. This is because of the limitations of the dataset used.

## Requirements
* [Python 2.7](https://www.python.org/download/releases/2.7.3/)
* [Java 8.0+](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* [WEKA-3.6 toolkit](https://sourceforge.net/projects/weka/files/weka-3-6/3.6.13/)
* [KEEL toolkit](https://sci2s.ugr.es/keel/download.php)

## Usage
1. The ELF files to be analyzed must be put into the folder **elfs**.
2. `pip install -r requirements.txt`
3. From the root of the project, run -
  `python run_system.py`

This prints the predicted class (Malware or Benign) for each ELF file in the same order as in the generated **final.csv** in the **elfs** folder.

## Steps involved
1. Run the ELF Miner framework for feature extraction on the given ELF files. The details of the dataset and the features that are extracted are explained in much detail in the presentation below. A total of 343 features are initially **342** features.
2. Perform some postprocessing on the CSV to convert values for certain attributes to a form suitable for applying Machine Learning.
3. Perform Feature Selection on the CSV file. The features to remove were determined using Information Gain. For this we used WEKA. The features to remove are given in `feature_selection/weka_features_toremove.txt`. These are the ones which have 0 Information Gain. This reduces the number of features to **147**.
4. Use the saved models (after training multiple classifiers using WEKA) to make predictions. The saved models and their details are present in `models` folder.

Two classes of classifiers have been used in the paper -  
1. Non-Evolutionary Classifiers
    * JRip
    * J48
    * PART
    * Random Forest
2. Evolutionary Classifiers
    * UCS
    * XCS
    * GAssist-Adi

For the Non-Evolutionary Classifiers we have used the WEKA toolkit and for the Evolutionary Classifiers we have used the KEEL toolkit. The accuracy of each of these classifiers (on 70-30 split of train-test split) is given in `keel/results/results.txt`.

However, the end-to-end system incorporates a voting classifier based only on the Non-Evolutionary classifiers, due to the availability of WEKA's Java API.

## Presentation   


<style>
.responsive-wrap iframe{ max-width: 100%;}
</style>

<div class="responsive-wrap">
<!-- this is the embed code provided by Google -->
  <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vT12_sI9gWoBe01UeGcgLKGAHX6WlK10x8wHjZSh3YbJPn1-_kY0SfPqxrqcp69jLl0dXk-2HBmhMbb/embed?start=false&loop=false&delayms=5000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
<!-- Google embed ends -->
</div>
