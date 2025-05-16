import pandas as pd


def save_to_csv(data, fname):
    df = pd.DataFrame(data)
    df.to_csv(fname, index=False, encoding='utf-8')
