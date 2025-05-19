import os
import pandas as pd


def save_to_csv(data, fname):
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(fname, index=False, encoding='utf-8')
