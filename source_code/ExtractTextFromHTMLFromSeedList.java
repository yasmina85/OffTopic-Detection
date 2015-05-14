package source_code;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.xml.sax.SAXException;

import de.l3s.boilerpipe.BoilerpipeProcessingException;
import de.l3s.boilerpipe.extractors.*;


public class ExtractTextFromHTMLFromSeedList {

	/**
	 * @param args
	 * @throws BoilerpipeProcessingException 
	 * @throws IOException 
	 * @throws SAXException 
	 */
	public static void main(String[] args) throws BoilerpipeProcessingException, IOException, SAXException {
//		int[] collection_ids = {1475,  694,  2966 ,3015 ,2535 ,335 ,2017 ,1582 ,823 ,639 ,459 , 1945} ;
			
			if(args.length < 2){
				System.out.println("Usage extract_text [timemap_file] [collection_directory]");
				System.exit(1);
			}
			
			String timemap_file = args[0];
		    String collection_directory = args[1];
		    String[] types={"default","canola"};
		    
		    
		    for (String type : types) {
			
			    String text_dir="";
			    if(type.equalsIgnoreCase("default")){
				    text_dir = collection_directory+"/text/";
			    } else if(type.equalsIgnoreCase("canola")){
				    text_dir = collection_directory+"/text_canola/";
		
			    } 
			    
				BufferedReader timemap_reader = new BufferedReader(new FileReader(timemap_file));
		
				while(timemap_reader.ready()){
					
					String line = timemap_reader.readLine();
					String[] fields = line.split("\t");
					String uri_id = fields[0];
					String dt = fields[1];
							
					File htmlFile = new File(collection_directory+"/html/"+uri_id+"/"+dt+".html");
					if(!htmlFile.exists()){
											
						continue;
					}
					
					File file = new File(text_dir);
					if (!file.exists()) {
						file.mkdir();
					}
								
					File textFile = new File(text_dir+uri_id+"/"+dt+".txt");
					textFile.getParentFile().mkdirs();
					BufferedReader reader = new BufferedReader(new FileReader(htmlFile));
						
					StringBuffer htmlBuffer = new StringBuffer();
					while(reader.ready()){
						htmlBuffer.append(reader.readLine()+"\n");
					}
					reader.close();
					String text ="";
				   if(type.equalsIgnoreCase("default")){
					   text = KeepEverythingExtractor.INSTANCE.getText(htmlBuffer.toString());
				    } else if(type.equalsIgnoreCase("canola")){
				    	text = CanolaExtractor.INSTANCE.getText(htmlBuffer.toString());
		
				    } 
					    
					//String facebookPage = "";
					//if(host.equalsIgnoreCase("facebook")){
					//	facebookPage = parseFacebookPage(htmlBuffer.toString());
					//}
					
					BufferedWriter writer = new BufferedWriter(new FileWriter(textFile));
					writer.write(text);
					writer.close();
				}
				timemap_reader.close();
				
			
		}
	}
	
	public static String parseFacebookPage(String htmlText){
		StringBuffer textBuffer = new StringBuffer();
		
		Document doc = Jsoup.parse(htmlText);
		Elements codes = doc.select("code");
		for(int j=0 ; j<codes.size();j++){
			Element code=codes.get(j);
			String html = code.html();
			if(html.startsWith("<!--")){
				html=html.substring(4);
				html = html.substring(0, html.length()-4);
			}
			
			Document subdoc = Jsoup.parse(html);
			textBuffer.append(subdoc.body().text());
			
			}
		
		return textBuffer.toString();

	}
}
