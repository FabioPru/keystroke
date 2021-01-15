#sample usage ./iterate_JSON node hello

outlocation="../../src/preprocess/"

echo "Initialized accumulator.out and sentences/keystrokes.csv"

echo "0" > accumulator.out

cat ../../pads/empty_csv/sentences.csv > ./sentences.csv
cat ../../pads/empty_csv/keystrokes.csv > ./keystrokes.csv

for sem in ../preprocess/data/*.json; do
  echo "inspecting $sem"

	prefix=${sem%?????}

	cd ../sh

	echo "		Creating df.json, ops.json and l"
	node ./../js/changelog_parser.js "$sem"

	python3 ./../py/genList.py $prefix > "${prefix}l.out"

	echo "		Converting l to keystroke.csv"
	echo "t,end_t,char,pos,op,path" > "${prefix}keystroke.csv"
	../cpp/a.out < "${prefix}l.out" >> "${prefix}keystroke.csv"

	python3 ./../py/genTxt.py $prefix > "${prefix}.txt"

	echo "		Running Stanford CoreNLP"
	cd ../java/stanford-corenlp
	echo "text,start_pos,end_pos,path" > "../${prefix}sentence.csv"
	java -cp "*" getSentences.java "../${prefix}.txt" >> "../${prefix}sentence.csv" 2> /dev/null 
	cd ../../preprocess

	sed -i -e 's/"/""/g' "${prefix}sentence.csv"
	sed -i -e 's/£/"/g' "${prefix}sentence.csv"

	echo "		Running single-file preprocessing"
	id_start=`cat accumulator.out`
	python3 ./../py/singleFilePreprocessing.py "${prefix}" "${outlocation}" "${id_start}"

	rm "${prefix}df.json"
	rm "${prefix}ops.json"
	rm "${prefix}l.out"
#	rm "${prefix}keystroke.csv"
#	rm "${prefix}sentence.csv"	
	rm "${prefix}sentence.csv-e"	
	echo "		Done"

done

rm accumulator.out

echo "############ Computing summary statistics for all the data processed"
echo "** To compute additional basic metrics at this point,"
echo "    add code to /py/postprocess.py at lines 40+"
#mkdir ../../frontend/files
python3 ./../py/postprocess.py "${outlocation}"
echo "Done"

#echo "############ Running CoCoGen"
#cd ../../frontend/
#./iterate.sh
#cd ../src/preprocess/

#echo "s_id,f_id,Syntactic.ClausesPerSentence_value,Syntactic.DependentClausesPerSentence_value,Syntactic.CoordinatePhrasesPerSentence_value,Syntactic.VerbPhrasesPerSentence_value,Syntactic.ComplexNominalsPerSentence_value,NounPhrasePreModificationWords_value,NounPhrasePostModificationWords_value,Lexical.Sophistication.NAWL_value,Lexical.Sophistication.NGSL_value,Lexical.Sophistication.AFL_value,Lexical.Sophistication.ANC_value,Lexical.Sophistication.BNC_value,Lexical.Density_value,Lexical.Diversity.NDW_value,Lexical.Diversity.CNDW_value,Lexical.Diversity.TTR_value,Lexical.Diversity.CTTR_value,Lexical.Diversity.RTTR_value,Morphological.MeanSyllablesPerWord_value,Morphological.MeanLengthWord_value,KolmogorovDeflate_value,Morphological.KolmogorovDeflate_value,Syntactic.KolmogorovDeflate_value
#" > cocogen.csv
#cat ../../frontend/cocogen.csv >> cocogen.csv
#rm -r "../../frontend/files"
#rm ../../frontend/cocogen.csv
#rm ../../frontend/output.csv
#echo "Done"

#echo "############ Merging"
#python3 ./../py/merge.py "${outlocation}"
#rm cocogen.csv
#echo "Done"

