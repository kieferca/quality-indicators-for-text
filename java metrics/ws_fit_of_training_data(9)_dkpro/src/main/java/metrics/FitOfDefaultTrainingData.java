package metrics;




import java.util.ArrayList;
import dkpro.similarity.algorithms.api.SimilarityException;
import dkpro.similarity.algorithms.api.TextSimilarityMeasure;
import dkpro.similarity.algorithms.lexical.string.CosineSimilarity;





public class FitOfDefaultTrainingData {

	public static void main(String[] args) {
		
			
        // this similarity measure is defined in the dkpro.similarity.algorithms.lexical-asl package	
		TextSimilarityMeasure measure = new CosineSimilarity();    // Use cosine similarity

		
		ArrayList<String> tokens1 = new ArrayList<String>(); //add operational text tokens here
		ArrayList<String> tokens2 = new ArrayList<String>(); //add default, e.g., treebank tokens here
		
		tokens1.add("This");   
		tokens1.add("is");   
		tokens1.add("an");   
		tokens1.add("example"); 
		
			
		tokens2.add("This");   
		tokens2.add("is");   
		tokens2.add("a");   
		tokens2.add("example"); 
		
		try {
			double score = measure.getSimilarity(tokens1, tokens2);
			System.out.println(score);
		} catch (SimilarityException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		
        
	}

}
