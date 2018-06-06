************************
Assumptions
************************

- The tuple size is always smaller than the word size per line of the file.
- All synonyms have to be on the same line.
- All the words in all files are in lowercase and are without any punctuation marks.

************************
Running the program
************************

```
python plagiarism.py -f file1.txt -ff file2.txt -s syns.txt -t 3

```
OR

```
python plagiarism.py -f file1.txt -ff file2.txt -s syns.txt 

```