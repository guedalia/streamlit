import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter

@st.cache  
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

book_list=list(set(topics["book"]))
default_chosen_book='Bava Kamma'
default_step=10
default_num_most_common=1

st.sidebar.title('Options')
chosen_book = st.sidebar.selectbox(
    "Masechet",
    book_list,
    book_list.index(default_chosen_book)
)
step = st.sidebar.slider(
    'number of Dapim in each group',
    1, 200, 
    default_step
)
num_most_common = st.sidebar.slider(
    'number of most common topics shown per group',
    1, 10,
    default_num_most_common
)

expanded=False
if (
    (chosen_book == default_chosen_book) &
    (step == default_step) &
    (num_most_common == default_num_most_common)
):
    expanded=True

'''
# Visualizing Talmud Topics in a Masechet
'''
with st.beta_expander("Details", expanded=expanded):
    '''
    This tool can be used to see what are the top topics in each Masechet, what topics will appear in the next few Dapim of learning, or where else in the Masechet does the same topic appear.

    The default shows the top ten topics in 'Bava kamma'. Feel free to change the Masechet with the dropdown bar or change the different sliders to change the number of Dapim in each group - or the number of most common topics shown per group.

    Written by Hagai Guedalia
    '''

topic_by_daf(chosen_book, step, num_most_common)
