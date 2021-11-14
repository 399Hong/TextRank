# Text Summariser

Text Summariser is a command line tool that takes in a long piece of text as input, and extracts the most relevant and important idea from the input, and generates a summary for the given text. 

The project was written purely in Python3, and all libraries used can be found in the `requirements.txt` file.


**6523 matches returned from 2225 articles** 

## Setup

To clone and run this program, you need Python 3.6 or above installed on your machine.

From your command line, do the following 

```shell
# First, clone this repository
$ git clone https://github.com/uoa-compsci399-s2-2021/sherlock.git

# Install all required dependencies
$ pip install -r requirements.txt
```

####  Download GloVe
Please download **glove.6B.200d.txt** from <a href ="https://nlp.stanford.edu/data/glove.6B.zip" > https://nlp.stanford.edu/data/glove.6B.zip</a>, and put it into the `sherlock` directory.

You may also try to use other glove word embeddings file to gain better performance. Use the glove(filename) method from the textRank class to input different glove embedding. 

Replace
```python
  tr.lazysetup()
```
With

```python
  fileName = ""
  tr.installStopWords()
  tr.glove(fileName)
```

> Not all glove file has been tested, current code is **guaranteed to work on the 200d file**.

> The testing function works on MacOS and Windows, It may or may not work on other OS. This is not a required feature of the client.

##  Usage

From your command line, 

```shell 
$ python3 main.py
```
and then follow the instructions on the Command Line Interface 

Note: 
If you receive an error stating stopwords not found when import nltk library, run:

```shell
$ python -m nltk.downloader stopwords
```
