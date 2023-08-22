import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import pyvis


st.set_page_config(page_title="第一頁的字詞相關",page_icon="")

@st.cache_data
def getData(name):
    df = pd.read_csv(name)
    return df

def plot_graph(df_sim,df_word_count,st,ed,count_st,count_ed):
    df_sim_ = df_sim[(df_sim['cosin']>st) & (df_sim['cosin']<ed)].sort_values('cosin',ascending=False)
    df_word_count_ = df_word_count[(df_word_count['count']>=count_st) & (df_word_count['count']<count_ed)]
    df_sim_ = df_sim_[(df_sim_.w1.isin(df_word_count_.word.tolist())) & (df_sim_.w2.isin(df_word_count_.word.tolist()))]
    
    net =  pyvis.network.Network(notebook=True,cdn_resources='in_line')
    nodes = list(set(df_sim_.w1.unique().tolist()+df_sim_.w2.unique().tolist()))
    net.add_nodes(nodes,color=['#FF2D2D']*len(nodes))
    
    for i in df_sim_[['w1','w2','cosin']].to_numpy():
        net.add_edge(i[0],i[1],width = i[2]*10,title = str(i[2]))
    net.repulsion()
    net.show('cos_sim_w2v.html')
    HtmlFile = open('cos_sim_w2v.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(),height=660, scrolling=True)

st.title("字詞相似程度")
st.sidebar.title('參數')

word_count = pd.read_csv("word_count.csv")
cos_sim = pd.read_csv("cos_sim.csv")

st_,ed_ = st.sidebar.slider('相似性:', 0., 1., (.3, 1.))
count_st,count_ed = st.sidebar.slider('字數頻率:', word_count['count'].min(), word_count['count'].max(), (70,300))

plot_graph(cos_sim,word_count,st_,ed_,count_st,count_ed)
