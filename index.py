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
    def __init__(self, crawled_urls_json, columns):
        """
        Initializes the Index object.

        Parameters:
        - crawled_urls_json (str): The json file that contains the crawled webpages.
        - columns (list of str): The information that should be used to create the indexes and the metadata file. \
            Usually they are the 'title', the 'content' and 'h1'.
        """
        self.crawled_urls=crawled_urls_json
        self.columns=columns
    
    def create_metadata(self):
        """
        Creates the metadata file for the information specified in the initialization.
        """
        crawled_urls_pd=pd.read_json(self.crawled_urls)

        metadata={}

        nb_docs=len(crawled_urls_pd)

        metadata["The number of documents is:"]=nb_docs

        print(f"The number of documents in the crawled_urls.JSON file is: {nb_docs}")

        list_sum=[]

        for column in self.columns:
            crawled_urls_pd[column + '_Tokens'] = crawled_urls_pd[column].apply(self.word_tokenize_fr)
            list_sum.append(crawled_urls_pd[column + '_Tokens'].apply(len).sum())

        total_nb_tokens=sum(list_sum)

        metadata["Total number of tokens"]=int(total_nb_tokens)
        print(f'Total number of tokens in the crawled_urls.JSON file (globally, meaning we have the tokens of the title, the content and the h1): {total_nb_tokens}')

        # Flatten the 'List_Column' and count occurrences of each number
        number_counts_list=[]
        for column in self.columns:
            number_counts_list.append(Counter([token for sublist in crawled_urls_pd[column + '_Tokens'] for token in sublist]))

        # Convert the Counter to a DataFrame
        count_df_list = [pd.DataFrame.from_dict(number_counts, orient='index', columns=['Count']).reset_index() for number_counts in number_counts_list]

        # Rename columns for clarity
        count_df_list = [count_df.rename(columns={'index': 'Number'}) for count_df in count_df_list]

        for i in range(len(self.columns)):
            metadata["Number of tokens in the field "+self.columns[i]]=int(list_sum[i])
            metadata["Mean of the number of tokens in the field "+self.columns[i]]=list_sum[i]/nb_docs
            metadata["Number of unique tokens in the field "+self.columns[i]]=len(count_df_list[i])
            print(f"The number of tokens in the field {self.columns[i]} is: {list_sum[i]}.")
            print(f"The mean of tokens in the field {self.columns[i]} is: {list_sum[i]/nb_docs}.")
            print(count_df_list[i].sort_values(by='Count', ascending=False).head())

        with open('metadata.json', 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=1)#, separators=(",\n",": "))
    
    def create_index(self, index_for_content=False, stem_index=False):
        """
        Creates the different index using a helper function.

        Parameters:
        - index_for_content (bool): by default set to False. If set to True, indexes are created for content.
        - stem_index (bool): by default set to False. If set to True, indexes are created 
                            using the stems and not only the tokens.
        """
        # Load the JSON data
        with open(self.crawled_urls, 'r') as file:
            data = json.load(file)
        
        self.create_index_one_field(data, self.columns[0], stem_index)
        
        if index_for_content:
            self.create_index_one_field(data, self.columns[1], stem_index)

    
    def word_tokenize_fr(self, text, language='french'):
        """
        Enables to tokenize text and to lowerize all the tokens.

        Parameters:
        - text (str): Text to tokenize.
        - language (str): set by default to French. It corresponds to the language of the text.

        Returns:
        - list of str: the lowerize tokens of 'text'.
        """
        return [token.lower() for token in word_tokenize(text,language=language)]

    
    def create_index_one_field(self, data, column_to_index, stem_index):
        """
        Helper function to create an index for a specific column (title or content for example).

        Parameters:
        - data (loaded json file): file containing the data about the crawled URLs.
        - column_to_index (str): the name of the column to use for the index (usually 'title' or 'content')
        - stem_index (bool): If set to True, in addition to an index using the tokens, an index using the stems is created.
        """
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

if __name__=="__main__":
    index= Index("crawled_urls.json", ['title', 'content', 'h1'])
    #index.create_metadata()
    index.create_index(False, False)