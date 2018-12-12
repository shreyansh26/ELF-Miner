# coding: utf-8


import pandas as pd
import numpy as np

attr_list = []
with open('../feature_selection/weka_features_toremove.txt', 'r') as f:
    for l in f:
        attr_list.append(l[27:].strip())


df_train = pd.read_csv('./final_postprocessing.csv')


df_train.drop(attr_list, axis=1, inplace=True)
df_train['label'] = '?'

df_train.to_csv('final_feature_selection.csv', index=False)



