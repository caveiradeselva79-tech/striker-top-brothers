import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")

def load_csv(name):
    file_path = DATA_PATH / name
    if not file_path.exists():
        df = pd.DataFrame()
        df.to_csv(file_path, index=False)
    return pd.read_csv(file_path)

def save_csv(df, name):
    file_path = DATA_PATH / name
    df.to_csv(file_path, index=False)
