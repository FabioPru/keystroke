#sample usage ./preprocess path

prefix=${@%?????}
outlocation="../../pads/"

#echo "		Operating on: " $prefix

echo "		Creating df.json, ops.json and l"
node ./../js/changelog_parser.js "$@"

#echo "		Creating l"
python ./../py/genList.py $prefix > "${prefix}l.out"
rm "${prefix}df.json"
rm "${prefix}ops.json"

echo "		Converting l to keystroke.csv"
#cat "../../pads/empty_csv/keystroke.csv" > "${prefix}keystroke.csv"
../cpp/a.out < "${prefix}l.out" >> "${prefix}keystroke.csv"

echo "		Running Stanford CoreNLP"
cd ../java/stanford-corenlp
#cat "../../../pads/empty_csv/sentence.csv" > "../${prefix}sentence.csv"
java -cp "*" getSentences.java "../${prefix}.txt" >> "../${prefix}sentence.csv" 2> /dev/null 
cd ../../sh

sed -i -e 's/"/""/g' "${prefix}sentence.csv"
sed -i -e 's/£/"/g' "${prefix}sentence.csv"

echo "		Running single-file preprocessing"
id_start=`cat accumulator.out`
python ./../py/singleFilePreprocessing.py "${prefix}" "${outlocation}" "${id_start}"

##cat "${prefix}sentences.csv" >> "${outlocation}sentences.csv"
#rm "${prefix}l.out"

#rm "${prefix}keystroke.csv"
#rm "${prefix}sentence.csv"
#rm "${prefix}sentence.csv-e"

echo "		Done"
