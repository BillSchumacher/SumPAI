import os
import pickle


def load_sum(path):
    if os.path.exists(path):
        with open(path, "rb") as input_file:
            return pickle.load(input_file)


def save_sum(path, sum):
    with open(path, "wb") as output_file:
        pickle.dump(sum, output_file)
