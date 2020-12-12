## Source code description

All the work on data is in the /ipynb/ folder. Please refer to the README in that folder for more information. Everything else here is for preprocessing the data from the weird format it was in into something usable.

## Preprocessing tool

If you ever need to preprocess some file from anew use this command

 ./preprocess.sh "../../pads/raw/1.json"
 
 from the /src/sh/ folder. This expects both a .json and a .txt files with the same name at the specified location. You can use iterateJSON.sh if you need to iterate over folders of json files.
