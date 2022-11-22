import pandas as pd
import os


if __name__ == "__main__":
    folder = "wikiData"
    # get all .json files in the folder
    files = [file for file in os.listdir(folder) if file.endswith("-cleaned.pkl")]
    df = pd.read_pickle(os.path.join(folder, files[0]))
    print(df.head(10))
