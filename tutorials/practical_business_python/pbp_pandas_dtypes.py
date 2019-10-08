# http://pbpython.com/pandas_dtypes.html
#%% import
import pandas as pd

#%%
df = pd.read_clipboard()

#%%
df.head()

print(df.info())
print(df.dtypes)

#%% custom conversion
def convert_currenct(val):
    new_val = val.replace(',', '').replace('$', '')
    return float(new_val)


df['2016'].apply(convert_currenct)
