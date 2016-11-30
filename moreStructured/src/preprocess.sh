
python Preprocessing_for_adding_implicit_heads.py 
for f in data/problems_preprocessed/*.txt; do cp $f ../code/np_extract-master/problems; done
cd ../code/np_extract-master
export CLASSPATH=$CLASSPATH:/Users/amini91/Documents/Docs/UW/Research/tools/stanford-corenlp-full-2015-12-09/slf4j-simple.jar
export CLASSPATH=$CLASSPATH:/Users/amini91/Documents/Docs/UW/Research/tools/stanford-corenlp-full-2015-12-09/slf4j-api.jar
export CLASSPATH=$CLASSPATH:/Users/amini91/Documents/Docs/UW/Research/tools/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0.jar 
for f in problems/*; do  java edu.stanford.nlp.process.DocumentPreprocessor $f > $f\.ssplit ; done
for f in problems/*.ssplit; do java -jar easyccg.jar --model model -f $f > $f\.ccg; done
python3 np_extract.py
for f in problems/*.ssplit; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/data/spilit_preprocessed; done
for f in problems/*.ssplit.ccg; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/data/ccg_preprocessed; done
for f in problems/*.ssplit.ccg.nps; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/data/np_preprocessed; done

for f in problems/*.txt; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/moreStructured/src/lemmatizer; done
java Main.java ".txt" "_lemma.txt"
for f in problems/*.ssplit; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/moreStructured/src/lemmatizer; done
java Main.java ".txt.ssplit" "_lemma.txt.ssplit"
for f in problems/*.ssplit.ccg; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/moreStructured/src/lemmatizer; done
java Main.java ".txt.ssplit.ccg" "_lemma.txt.ssplit.ccg"
for f in problems/*.ssplit.ccg.nps; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/moreStructured/src/lemmatizer; done
java Main.java ".txt.ssplit.ccg.nps" "_lemma.txt.ssplit.ccg.nps"

for f in problems/*_lemma.txt; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/data/problems_preprocessed; done
for f in problems/*_lemma.txt.ssplit; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/data/spilit_preprocessed; done
for f in problems/*_lemma.txt.ssplit.ccg; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/data/ccg_preprocessed; done
for f in problems/*_lemma.txt.ssplit.ccg.nps; do cp $f /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/data/np_preprocessed; done