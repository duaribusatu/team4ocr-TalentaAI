import streamlit as st 
import os
import re
import pandas as pd
import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from scripts.auth import azure_ad_auth

st.title("Analyze ur Recipe")

# Auth
email, username, full_name, uid = azure_ad_auth('home', True)
st.text(f'email, username, full_name, uid: {(email, username, full_name, uid)}')

# Search Engine
service_endpoint = 'https://team4search.search.windows.net'
index_name = 'team4-index'
key = 'FyD93VZXnZzCYmSmniUE4aAkzOADP1C27HYq2363ptAzSeAZBgNd'

search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

def search_pangan_by_name(nama_pangan, gram):
    if nama_pangan is not None:
        results = search_client.search(search_text=nama_pangan)
        data = [result for result in results]
        if len(data) > 0:
            df_res = pd.DataFrame(data)[['@search.score', 'Lemak', 'VitaminB1', 'VitaminB2', 'VitaminA', 'Besi', 'Karbohidrat', 'Serat', 'VitaminB3', 'id', 'NamaPangan', 'Energi', 'NamaPangan_Emb', 'VitaminC', 'Garam', 'Protein']]
            for col in ['Lemak', 'VitaminB1', 'VitaminB2', 'VitaminA', 'Besi', 'Karbohidrat', 'Serat', 'VitaminB3', 'Energi', 'VitaminC', 'Garam', 'Protein']:
                df_res[col] = df_res[col] * (gram / 100)
            return df_res.iloc[0]

    return pd.Series(index=['@search.score', 'Lemak', 'VitaminB1', 'VitaminB2', 'VitaminA', 'Besi', 'Karbohidrat', 'Serat', 'VitaminB3', 'id', 'NamaPangan', 'Energi', 'NamaPangan_Emb', 'VitaminC', 'Garam', 'Protein'])

def convert_to_grams(text):
    conversions = {
        "sdm": 12,
        "sdt": 4,
        "ml": 1,
        "suing": 5,
        "siung": 5,
        "butir": 50,
        "buah": 150,
        "daun": 1,
        "potong": 100,
        "bh": 50,
        "bt": 50,
        "biji": 50,
        "bj": 50,
        "sendok makan": 12,
        "sendok teh": 4,
        "btr": 50,
        "ptng": 100,
        "btg": 100,
        "lmbr": 5,
        "cup": 230,
        "gelas": 250,
        "gls": 250,
        "mangkok": 300,
        "secukupnya": 5,
        "gr": 1,
        "gram": 1,
    }

    result = []
    pattern = r'(\d+\s*(?:\d+/\d+)?)(?:\s*(\S+))?\s*\[?(\S*)\]?\s*'
    for line in text.split('\n'):
        for match in re.finditer(pattern, line):
            amount, unit, ingredient = match.groups()
            amount = amount.replace(' ', '')
            amount = eval(amount) if '/' in amount else float(amount)

            if unit in conversions:
                grams = amount * conversions[unit]
                result.append((line, amount, unit, grams, ingredient))
            else:
                result.append((line, None, None, None, None))

    return result

resep = st.text_area('Resep manakan')
extract = st.button('Extract')
if extract:
    print(resep)

    conversions = convert_to_grams(resep.strip())
    df = pd.DataFrame(conversions, columns=['original', 'qyt_old', 'satuan', 'gram', 'bahan'])
    df[['@search.score', 'Lemak', 'VitaminB1', 'VitaminB2', 'VitaminA', 'Besi',
       'Karbohidrat', 'Serat', 'VitaminB3', 'id', 'NamaPangan', 'Energi',
       'NamaPangan_Emb', 'VitaminC', 'Garam', 'Protein']] = df.apply(lambda row: search_pangan_by_name(row['bahan'], row['gram']), axis=1)
    st.session_state['ingredients_result'] = df
    
df = st.session_state.get('ingredients_result', None)
if df is not None:
    st.dataframe(df)
    df_sum = df.select_dtypes(float).sum().to_frame().transpose()
    st.dataframe(df_sum)

submit = st.button('Submit to SQL')
if submit:
    pass
    # TODO: insert to SQL database 
    # https://learn.microsoft.com/en-us/sql/machine-learning/data-exploration/python-dataframe-sql-server?view=sql-server-ver16
