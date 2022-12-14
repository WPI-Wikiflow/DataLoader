import gensim
import decimal
import numpy as np
# import cosine similarity function
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


# create a new context for this task
ctx = decimal.Context()

# 20 digits should be enough for everyone :D
ctx.prec = 20

def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')

# Load the doc2vec model
model = gensim.models.doc2vec.Doc2Vec.load("doc2vec.model")

# Load the csv file
import pandas as pd
df = pd.read_csv("needDtoVFinalWithVectors.csv")
# Print the columns
print(df.columns)


vectors = []
for text in df['text']:
    vector = model.infer_vector(text.split(" "))
    vectors.append(vector)

titles = df['title']

# Find the best match for each of the first 10 vectors
for i in range(10): 
    # Find the best match for the ith vector
    bestMatch = 0
    bestMatchIndex = 0
    for j in range(len(vectors)):
        if i != j:
            sim = cosine_similarity(vectors[i].reshape(1,-1), vectors[j].reshape(1,-1))
            if sim > bestMatch:
                bestMatch = sim
                bestMatchIndex = j
    print("Best match for article " + titles[i] + " is " + titles[bestMatchIndex] + " with a similarity of " + str(bestMatch))



