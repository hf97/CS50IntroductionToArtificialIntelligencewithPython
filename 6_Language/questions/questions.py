import nltk
nltk.download('stopwords')
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), encoding="utf-8") as f:
            # save content in dic
            dic[file] = f.read()
    return dic


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # to lower case
    document_lower = document.lower()
    # tokenize
    words = nltk.word_tokenize(document_lower)
    list = [x for x in words if x not in string.punctuation and x not in nltk.corpus.stopwords.words("english")]
    return list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf = dict()
    for file in documents:
        checked_word = set()
        for word in documents[file]:
            if word not in checked_word:
                checked_word.add(word)
                try:
                    idf[word] += 1
                # whithout except gives a error
                except KeyError:
                    idf[word] = 1
    return {word: math.log(len(documents) / idf[word]) for word in idf}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    top = {}
    for file in files:
        top[file] = 0
        for word in query:
            # add to dic idf
            top[file] += files[file].count(word) * idfs[word]
    return [k for k, v in sorted(top.items(), key=lambda x: x[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    score = list()
    for sentence in sentences:
        values = [sentence, 0, 0]
        for word in query:
            if word in sentences[sentence]:
                values[1] += idfs[word]
                values[2] += sentences[sentence].count(word) / len(sentences[sentence])
        score.append(values)
    return [sentence for sentence, _, _ in sorted(score, key=lambda item: (item[1], item[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
