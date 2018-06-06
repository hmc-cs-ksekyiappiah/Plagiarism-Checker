from argparse import *
from string import punctuation
from itertools import chain


class PlagiarismDetector:
    """
    Class to detect and compute the percentage of text plagiarized 
    when comparing two text files
    """

    def __init__(self, synonyms, file_one, file_two, tuple_size):
        """ Constructor for the class.
            Takes in the synonyms file, first and second files and 
            the optional tuple size as arguments.
            Prepares all maps and lists of files
        """

        if tuple_size <= 0:
            raise Exception("Tuple size must exceed 0")

        self.tuple_size = tuple_size
        self.synonyms = self.map_of_synonyms(synonyms)
        self.file_one = self.map_of_tuples(file_one)
        self.file_two = self.list_of_tuples_from_word_list(self.words_in_file(file_two))

    def words_in_file(self, file_path):
        """ Returns list of words from the file. """
        with open(file_path, 'r') as path:
            return list(chain.from_iterable(line.split() for
                        line in path if line.rstrip()))

    def get_plagiarized_percentage(self):
        """ Returns the percetage plagiarized when comparing file_two
        file with file_one """

        SIZE = len(self.file_two)
        total_plagiarized_phrases = 0
        for tupl in self.file_two:
            if tupl in self.file_one:
                total_plagiarized_phrases += 1

        total_plagiarized_phrases = float(total_plagiarized_phrases)

        if SIZE == 0:
            return 0 
        else:
            plagiarized_percentage = (total_plagiarized_phrases / SIZE) * 100
        return plagiarized_percentage

    def map_of_tuples(self, file_path):
        """ Returns a map of all the tuples given file """

        list_of_words = self.words_in_file(file_path)
        list_of_phrases = self.list_of_tuples_from_word_list(list_of_words)
        return self.map_of_tuples_with_true_value(list_of_phrases)

    def map_of_tuples_with_true_value(self, phrases):
        """ Returns a map of tuples with values set as True
        by going through a list of tuples. """

        tuples_map = {}
        for phrase in phrases:
            tuples_map[phrase] = True
        return tuples_map

    def list_of_tuples_from_word_list(self, words):
        """ Returns a list of tuples obtained from a list of words that have
        gone through the check of being a possible synonym. """

        SIZE = len(words)

        """ Creates the first iteration of tuple_size from the list of words. """
        list_of_words = [self.get_synonym(word) for word
                         in words[:self.tuple_size]]
        tuples_list = [tuple(list_of_words)]

        """ After the first iteration, it repeatedly does the ff until it 
            reaches the last element in the list:
        - it takes the next word from the list
        - checks to see if it can be converted to a synonym
        - appends to the back of list
        - pops the first word in the list
        - creates a tuple of the list of words
        - and finally appends this list of words tuple to the tuples list 

        It then returns the tuples list"""

        for index in xrange(self.tuple_size, SIZE):
            end_word = words[index]
            end_word = self.get_synonym(end_word)
            list_of_words.append(end_word)
            list_of_words.pop(0)
            phrase_list = tuple(list_of_words)
            tuples_list.append(phrase_list)

        return tuples_list

    def map_of_synonyms(self, file_path):
        """ Returns a map with synonyms as keys and have their first respective synonym 
            as a value
        """
        synonym_map = {}
        with open(file_path, 'r') as file:
            for line in file:
                words = line.split()
                synonym_word = words[0]
                for word in words:
                    synonym_map[word] = synonym_word

        return synonym_map

    def get_synonym(self, word):
        """ Gets the synonym of a word by first checking if that word is in the synonym map. 
            If it's inside, it returns the respective synonym. 
        """
        if word in self.synonyms:
            word = self.synonyms[word]
        return word



def main():
    """ Takes in flags with corresponding arguments as follows: 
    -s is followed by the synonym dictionary
    -f is followed by the file path of the file1
    -ff is followed by the file path of file2
    -t is follwed by the tuple size and is set to 3 by default if not included 

    Returns the percetage plagiarized"""

    parser = ArgumentParser()
    parser.add_argument('-s', required=True, help='the file path of synonym dictionary')
    parser.add_argument('-f', required=True,  help='the file path of file 1')
    parser.add_argument('-ff', required=True, help='the file path of file 2')
    parser.add_argument('-t', type=int, help='the tuple size', default=3)
    parser = parser.parse_args()

    p = PlagiarismDetector(parser.s, parser.f, parser.ff, parser.t)

    print ("Percentage of text plagiarized is: %.1f%% " % p.get_plagiarized_percentage())


if __name__ == '__main__':
    main()