import camelot
import pandas as pd
import numpy as np
import os

def convert_to_float_or_blank(value):
    try:
        return float(value)
    except ValueError:
        return ''

filelist = os.listdir()
for item in filelist:
    if ".pdf" not in item:
        filelist.pop(filelist.index(item))
#filelist.pop(filelist.index("readAsda.py"))
filelist.pop(filelist.index("old"))
filelist.pop(filelist.index("output.xlsx"))
filelist.pop(filelist.index(".gitignore"))
#output with missing rows on last tables

#filelist = ["202304.pdf"]

df_raw = pd.DataFrame()
n=1
for file in filelist:
    tables = camelot.read_pdf(file,pages='1-end',flavor='stream',strip_text='£')
    for table in tables:
        df_raw = pd.concat([df_raw,table.df])


df_drop_rows=df_raw.copy()
#Drop rows that dont start with number
mask = df_drop_rows[0].str.match(r'^\d') # & df_drop_rows[0] =='28, PERCY STREET'
df_drop_rows=df_drop_rows[mask]
#Drop rows that are the address
mask = df_drop_rows[0] !='28, PERCY STREET'
df_drop_rows=df_drop_rows[mask]

df_merge_values = df_drop_rows.copy()
# fx data on numeric cols
df_merge_values[3] = pd.to_numeric(df_merge_values[3], errors='coerce')
df_merge_values[4] = pd.to_numeric(df_merge_values[4], errors='coerce')
df_merge_values[5] = pd.to_numeric(df_merge_values[5], errors='coerce')
df_merge_values[3].fillna(0, inplace=True)
df_merge_values[4].fillna(0, inplace=True)
df_merge_values[5].fillna(0, inplace=True)

#print(df_merge_values)

#df_merge_values['Values'] = df_merge_values[3].fillna(df_merge_values[4])
df_merge_values['Values'] = df_merge_values[3] + df_merge_values[4] +df_merge_values[5]

df_fix_dates = df_merge_values.copy()
#df_fix_dates['Date'] = df_fix_dates[0] + ' 23'
df_fix_dates['Date'] = pd.to_datetime(df_fix_dates[0] +' 23', format='%d %b %y').dt.date


df_final=df_fix_dates.copy()
df_final = df_final.rename(columns={2: 'Description'})
df_final['Account'] = "Asda CC"
df_final['Category'] =""
df_final['Category Group']=""

df_final=df_final[['Date','Values','Description','Category','Category Group','Account']]

with pd.ExcelWriter('output.xlsx') as writer:  
    df_raw.to_excel(writer, sheet_name='df_raw',index=False)
    df_drop_rows.to_excel(writer, sheet_name='df_drop_rows',index=False)
    df_merge_values.to_excel(writer, sheet_name='df_mergevalues',index=False)
    df_final.to_excel(writer, sheet_name='df_final',index=False)