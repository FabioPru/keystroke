#sample usage ./iterate_JSON node hello

echo "Initialized accumulator.out and sentences/keystrokes.csv"

echo "0" > accumulator.out

rm ../../pads/sentences.csv
rm ../../pads/keystrokes.csv

cat ../../pads/empty_csv/sentences.csv > ../../pads/sentences.csv
cat ../../pads/empty_csv/keystrokes.csv > ../../pads/keystrokes.csv
