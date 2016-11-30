//import java.io.BufferedReader;
//import java.io.File;
//import java.io.FileNotFoundException;
//import java.io.FileReader;
//import java.io.FileWriter;
//import java.io.IOException;
//import java.util.ArrayList;
//import java.util.List;
//
//
//public class Main {
//	public static void main (String argv[]){
//		StanfordLemmatizer stanfordTool = new StanfordLemmatizer();
//		for(int i = 0; i < 140; i++) {
//			try {
//				BufferedReader in = new BufferedReader(new FileReader(new File(i + ".pos")));
//				FileWriter file = new FileWriter(i +"_lemma.pos");
//				String text = in.readLine();
//				while(text !=  null){
//					if (text == "")
//						break;	
//					List<String> lemmaRes = stanfordTool.lemmatize(text);
//					System.out.println(lemmaRes);
//					for (int j = 0; j < lemmaRes.size()-1; j++){
//						file.write(lemmaRes.get(j) + ' ' );
//					}
//					file.write(lemmaRes.get(lemmaRes.size() -1) + '\n');
//					text = in.readLine();
//					//this part is for subset or disjoint format
////					String[] textParts = text.split("	");
////					List<String> lemmaRes = stanfordTool.lemmatize(textParts[0]);
////					System.out.println(lemmaRes);
////					for (int j = 0; j < lemmaRes.size() - 1; j++){
////						file.write(lemmaRes.get(j) + ' ' );
////					}
////					System.out.println(i);
////					file.write(lemmaRes.get(lemmaRes.size() - 1) + "	" );
////					lemmaRes = stanfordTool.lemmatize(textParts[1]);
////					for (int j = 0; j < lemmaRes.size(); j++){
////						file.write(lemmaRes.get(j) + ' ' );
////					}
////					file.write("\n");
////					text = in.readLine();
//				}
//				file.close();
//			} catch (FileNotFoundException e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			} catch (IOException e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}
//		}
//	}
//
//}
// 
//
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.stanford.nlp.ling.TaggedWord;


public class Main {
	public static void main (String argv[]){
		String input_suffix = argv[1];
		String output_suffix = argv[2];
		StanfordLemmatizer stanfordTool = new StanfordLemmatizer();
		for(int i = 0; i < 140; i++) {
			try {
				BufferedReader in = new BufferedReader(new FileReader(new File(i+input_suffix)));
				FileWriter file = new FileWriter(i + output_suffix);
				String text = in.readLine();
				while(text !=  null){
					if (text == "")
						break;	
					List<String> lemmaRes = stanfordTool.lemmatize(text);
//					System.out.println(lemmaRes.get(0).toString().substring(1));
//					String[] parts = lemmaRes.get(0).toString().split(", ");
//					System.out.println(lemmaRes.size());
//					for (int j = 0; j < lemmaRes.size(); j++) {
//						file.write(lemmaRes.get(j).toString() + '\n');
//					}
					for (int j = 0; j < lemmaRes.size()-1; j++){
						file.write(lemmaRes.get(j) + ' ');
					}
					file.write(lemmaRes.get(lemmaRes.size() -1) + '\n');
					text = in.readLine();
					//this part is for subset or disjoint format
//					String[] textParts = text.split("	");
//					List<String> lemmaRes = stanfordTool.lemmatize(textParts[0]);
//					System.out.println(lemmaRes);
//					for (int j = 0; j < lemmaRes.size() - 1; j++){
//						file.write(lemmaRes.get(j) + ' ' );
//					}
//					System.out.println(i);
//					file.write(lemmaRes.get(lemmaRes.size() - 1) + "	" );
//					lemmaRes = stanfordTool.lemmatize(textParts[1]);
//					for (int j = 0; j < lemmaRes.size(); j++){
//						file.write(lemmaRes.get(j) + ' ' );
//					}
//					file.write("\n");
//					text = in.readLine();
				}
				file.close();
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

}
