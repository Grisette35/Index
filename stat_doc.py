import json
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

crawled_urls = pd.read_json("crawled_urls.json")

print(crawled_urls.head())

metadata={}

metadata["The number of documents in the crawled_urls.JSON file is:"]=len(crawled_urls)

print(f"The number of documents in the crawled_urls.JSON file is: {len(crawled_urls)}")

print(f"The different information we can have from the crawled_urls.JSON: {crawled_urls.columns}")

# Download the NLTK data for French tokenization
#nltk.download('punkt')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

# Sample French text
#text_french = "La tokenisation est le processus de découpage du texte en mots ou en sous-mots."

# Tokenize the French text
#tokens_french = word_tokenize(text_french, language='french')

# Print the tokens
#print(tokens_french)

def word_tokenize_fr(text):
    return [token.lower() for token in word_tokenize(text,language='french')]

columns_to_tokenize=["title", "content", "h1"]

for column in columns_to_tokenize:
    crawled_urls[column + '_Tokens'] = crawled_urls[column].apply(word_tokenize_fr)

print(crawled_urls.head())

list_sum=[]

for column in columns_to_tokenize:
    list_sum.append(crawled_urls[column + '_Tokens'].apply(len).sum())

total_nb_tokens=sum(list_sum)

metadata["Total number of tokens"]=int(total_nb_tokens)
metadata["Number of tokens in the field 'title'"]=list_sum[0]
metadata["Number of tokens in the field 'content'"]=list_sum[1]
metadata["Number of tokens in the field 'h1'"]=list_sum[2]

metadata["Number of tokens in the field 'title'"]=list_sum[0]/len(crawled_urls)
metadata["Number of tokens in the field 'content'"]=list_sum[1]/len(crawled_urls)
metadata["Number of tokens in the field 'h1'"]=list_sum[2]/len(crawled_urls)


print(f'Total number of tokens in the crawled_urls.JSON file (globally, meaning we have the tokens of the title, the content and the h1): {total_nb_tokens}')

print(f"The number of tokens in the field 'title' is: {list_sum[0]}.")
print(f"The number of tokens in the field 'content' is: {list_sum[1]}.")
print(f"The number of tokens in the field 'h1' is: {list_sum[2]}.")


print(f"The mean of tokens in the field 'title' is: {list_sum[0]/len(crawled_urls)}.")
print(f"The mean of tokens in the field 'content' is: {list_sum[1]/len(crawled_urls)}.")
print(f"The mean of tokens in the field 'h1' is: {list_sum[2]/len(crawled_urls)}.")


# Flatten the 'List_Column' and count occurrences of each number
number_counts_list=[]
for column in columns_to_tokenize:
    number_counts_list.append(Counter([token for sublist in crawled_urls[column + '_Tokens'] for token in sublist]))

# Convert the Counter to a DataFrame
count_df_list = [pd.DataFrame.from_dict(number_counts, orient='index', columns=['Count']).reset_index() for number_counts in number_counts_list]

# Rename columns for clarity
count_df_list = [count_df.rename(columns={'index': 'Number'}) for count_df in count_df_list]

# Display the count DataFrame
print(count_df_list[0].sort_values(by='Count', ascending=False).head())
print(count_df_list[1].sort_values(by='Count', ascending=False).head())
print(count_df_list[2].sort_values(by='Count', ascending=False).head())

metadata["Number of unique tokens in the field 'title'"]=len(count_df_list[0])
metadata["Number of unique tokens in the field 'content'"]=len(count_df_list[1])
metadata["Number of unique tokens in the field 'h1'"]=len(count_df_list[2])

with open('metadata.json', 'w') as metadata_file:
    json.dump(metadata, metadata_file, indent=1)#, separators=(",\n",": "))
