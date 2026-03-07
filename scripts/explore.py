import pandas as pd

df = pd.read_csv("data/raw/synthetic_dataset.csv")

print("SHAPE:", df.shape)
print("\nCOLUMNS:", df.columns.tolist())
print("\nDATA TYPES:\n", df.dtypes)
print("\nFIRST 10 ROWS:\n", df.head(10))
print("\nNULL COUNTS:\n", df.isnull().sum())
print("\nSTATS:\n", df.describe())