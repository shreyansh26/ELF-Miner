import java.io.BufferedReader;
import java.io.FileReader;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.classifiers.trees.RandomForest;
import weka.classifiers.trees.J48;
import weka.classifiers.rules.PART;
import weka.classifiers.rules.JRip;
import weka.core.SerializationHelper;
import weka.core.converters.ConverterUtils.DataSource;


public class evaluate {
	private static Instances getDataFromFile(String path) throws Exception{

	    DataSource source = new DataSource(path);
	    Instances data = source.getDataSet();

	    if (data.classIndex() == -1){
	        data.setClassIndex(data.numAttributes()-1);
	        //last attribute as class index
	    }

	    return data;    
	}
	
	public static double roundHalfDown(double d) {
	    return new BigDecimal(d).setScale(0, RoundingMode.HALF_DOWN)
	                            .doubleValue();
	}
	
	public static void main(String args[]) throws Exception {
		// Load models
		RandomForest rf = (RandomForest) SerializationHelper.read("../models/models/Random_Forest.model");
		J48 j48 = (J48) SerializationHelper.read("../models/models/J48.model");
		PART prt = (PART) SerializationHelper.read("../models/models/PART.model");
		JRip jrip = (JRip) SerializationHelper.read("../models/models/JRip.model");
		
		// Load headers from all.txt
		BufferedReader in = new BufferedReader(new FileReader("../arff_headers/all.txt"));
		String str;

		List<String> header_list = new ArrayList<String>();
		while((str = in.readLine()) != null) {
			header_list.add(str);
		}
		
		List<Integer> linenos = new ArrayList<Integer>();
		for(int i=3; i<=149; i++) {
			linenos.add(i);
		}
		
		// Modify headers of arff file
		Path path = Paths.get("final.arff");
	    List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
	    for(int i=0; i<linenos.size(); i++) {
		    lines.set(linenos.get(i)-1, header_list.get(i));
		    Files.write(path, lines, StandardCharsets.UTF_8);
	    }
	    
	    // Load test set
	    Instances testingdata = getDataFromFile("final.arff");
	    int s = testingdata.numInstances();

	    for(int i=0; i<s; i++) {
			// Make predictions
			double valuej48 = j48.classifyInstance(testingdata.instance(i));
			double valuepart = prt.classifyInstance(testingdata.instance(i));
			double valuerf = rf.classifyInstance(testingdata.instance(i));
			double valuejrip = jrip.classifyInstance(testingdata.instance(i));
			double final_val = (valuej48 + valuepart + valuerf + valuejrip)/4;
//			System.out.println(String.valueOf(final_val));
		    // get the name of the class value
		    String prediction = testingdata.classAttribute().value((int)roundHalfDown(final_val)); 
	
		    System.out.println("The predicted value of instance " + Integer.toString(i) + ": " + prediction);
	    }
	}
}