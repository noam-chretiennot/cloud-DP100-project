# import libraries
import argparse
import pandas as pd
from pathlib import Path

def main(args):
    # read data
    df = get_data(args.input_data)

    cleaned_data = clean_data(df)

    output_df = cleaned_data.to_csv((Path(args.output_data) / "cleaned-breast-cancer.csv"), index = False)

# function that reads the data
def get_data(path):
    df = pd.read_csv(path)

    # Count the rows and print the result
    row_count = (len(df))
    print('Preparing {} rows of data'.format(row_count))
    
    return df

# function that removes missing values
def clean_data(df):
    df = df.dropna()
    df["age"] = df["age"].apply(lambda x: int(x[0]))
    df["menopause"] = df["menopause"].apply(lambda x: 1 if x == "lt40" else (2 if x == "ge40" else 3))
    df["tumor-size"] = df["tumor-size"].apply(lambda x: int(x[0]))
    df["inv-nodes"] = df["inv-nodes"].apply(lambda x: int(x[0]))
    df["node-caps"] = df["node-caps"].apply(lambda x: 1 if x == "yes" else 0)
    df["breast"] = df["breast"].apply(lambda x: 1 if x == "left" else 0)
    df = pd.get_dummies(df, columns=["breast-quad"])
    df["irradiat"] = df["irradiat"].apply(lambda x: 1 if x == "yes" else 0)
    df["recurence"] = df["recurence"].apply(lambda x: 1 if x == "recurrence-events" else 0)
    
    return df


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--input_data", dest='input_data',
                        type=str)
    parser.add_argument("--output_data", dest='output_data',
                        type=str)

    # parse args
    args = parser.parse_args()

    # return args
    return args

# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")