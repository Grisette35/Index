import json
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from collections import defaultdict
from collections import Counter

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

class Index:
    def __init__(self, crawled_urls_json, columns_for_meta, columns_to_index):
        self.crawled_urls=crawled_urls_json
        self.columns_for_meta=columns_for_meta
        self.columns_to_index=columns_to_index
    
    def create_metadata(self):
        crawled_urls_pd=pd.read_json(self.crawled_urls)

        metadata={}

        nb_docs=len(crawled_urls_pd)

        metadata["The number of documents is:"]=nb_docs

        print(f"The number of documents in the crawled_urls.JSON file is: {nb_docs}")

        list_sum=[]

        for column in self.columns_for_meta:
            crawled_urls_pd[column + '_Tokens'] = crawled_urls_pd[column].apply(self.word_tokenize_fr)
            list_sum.append(crawled_urls_pd[column + '_Tokens'].apply(len).sum())

        #print(crawled_urls.head())

        total_nb_tokens=sum(list_sum)

        metadata["Total number of tokens"]=int(total_nb_tokens)
        print(f'Total number of tokens in the crawled_urls.JSON file (globally, meaning we have the tokens of the title, the content and the h1): {total_nb_tokens}')

        # Flatten the 'List_Column' and count occurrences of each number
        number_counts_list=[]
        for column in self.columns_for_meta:
            number_counts_list.append(Counter([token for sublist in crawled_urls_pd[column + '_Tokens'] for token in sublist]))

        # Convert the Counter to a DataFrame
        count_df_list = [pd.DataFrame.from_dict(number_counts, orient='index', columns=['Count']).reset_index() for number_counts in number_counts_list]

        # Rename columns for clarity
        count_df_list = [count_df.rename(columns={'index': 'Number'}) for count_df in count_df_list]

        for i in range(len(self.columns_for_meta)):
            metadata["Number of tokens in the field "+self.columns_for_meta[i]]=int(list_sum[i])
            metadata["Mean of the number of tokens in the field "+self.columns_for_meta[i]]=list_sum[i]/nb_docs
            metadata["Number of unique tokens in the field "+self.columns_for_meta[i]]=len(count_df_list[i])
            print(f"The number of tokens in the field {self.columns_for_meta[i]} is: {list_sum[i]}.")
            print(f"The mean of tokens in the field {self.columns_for_meta[i]} is: {list_sum[i]/nb_docs}.")
            print(count_df_list[i].sort_values(by='Count', ascending=False).head())

        with open('metadata.json', 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=1)#, separators=(",\n",": "))

    
    def word_tokenize_fr(self, text):
        return [token.lower() for token in word_tokenize(text,language='french')]
    

    #def word_stemming(self, text):
        #stemmer = SnowballStemmer('french')
        #text_tokenized = word_tokenize
        #stemmed_words = [stemmer.stem(word) for word in words]

    
    def create_index_one_field(self, data, column_to_index, stem_index):
        stemmer = SnowballStemmer('french')
        field_index = defaultdict(list)
        field_index_stem = defaultdict(list)

        field_index_pos = defaultdict(lambda: defaultdict(defaultdict))

        # Tokenize and create the index
        for doc, entry in enumerate(data):
            field_tokens = self.word_tokenize_fr(entry[column_to_index])

            if stem_index:
                field_stem=[stemmer.stem(word) for word in field_tokens]
                for stem in field_stem:
                    if doc not in field_index_stem[stem]:
                        field_index_stem[stem].append(doc)

            for token in field_tokens:
                if doc not in field_index[token]:
                    field_index[token].append(doc)
                    field_index_pos[token][doc]['positions']=[]
                    field_index_pos[token][doc]['count']=0
                field_index_pos[token][doc]['positions'].append(field_tokens.index(token))
                field_tokens[field_tokens.index(token)]=None
                field_index_pos[token][doc]['count']+=1

        
        # Convert defaultdict to a regular dictionary
        field_index_dict = dict(field_index)
        field_index_pos_dict=dict(field_index_pos)

        # Save the index to a JSON file
        with open(column_to_index+'.non_pos_index.json', 'w') as index_file:
            json.dump(field_index_dict, index_file, indent=None)#, separators=(",\n",": "))
        
        print(f"Index for {column_to_index} created in {column_to_index}.non_pos_index.json")

        # Save the index to a JSON file
        with open(column_to_index+'._pos_index.json', 'w') as index_file:
            json.dump(field_index_pos_dict, index_file, indent=None)#, separators=(",\n",": "))
        
        print(f"Index for {column_to_index} created in {column_to_index}._pos_index.json")
        
        if stem_index:
            # Convert defaultdict to a regular dictionary
            field_index_stem_dict = dict(field_index_stem)

            # Save the index to a JSON file
            with open("mon_stemmer."+column_to_index+'.non_pos_index.json', 'w') as index_file:
                json.dump(field_index_stem_dict, index_file, indent=None)
                
            print(f"Index for {column_to_index} stemmed created in mon_stemmer.{column_to_index}.non_pos_index.json")


    def create_index(self, index_for_content=False, stem_index=False):
        # Load the JSON data
        with open(self.crawled_urls, 'r') as file:
            data = json.load(file)
        
        self.create_index_one_field(data, self.columns_to_index[0], stem_index)
        
        if index_for_content:
            self.create_index_one_field(data, self.columns_to_index[1], stem_index)

if __name__=="__main__":
    index= Index("crawled_urls.json", ['title', 'content', 'h1'], ['title', 'content'])
    #index.create_metadata()
    index.create_index(False, True)