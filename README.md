# Asda
Code to read Asda Pdf statements and pull the tables into a dataframe.

Requirements
Filelist needs to just collect the pdfs,  make sure anything else is removed.
Statements from 2023 only tested.  I think the older ones are differnt although I haven't tested

uses camelot-py
requires ghostscript to run

Outputs
Creates an Excel Output.xlsx file sheet-df_final,  I have set the format to mirror MoneyHub download format.  Moneyhub does not connect to Asda CC to get transaction data.  
This file is added manually to that download.  Categories are manually set
