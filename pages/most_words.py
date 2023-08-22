import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

import plotly.express as px

st.set_page_config(page_title="每篇文章字詞頻率",page_icon="")
st.title("字詞頻率統計")
@st.cache_data
def getData(name):
    df = pd.read_csv(name)
    return df
st.sidebar.title('參數')


word_count = getData("word_count_pages.csv")
top_k = st.sidebar.slider('Top K:', 1,20,5)

tab_list = []
fig_list = []
for i,l in enumerate(word_count.links.unique()):
    
    tab_list.append(":clipboard:  page"+str(i+1))
    sub = word_count[word_count.links == l].sort_values('counts',ascending=False).reset_index(drop=True)[0:top_k]
    fig = px.bar(sub,y='counts',x='words',)
    fig_list.append(fig)

print(word_count)
tab_list_ = st.tabs(tab_list)
for l,fig in enumerate(fig_list):
    
    with tab_list_[l]:
        link = word_count.links.unique()[l]
        st.markdown(f"##### {link}")
        st.plotly_chart(fig, theme=None, use_container_width=True)


