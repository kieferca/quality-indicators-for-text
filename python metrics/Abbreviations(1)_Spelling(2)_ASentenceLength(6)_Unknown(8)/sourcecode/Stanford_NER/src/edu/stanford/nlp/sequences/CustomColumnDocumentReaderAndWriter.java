package edu.stanford.nlp.sequences;

import java.io.PrintWriter;
import java.util.List;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;

public class CustomColumnDocumentReaderAndWriter extends ColumnDocumentReaderAndWriter {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -9153395839484378648L;

	@Override
	public void printAnswers(List<CoreLabel> doc, PrintWriter out) {
		for (CoreLabel wi : doc) {
			String answer = wi.get(CoreAnnotations.AnswerAnnotation.class);
			out.println(wi.word() + "\t" + answer);
		}
		out.println();
	}


}
