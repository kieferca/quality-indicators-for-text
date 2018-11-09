package de.uni_stuttgart.gsame.main;



import opennlp.tools.chunker.ChunkerME;
import opennlp.tools.chunker.ChunkerModel;
import opennlp.tools.cmdline.parser.ParserTool;
import opennlp.tools.namefind.NameFinderME;
import opennlp.tools.namefind.TokenNameFinderModel;
import opennlp.tools.parser.Parse;
import opennlp.tools.parser.ParserFactory;
import opennlp.tools.parser.ParserModel;
import opennlp.tools.parser.chunking.Parser;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.util.Span;
import java.io.IOException;
import java.io.InputStream;
import java.io.FileInputStream;
import java.util.ArrayList;



public class ConfidencesParsable {

  public static void main(String[] args) throws Exception {
	    
	   
	  //store sentences in descriptions
	  ArrayList<String> descriptions = new ArrayList<String>();
	  //descriptions.add("This is an example sentence to analyze.");
	  descriptions.add("Thisss is n e+++-mple sntence to an.-ze.");
	 	  
	  int numUncompleteParses = 0;
	
	 	  
	  ArrayList<Double> tokenizerProbs = new ArrayList<Double>();
	  ArrayList<Double> posProbs = new ArrayList<Double>();
	  ArrayList<Double> neProbs = new ArrayList<Double>();
	  ArrayList<Double> chunkProbs = new ArrayList<Double>();
	  ArrayList<Double> parseProbs = new ArrayList<Double>();
	  ArrayList<Double> thisPosSequenceProbs = new ArrayList<Double>();
	  
	  
	  
	  // use models from http://opennlp.sourceforge.net/models-1.5/ 
	  System.out.println("Loading Models ...");
	  
	  
	  InputStream modelIn = new FileInputStream("models/en-token.bin");
	  //uncomment and use german models if needed
	 // InputStream modelIn = new FileInputStream("models/de-token.bin");
	  
	 TokenizerModel model = null;
	  try {
	    model = new TokenizerModel(modelIn);
	  }
	  catch (IOException e) {
	    e.printStackTrace();
	  }
	  finally {
	    if (modelIn != null) {
	      try {
	        modelIn.close();
	      }
	      catch (IOException e) {
	      }
	    }
	  }
	  
	  InputStream modelNE = new FileInputStream("models/en-ner-person.bin");
	  TokenNameFinderModel model1 = null;

	  try {
	    model1 = new TokenNameFinderModel(modelNE);
	  }
	  catch (IOException e) {
	    e.printStackTrace();
	  }
	  finally {
	    if (modelNE != null) {
	      try {
	    	  modelNE.close();
	      }
	      catch (IOException e) {
	      }
	    }
	  }
	  
	  InputStream modelTag = null;
	  POSModel model2 = null;
	  try {
		//  modelTag = new FileInputStream("models/de-pos-maxent.bin");
		  modelTag = new FileInputStream("models/en-pos-maxent.bin");
	      model2 = new POSModel(modelTag);
	  }
	  catch (IOException e) {
	    // Model loading failed, handle the error
	    e.printStackTrace();
	  }
	  finally {
	    if (modelTag != null) {
	      try {
	    	  modelTag.close();
	      }
	      catch (IOException e) {
	      }
	    }
	  }
	  
	  InputStream modelC = null;
	  ChunkerModel model3 = null;
  
	  try {
		    modelC = new FileInputStream("models/en-chunker.bin");
	
		    model3 = new ChunkerModel(modelC);
		  } catch (IOException e) {
		    // Model loading failed, handle the error
		    e.printStackTrace();
		  } finally {
		    if (modelC != null) {
		      try {
		        modelC.close();
		      } catch (IOException e) {
		      }
		    }
		  }
	  
	 
	  
	  InputStream modelP = new FileInputStream("models/en-parser-chunking.bin");
	  ParserModel model4 = null;
	 
	  try {
		     model4 = new ParserModel(modelP);
		  }
		  catch (IOException e) {
		    e.printStackTrace();
		  }
		  finally {
		    if (modelP != null) {
		      try {
		    	  modelP.close();
		      }
		      catch (IOException e) {
		      }
		    }
		  }
	  
	  System.out.println("Starting calculations!");
	  
		  
		  for(String sentence : descriptions){ //format of descriptions: one sentence per line			  	 	  
		
			  Tokenizer tokenizer = new TokenizerME(model);
			  String tokens[] = tokenizer.tokenize(sentence);  
			  double tokenProbs[] = ((TokenizerME) tokenizer).getTokenProbabilities();
			  double sumTokenProbs = 0;
			  for (double d : tokenProbs) sumTokenProbs += d;
			  double averageTokens = sumTokenProbs / tokenProbs.length;
			  tokenizerProbs.add(averageTokens);
			
			 
			  NameFinderME nameFinder = new NameFinderME(model1);
			  Span nameSpans[] = nameFinder.find(tokens);
			  double[] probsNE = nameFinder.probs();
			  nameFinder.clearAdaptiveData();
			  double sumName = 0;
			  for (double d : probsNE) sumName += d;
			  double averageName = sumName / probsNE.length;			
			  neProbs.add(averageName);
			    
			   
			  		  
			  POSTaggerME tagger = new POSTaggerME(model2);
			  String tags[] = tagger.tag(tokens);			  		  
			  double probsPOS[] = tagger.probs();			  
			  double sumPOS = 0;
			  for (double d : probsPOS) sumPOS += d;
			  double averagePOS = sumPOS / probsPOS.length;			  
			  posProbs.add(averagePOS);	  
			  
			 	  
				
			  ChunkerME chunker = new ChunkerME(model3);
			  String tag[] = chunker.chunk(tokens, tags);			  
			  Span tagSpans[] = chunker.chunkAsSpans(tokens, tags);			  
			  double probsChunk[] = chunker.probs();			  
			  double sumCh = 0;
			  for (double d : probsChunk) sumCh += d;
			  double averageCh = sumCh / probsChunk.length;			  
			  chunkProbs.add(averageCh);
			 
			  Parser parser = (Parser) ParserFactory.create(model4);
			  Parse topParses[] = ParserTool.parseLine(sentence, parser, 1);		
			  
			  for(Parse p : topParses){
				  //p.show();
				  double probParse = p.getProb();
				  double probParseTagSequence = p.getTagSequenceProb();
				  parseProbs.add(probParse);
				  thisPosSequenceProbs.add(probParseTagSequence);
				  if(!p.complete()){
					  numUncompleteParses++;
				  }
				  

			  }
		  }	  
		  
		    
	  
	  double sumT = 0;
	  for (double d : tokenizerProbs) sumT += d;
	  double averageT = sumT / tokenizerProbs.size();
	  
	  double sumPOS = 0;
	  for (double d : posProbs) sumPOS += d;
	  double averagePOS = sumPOS / posProbs.size();
	  
	  double sumNE = 0;
	  for (double d : neProbs) sumNE += d;
	  double averageNE = sumNE / neProbs.size();
	  
	  double sumCh = 0;
	  for (double d : chunkProbs) sumCh += d;
	  double averageCh = sumCh / chunkProbs.size();
	  
	  double sumP = 0;
	  for (double d : parseProbs) sumP += d;
	  double averageP = sumP / parseProbs.size();
	  
	  double sumS = 0;
	  for (double d : thisPosSequenceProbs) sumS += d;
	  double averageS = sumS / thisPosSequenceProbs.size();
	  
	  System.out.println();
	  System.out.println("Number of sentences:" + "\t" + descriptions.size());
	  System.out.println("Confidence of Tokenizer:" + "\t" + averageT);
	  System.out.println("Confidence of POS Tagger:" + "\t" + averagePOS);
	  System.out.println("Confidence of NER:" + "\t" + averageNE);
	  System.out.println("Confidence of Chunker:" + "\t" + averageCh);
	  System.out.println("Probability of best parse:" + "\t" + averageP);
	  System.out.println("Probability of this tag sequence:" + "\t" + averageS);
	  System.out.println("Number of uncomplete parses:" + "\t" + numUncompleteParses);
	  
	  
	  
    System.out.println("Done!");
  }
}


