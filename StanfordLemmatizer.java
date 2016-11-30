import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.DependencyParseAnnotator;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;

public class StanfordLemmatizer {

    protected StanfordCoreNLP pipeline;

    public StanfordLemmatizer() {
        // Create StanfordCoreNLP object properties, with POS tagging
        // (required for lemmatization), and lemmatization
        Properties props;
        props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma, depparse");

        // StanfordCoreNLP loads a lot of models, so you probably
        // only want to do this once per execution
        this.pipeline = new StanfordCoreNLP(props);
    }
    
    public void depParse() {
    	String text = "I am feeling very sad and frustrated.";
//    	Properties props = new Properties();
//    	props.setProperty("annotators", "tokenize, ssplit, pos, lemma, parse, sentiment");
//    	StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    	Properties props;
    	Annotation document = new Annotation(text);
        props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma, depparse");
    	DependencyParseAnnotator stanDep = new DependencyParseAnnotator(props);
 
    	stanDep.annotate(document);
    	List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        for(CoreMap sentence: sentences) {
            // Iterate over all tokens in a sentence
            for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
                // Retrieve and add the lemma for each word into the list of lemmas
               System.out.println(token);
            }
        }
    }

    public List<String> lemmatize(String documentText)
    {
        List<String> lemmas = new LinkedList<String>();

        // create an empty Annotation just with the given text
        Annotation document = new Annotation(documentText);

        // run all Annotators on this text
        this.pipeline.annotate(document);

        // Iterate over all of the sentences found
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        for(CoreMap sentence: sentences) {
            // Iterate over all tokens in a sentence
            for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
                // Retrieve and add the lemma for each word into the list of lemmas
                lemmas.add(token.get(LemmaAnnotation.class));
            }
        }

        return lemmas;
    }
    public ArrayList<TaggedWord> POSTagger(String DocumentText) {
    	String[] sent = DocumentText.split(" ");
    	LexicalizedParser lp = LexicalizedParser.loadModel("edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz");
    	List<CoreLabel> rawWords = Sentence.toCoreLabelList(sent);
    	Tree parse = lp.apply(rawWords);
    	ArrayList ar=parse.taggedYield();
    	System.out.println(ar.toString());
		return ar;  
    }
}
