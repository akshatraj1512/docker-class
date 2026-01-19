#!/usr/bin/env python
#test pipeline

import sys
import pandas as pd

print("arguments", sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({"day": [1, 2, 3], "passengers": [23, 14, 19]})
df['month'] = month
print(df.head())

df.to_parquet(f'output_{month}.parquet')
    
print(f"pipeline check, month = {month}")