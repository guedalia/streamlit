import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import plotly.graph_objects as go
from collections import Counter

@st.cache  # 👈 This function will be cached
def gen_data():
    filename= "https://github.com/guedalia/binder/raw/master/talmud_topics_clean.csv"
    return pd.read_csv(filename)

topics = gen_data()

def split_book_to_chunks(book_daf_min, book_daf_max, step, my_topics, num_most_common): 
    l=[]

    for x in range(book_daf_min, book_daf_max, step):
        slugs = my_topics[(my_topics["daf_int"] >= x)&(my_topics["daf_int"] < x+step)]["Topic He"]
        counted_slugs = Counter(slugs)
        if x+step > book_daf_max:
            new_step =  book_daf_max
        else:
            new_step =  x + step

        for top_slug in counted_slugs.most_common(num_most_common):
            d={
                'chunk': (x, new_step),
                'topic': top_slug[0],
                'count': top_slug[1]
            }
            l.append(d)
            
    return(l)

def topic_by_daf(chosen_book= "Sukkah", step = 10, num_most_common = 1):
    my_topics = topics[topics["book"]==chosen_book]

    book_daf_min = min(my_topics["daf_int"])
    book_daf_max = max(my_topics["daf_int"])

    l = split_book_to_chunks(book_daf_min, book_daf_max, step, my_topics, num_most_common)

    source = []
    target = []
    count = []

    for x in l:
        source.append(x['chunk'])
        target.append(x['topic'])
        count.append(x['count'])

    color_lookup = {}
    for i,x in enumerate(set(target)):
        color_lookup[x] = i

    color_list = []
    for x in target:
        color_list.append(color_lookup[x])


    fig = go.Figure(
        go.Parcats(
            dimensions=[
                {'label': 'Dapim',
                'values': source},
                {'label': 'Topics',
                'values': target},
            ],
            counts=count,
            line={'color': color_list}
        )
    )
    fig.update_layout(
        title = chosen_book
    )
    st.plotly_chart(fig)

# @interact(chosen_book = set(topics["book"]),  step = (1, 200, 1), num_most_common=(1,10,1))

chosen_book = st.sidebar.selectbox(
    "Masechet",
    list(set(topics["book"])),
)
step = st.sidebar.slider(
    'Step',
    1, 200, 
    10
)
num_most_common = st.sidebar.slider(
    'num_most_common',
    1, 10,
    1
)

topic_by_daf(chosen_book, step, num_most_common)
