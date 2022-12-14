import gensim
import decimal

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
df = pd.read_csv("needDtoVFinal.tsv", sep="\t")
# Print the columns
print(df.columns)

# Get the vectors for each article
vectors = []
for thing, text in enumerate(df['text']):
    text = text.split()
    # Remove all commas from the text
    text = [word.replace(",", "") for word in text]
    # Remove all backets from the text
    text = [word.replace("[", "") for word in text]
    text = [word.replace("]", "") for word in text]
    # Remove all ' from the text
    text = [word.replace("'", "") for word in text]
    # Print the first 10 words of the text
    print(text[:10])
    out_string = ""
    vector = model.infer_vector(text)
    for i in range(len(vector)):
        if i == len(vector) - 1:
            out_string += float_to_str(vector[i])
        else:
            out_string += float_to_str(vector[i]) + " "
    vectors.append(out_string)


# Add the vectors to the dataframe
df['vector'] = vectors



# Convert the vectors to a string without the brackets and scientific notation



# Save the dataframe as a csv with the following columns:
# vector, title, id (in that order)
df.to_csv("needDtoVFinalWithVectors2.csv", columns=['vector', 'title', 'id', 'summary'], sep="\t")

