import pandas as pd

data = pd.read_csv('funds/instruments.csv')

print(set(data['fund_type']))