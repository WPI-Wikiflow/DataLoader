import pickle
import pandas as pd

if __name__ == "__main__":
    # unpickle the df.pkl dataframe
    df = pickle.load(open("df.pkl", "rb"))
    # print the columns
    print(df.columns)
    print(df.head())

    # Load the needDtoVFinal.csv file
    df2 = pd.read_csv("needDtoVFinal.csv")
    # print the columns
    print(df2.columns)
    print(df2.head())

    # Replace the summaries in df2 with the summaries from df
    df2['summary'] = df['summary']

    
    # print(df2.head())

    # Save the dataframe to a tsv file
    df2.to_csv("needDtoVFinal.tsv", sep="\t", index=False)