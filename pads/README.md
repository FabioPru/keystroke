# Clean data from pads

This folder contains cleaned .csv version of the data provided. The raw data is stored in the ./raw/ folder. Please mind that a significant portion of the data has been removed due to copy pastes, and has been severely cleaned in at least two ways:

1) Keystroke positions were shifted from (before) the position they occupied at the moment the keystroke was typed to (after) the position they occupy in the final file.

2) Multiple keystroke in the same Etherpad batch of 500ms were separated, by letting them be in their own batch of length 500/n.

For details about preprocessing, please consult the README in the ../src/ foder.

## List of files

Here are the files provided:

- keystrokes.csv (k): contains modified data about each keystroke in the database. Each has w_id, f_id etc. to be mapped to other dataframes/csvs.

- words.csv (w): contains info about each word. A word includes by convention all the whitespace/punctuation that comes BEFORE it (but not after), without crossing file boundaries.

- sentences.csv (s): contains info about each sentence as split by stanford-coreNLP. Includes whitespace BEFORE it (but not after), does not cross file boundaries.

- files.csv (f) and users.csv (u): basic aggregator info for files, users.

- n-gram/bigrams, bigrams-full: list of 2-grams. The full version includes all appearences, the base one ony those that appear >= 3 times in our data. Similarly for trigrams

- pcc.csv: Pearson Correlation Coefficients between pairs of CoCoGen and Keystroke Logging measures.

## Specification of each file

Below you can find rough specifications of each file and column. Please note that some additional columns might be present, we'll try to keep this list updated. Data from the corpus goes BEFORE statistics compute by us. We try to group everything as cleanly as possible. Refer to fabio's notebook for code that generates each column.

### keystrokes.csv

- w_id, ..., u_id: indexes of the word, ..., user the keystroke belongs to in the other files.

- path: shortened version of the path in which you can find the file in the /raw/ folder

- char: char typed. Might not be unicode-compliant. Use encoding 'latin1' with pandas. Is NaN in case of deletions.

- pos: position of the char in the final file. First char has position 0. If deleted, position at which the replacement character is in the final file. If multiple deletions, they all get stored in the first char that lives to the end. Might not be fully accurate due to difficulties in copy-paste preprocessing.

- type: whether the char is within a word, between words etc. See Joo's paper for details.

- t: time in milliseconds from the prev keystroke to when this was typed. As etherpad only records every 500ms, we had to split multiple chars in the same 500ms in two keystrokes of 250ms etc. So values <500ms are not exact.

- end_t: unix timestamp of the time the key is pressed.

- op: '+' for additions, '-' for deletions

- log_t, adjusted_log_t: log of 1+t; normalized user-wise to have mean 0 std 1

### words.csv
- s_id, f_id, u_id : sentence id, file id, user id

- start_pos, end_pos: includes whitespace and punctuation before but not after

- spell_err: whether word is not in the vocabulary

- word_freq: frequency of given word

- text_len: number of characters in word

- k_count: keystroke counts

- t/len_filter_x: {sum of ts, but if t > x, then t = x}/{text_len}

- max_p: maximum pause in word

- n_revisions: number of revisions made in the word

- part_of_speech: part of speech of words. For acronyms, see https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

### sentences.csv

- cols 0-7: basic info

- cocogen measures: refer to paper. We removed measures that were irrelevant/superfluous       

- 'n_'+something: for measures that depended linearly on text_length, we normalized by taking mean and std of sentences with same text len. They now have mean 0 std 1       

- word, keystroke count. k/len is almost like revision/len       

- t_filter_x: sum of ts, but if t > x, then t = x 

- p_x_no: number of pauses at or above x   

- 'max_t', 'max_pos', 'max_pos_pct': time and position fo the max t. pct: where in the sentence it happens
       
- 't/len_filter_2000', 't/len_filter_5000', 't/len_filter_10000', 't/len_filter_30000', 't/word_filter_10000', self explanatory

- 'fluency', 'latency': see fabios paper; 'adj_log_t/len', 'adj_log_t/sqrt_len', 'adj_log_t/sqrt_k': intermediate steps, you can ignore

- 't_first_2', 't_first_5','t_first_20' time for the first keystrokes in the sentence

- 't/len_0_fraction', etc: percentage of time spent in the first tenth of the sentence. use together to get distribution of pauses over the length

- 'del_t', 'del_t_filter_10000', 'del_t/t_filter_10000', 'del_count', 'del/len': deletion data
       
- 'jumps', 'chunks' see fabios paper
       
- revision is all time except the time spent on the first draft. Word time is inside the word, separators is on spaces and punctuation.

### users.csv

- All things are simple averages over things written by user

### burst_bigram_frequency.csv

- burst_freq_x: average of log(1+bigram frequency) within burst over the file (ex. When given burst is {I am},{a smart person}, average of bigram frequencies of {I am}, {a smart}, {smart person})

- across_burst_freq_x: average of log(1+bigram frequency) across burst over the file (ex.When given burst is {I am},{a smart person}, bigram frequency of {am a} )

- (x is the pause threshold in milliseconds)

### burst_trigram_frequency.csv

- burst_freq_x: average of log(1+trigram frequency) within burst over the file

- across_burst_freq_x: average of log(1+trigram frequency) across burst over the file

### burstlength.csv

- avg_burst_len_x: average length of bursts in the file

- mean_p_x: mean pause time between bursts in the file

- med_p_x: median pause time between bursts in the file

- (x is the pause threshold in milliseconds)
 

### pcc.csv

- rows: CoCoGen complexity measures

- columns: Keystroke logging measures (from sentence dataframe)

- cell values: Pearson Correlation Coefficient (averaged across all files) for the given CCG and KL measures

- NOTE: using PCC, a correlation coefficient approaching 1 signifies strong positive correlation, approaching -1 signifies strong negative correlation, and 0 signifies no correlation. 

