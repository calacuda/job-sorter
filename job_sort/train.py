import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
from os import getcwd
from os.path import join


def entry_point(args):
    # TODO: get csv_fname from terminal args
    # csv_fname = args.csv
    csv_fname = join(getcwd(), args.csv) if args.csv[0] not in ["/", "~"] else args.csv

    df = pd.read_csv(csv_fname)
    x_train, x_test, y_train, y_test = train_test_split(df.text, df.alert, test_size=0.25)
    v = CountVectorizer()
    x_train_count = v.fit_transform(x_train.values)
    model = MultinomialNB()
    model.fit(x_train_count, y_train)

    # TODO: get model_name from terminal args
    model_name = args.model if args.model.endswith(".pkl") else args.model + ".pkl"
    pickle.dump((model, v), open(model_name, 'wb'))
