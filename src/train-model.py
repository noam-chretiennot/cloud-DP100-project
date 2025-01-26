# import libraries
import mlflow
import glob
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
from pathlib import Path
import os

def main(args):
    # enable autologging
    mlflow.autolog()

    # read data
    df = get_data(args.training_data)

    # split data
    X_train, X_test, y_train, y_test = split_data(df)

    # train model
    model = train_model(X_train, y_train, args.c, args.gamma, args.recurrence_weight)

    eval_model(model, X_test, y_test)
    
    if not os.path.isdir(args.model):
        os.makedirs(args.model)
    mlflow.sklearn.save_model(model, args.model)


# function that reads the data
def get_data(data_path):

    all_files = glob.glob(data_path + "/*.csv")
    df = pd.concat((pd.read_csv(f) for f in all_files), sort=False)
    
    return df

# function that splits the data
def split_data(df):
    print("Splitting data...")
    X, y = df[['age','menopause','tumor-size','inv-nodes',
    'node-caps', 'deg-malig','breast','irradiat', 
    'breast-quad_central', 'breast-quad_left_low',
    'breast-quad_left_up', 'breast-quad_right_low',
    'breast-quad_right_up']], df['recurence']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

    return X_train, X_test, y_train, y_test

# function that trains the model
def train_model(X_train, y_train, c, gamma, weight):
    mlflow.log_param("C", c)
    mlflow.log_param("gamma", gamma)
    print("Training model...")
    model = SVC(class_weight={0:1, 1:weight}, C=c, gamma=gamma).fit(X_train, y_train)

    return model

# function that evaluates the model
def eval_model(model, X_test, y_test):
    # calculate accuracy
    y_hat = model.predict(X_test)
    acc = np.average(y_hat == y_test)
    print('Accuracy:', acc)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    parser.add_argument("--c", dest='c',
                        type=float)
    parser.add_argument("--gamma", dest='gamma',
                        type=float)
    parser.add_argument("--recurrence_weight", dest='recurrence_weight',
                        type=float)
    parser.add_argument("--model", dest='model',
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
