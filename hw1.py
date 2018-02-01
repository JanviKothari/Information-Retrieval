# homework 1
# goal: tokenize, index, boolean query
# exports: 
#   student - a populated and instantiated ir4320.Student object
#   Index - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents


# ########################################
# first, create a student object
# ########################################

import cs525
import PorterStemmer 
import re
import nltk
import pandas as pd
import glob

MY_NAME = "Janvi Kothari"
MY_ANUM  = 167999376 # put your WPI numerical ID here
MY_EMAIL = "jkkothari@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = [ 
    ('Claire Danaher', 'Helped me understand how to initiate "self" objects in Python'),  
    ('Kavin Chandrasekaran', 'Helped me understand how to call the stem method from PorterStemmer class & cross-verified number of unique terms throughout the corpus after stemming'),
    ]

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "I do not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs525.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# ########################################
# now, write some code
# ########################################

# our index class definition will hold all logic necessary to create and search
# an index created from a directory of text files 
class Index(object):
    def __init__(self):
        # _inverted_index contains terms as keys, with the values as a list of
        # document indexes containing that term
        self._inverted_index = {}
        # _documents contains file names of documents
        self._documents = []
        # example:
        #   given the following documents:
        #     doc1 = "the dog ran"
        #     doc2 = "the cat slept"
        #   _documents = ['doc1', 'doc2']
        #   _inverted_index = {
        #      'the': [0,1],
        #      'dog': [0],
        #      'ran': [0],
        #      'cat': [1],
        #      'slept': [1]
        #      }


    # index_dir( base_path )
    # purpose: crawl through a nested directory of text files and generate an
    #   inverted index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: glob.glob()
    # parameters:
    #   base_path - a string containing a relative or direct path to a
    #     directory of text files to be indexed
    def index_dir(self, base_path):
        # PUT YOUR CODE HERE
        num_files_indexed = 0
        stemmed=[]
        tokens=[]
        doc_id=0
        i=0
        df_doc_index=pd.DataFrame(columns=['term','index'])
        
        for filename in glob.glob(base_path+'*.txt',recursive=True):
            self._documents.append(str(filename))
            file=open(filename,'r',encoding="utf8")
            text = file.read()
            tokens=Index.tokenize(self,text)
            stemmed+=Index.stemming(self,tokens)
            num_files_indexed+=1
#  The use of method set is to get only unique values from a list
        stemmed_set=set(stemmed)
#   The use of method list is to convert given set into a list so as to store in dataframe ahead  
        stemmed=list(stemmed_set)
#        df=pd.DataFrame(data=stemmed)
#        print(df.shape)
        for filename in glob.glob(base_path+'*.txt',recursive=True):
            file=open(filename,'r',encoding="utf8")
            text = file.read()
            tokens=Index.tokenize(self,text)
            doc_wise_stemmed=Index.stemming(self,tokens)
            doc_wise_stemmed_set=set(doc_wise_stemmed)
            doc_wise_stemmed=list(doc_wise_stemmed_set)
        
            for term in stemmed:
                for word in doc_wise_stemmed:
                    if(term==word):
                        df_doc_index.loc[i]=[term,doc_id]
                    i+=1
            doc_id+=1
        
        self._inverted_index=df_doc_index.groupby(['term'])['index'].apply(list).to_dict()
#        print(len(self._inverted_index))
        return num_files_indexed
    

    # tokenize( text )
    # purpose: convert a string of terms into a list of tokens.        
    # convert the string of terms in text to lower case and replace each character in text, 
    # which is not an English alphabet (a-z) and a numerical digit (0-9), with whitespace.
    # preconditions: none
    # returns: list of tokens contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        tokens = []
        # PUT YOUR CODE HERE
        text=text.replace("_"," ")
        text=re.sub(r'[^\w]',' ',text).lower()
        tokens=nltk.word_tokenize(text)
        return tokens

    # purpose: convert a string of terms into a list of tokens.        
    # convert a list of tokens to a list of stemmed tokens,     
    # preconditions: tokenize a string of terms
    # returns: list of stemmed tokens
    # parameters:
    #   tokens - a list of tokens
    def stemming(self, tokens):
        stemmed_tokens = []
        # PUT YOUR CODE HERE
        for token in tokens:
            stemmed_tokens.append(PorterStemmer.PorterStemmer().stem(token,0,(len(token)-1)))
        return stemmed_tokens
    
    # boolean_search( text )
    # purpose: searches for the terms in "text" in our corpus using logical OR or logical AND. 
    # If "text" contains only single term, search it from the inverted index. If "text" contains three terms including "or" or "and", 
    # do OR or AND search depending on the second term ("or" or "and") in the "text".  
    # preconditions: _inverted_index and _documents have been populated from
    #   the corpus.
    # returns: list of document names containing relevant search results
    # parameters:
    #   text - a string of terms
    def boolean_search(self, text):
        results = []
        # PUT YOUR CODE HERE
        stemmed=[]
        tokens=[]
        tokens=Index.tokenize(self,text)
        stemmed=Index.stemming(self,tokens)
        
        if(len(stemmed)==1):
            ids = self._inverted_index[stemmed[0]]    
        elif(len(stemmed) == 3):
            if(stemmed[1] == 'or'):
                part1_ids = self._inverted_index[stemmed[0]]
                part2_ids = self._inverted_index[stemmed[2]]
                ids=list(set(part1_ids+part2_ids))
            elif (stemmed[1] == 'and'):
                part1_ids = set(self._inverted_index[stemmed[0]])
                part2_ids = set(self._inverted_index[stemmed[2]])
                ids = list(part1_ids.intersection(part2_ids))
        else:
            print("Indexer unable to handle query of this sort")
#        print(ids)

        for id in ids:
            results.append(self._documents[id])
        
        
        return results
    

# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = Index()
    print("starting indexer")
    num_files = index.index_dir('data/')
    print("indexed %d files" % num_files)
    for term in ('football', 'mike', 'sherman', 'mike OR sherman', 'mike AND sherman'):
        results = index.boolean_search(term)
        print("searching: %s -- results: %s" % (term, ", ".join(results)))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

