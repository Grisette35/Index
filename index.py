import json
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def word_tokenize_fr(text):
    return [token.lower() for token in word_tokenize(text,language='french')]

# Load the JSON data
with open('crawled_urls.json', 'r') as file:
    data = json.load(file)

# Create an index for title tokens
title_index = defaultdict(list)

# Tokenize and create the index
for index, entry in enumerate(data):
    title_tokens = word_tokenize_fr(entry['title'])
    for token in title_tokens:
        title_index[token].append(index)

# Convert defaultdict to a regular dictionary
title_index_dict = dict(title_index)

# Save the index to a JSON file
with open('title.non_pos_index.json', 'w') as index_file:
    json.dump(title_index_dict, index_file, indent=None)#, separators=(",\n",": "))

# Display the index
#print(title_index_dict[0])