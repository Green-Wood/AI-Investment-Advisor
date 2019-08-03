import pickle
import pathlib

MODEL_PATH = pathlib.Path(__file__).parent
f = open(MODEL_PATH.joinpath('optimizer'), 'rb')
optimizer = pickle.load(f)