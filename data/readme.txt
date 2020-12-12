Welcome to the L2 keystroke dataset of RWTH Aachen. In this folder you will find the following files:

'users.csv':
-	'folder': folder in which user data is stored to preserve anonimity
-	'text_count': number of text files written by user
-	'keystroke_count': number of keystroke (including deletions) typed by user
-	'text_len_mean': average length of a text
-	't10000_mean': average time between keystrokes

'sentences.csv':
-	'user_id': id of the author
-	'file_path': path of the file the sentence belongs to
-	'text': full text of the sentence
-	'start_pos': position in the file at which the sentence starts
-	'end_pos': position in the file at which the sentence ends
-	'text_len': length of the sentence
-	'keystroke_count': number of keystrokes typed (including deletions)
-	'deletion_count': number of deletions
-	'word_count': number of space-separated words
-	't': total time spent writing the sentence
-	't10000': total time, except pauses longer than 10 seconds (breaks) are counted as being 10s long
-	'no_pauses_510': number of pauses above 510ms
-	'no_pauses_2000': number of pauses above 2000ms
-	'no_pauses_10000': number of pauses above 10000ms
-	'max_pause': longest pause, in ms
-	'jumps': number of times the user typed a character non-contiguously (e.g. fixing a previous mistake in the sentence)
-	'chunks': number of separate occasions the user edited the sentence in the entire writing/editing process
-	'word_t10000': time (filtered as above) spent writing word characters
-	'separator_t10000': time (filtered as above) spent writing punctuation and spaces
-	'revision_t10000': time spent revising, including deleting and re-writing text

'keystrokes.csv':
-	'sentence_id': id of the sentence
-	'user_id': id of the author
-	'file_path': path of the file the keystroke belongs to
-	'char': character typed, '' in case of deletion
-	'op': '+' for adding a new character, '-' for deleting
-	'position_in_file': position in the file of the character/deletion
-	'timestamp': in ms
-	't': time between previous and current keystroke