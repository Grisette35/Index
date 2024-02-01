import nltk
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')  # Make sure to download the punkt tokenizer if you haven't already

# Initialize the Snowball Stemmer for French
stemmer = SnowballStemmer('french')

# Example sentence
sentence = "Les chats sont en train de manger des croquettes."

# Tokenize the sentence
words = word_tokenize(sentence)

# Apply stemming to each word
stemmed_words = [stemmer.stem(word) for word in words]

# Print the original words and their stems
for original, stemmed in zip(words, stemmed_words):
    print(f"{original} -> {stemmed}")
