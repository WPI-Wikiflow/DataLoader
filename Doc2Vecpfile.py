import gensim
import pandas as pd
import ast
def gensimToVec():
    print('hello')
    # Load pre-trained Word2Vec model.
    model = gensim.models.Doc2Vec.load("doc2vec.model")
    data = pd.read_csv('needDtoVFinal.csv')
    subset = data.sample(n=1000,random_state = 8)
    subset['vec'] = subset['text'].map(lambda x: model.infer_vector(ast.literal_eval(x)))
    return subset

if __name__ == "__main__":
    dataframe = gensimToVec()
    dataframe.to_csv('final.csv')