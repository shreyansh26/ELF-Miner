# coding: utf-8

import pandas as pd
import numpy as np
import re

df = pd.read_csv("final.csv")

df.drop(['Name'], axis=1, inplace=True)
df['ELFVersion'] = df['ELFVersion'].apply(lambda x: x[2:])
df['Flags'] = df['Flags'].apply(lambda x: x[2:])

req_col = [a for a in df.columns if '_size' in a]
req_col.extend([a for a in df.columns if 'entsize' in a])

for i in req_col:
    df[i] = df[i].apply(lambda x: str(x).replace(".0", ''))
for i in req_col:
    df[i] = df[i].apply(lambda x: int(str(x), 16) if x != "nan" and "E" not in str(x).upper() else x)
    df[i] = df[i].apply(lambda x: np.NaN if x != "nan" and "E" in str(x).upper() else x)
    df[i] = df[i].apply(lambda x: np.NaN if x == "nan" else x)
    df[i] = pd.to_numeric(df[i])


df.to_csv("final_postprocessing.csv", index=False)





