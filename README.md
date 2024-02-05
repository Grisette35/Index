# Index project README

## Introduction
This Python-based project provides a simple way to create indexes from information gathered in a JSON file by a web crawler.

## Projects components

### 1. Index(es) creation (`index.py`)

The `index.py`scrip defines the core functionality of the indexes creation. It utilizes the `nltk` library for tokenizing and stemming the information from the crawled URLs JSON file, `pandas` for the calculation of statitics and the `collections` library for the `defaultdict` type and the `Counter` for the metadata. 

The creation of the index follows these steps: tokeninzing the title, the content, the first subtitle (h1) in an Pandas Dataframe to calculate some statistics and create the metadatafile. Then, we can proceed to the actual creation of the indexes by tokenizing and stemming (if the option is selected) the title and the content (if the option is selected) and creating a dictionnary where the tokens (or stems) are the keys and the values are the list of document ID in which the token (or the stem is). This is the simplest index given by the algorithm. The algorithm also gives the positions and the number of times a token is in a document. All the indexes are given in JSON files.

### 2. Example usage (`main.py`)

The `main.py` script demonstrates an example of using the index creator using an arguments parsers to facilitate interactions with the user in the Terminal.

## Setup

1. **Dependecies:** Ensure that you have the necessary Python packages installed. You can install them using the following:

    ```bash
   pip install nltk pandas
   ```
2. **Run the Project:**

To run the index creator, you can use the following command format:

```bash
python main.py "crawled_urls.json" "['title', 'content', 'h1']" --index_for_content False --stem_index False
```

Replace "crawled_urls.json" with your json file containing the information from the crawled URLS and adjust the other parameters accordingly. Note that it takes longer for the algorithm to finish when the paramaters --index_for_content and --stem_index are set to True.
You might need to change the `python` command by `python3`.

For more information on the parameters, you can use the following command:

```bash
python main.py --help
```

## Contributor

- Julia Toukal
