# <==== Importing Dependencies ====>

import pickle
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# <==== Code starts here ====>
smd1 = pickle.load(open('smd1.pkl', 'rb'))
simple1 = pickle.load(open('simple1.pkl', 'rb'))
similarity1 = pickle.load(open('similarity1.pkl', 'rb'))

smd1 = smd1.reset_index()
titles1 = smd1['title']
indices1 = pd.Series(smd1.index, index=smd1['title'])

smd2 = pickle.load(open('smd2.pkl', 'rb'))
simple2 = pickle.load(open('simple2.pkl', 'rb'))
similarity2 = pickle.load(open('similarity2.pkl', 'rb'))

smd2 = smd2.reset_index()
titles2 = smd2['title']
indices2 = pd.Series(smd2.index, index=smd2['title'])


def get_recommendations1(title):
    idx = indices1[title]
    sim_scores = list(enumerate(similarity1[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles1.iloc[movie_indices]


def get_recommendations2(title):
    idx = indices2[title]
    sim_scores = list(enumerate(similarity2[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles2.iloc[movie_indices]


st.markdown("<h2 style='text-align: center; color: blue;'>Coursera Course Recommendation System</h2>",
            unsafe_allow_html=True)
st.markdown(
    "<h4 style='text-align: center; color: black;'>Find similar courses from a dataset of over 3,000 courses from Coursera!</h4>",
    unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Web App created by Sagar Bapodara</h4>",
            unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Simple Recommender", "Content Based Recommender", "Collaborative Filtering"])

with tab1:
    number1 = st.number_input("Insert a number", min_value=1, max_value=250, step=1, format="%d", key=0)
    simple = simple1[["title", "year", "vote_count", "vote_average", "popularity"]].head(number1).reset_index(drop=True)
    st.table(simple)

with tab2:
    sub_option1 = st.selectbox('Please select Sub Recommender!', ('Movie Description Based Recommender',
                                                                  'Metadata Based Recommender'))
    if sub_option1 == 'Movie Description Based Recommender':
        input = st.text_input("moive name")
        number2 = st.number_input("Insert a number", min_value=1, max_value=30, step=1, format="%d", key=1)
        if st.button('Show Recommended Courses'):
            recommend = get_recommendations1(input)
            st.table(recommend[0:number2].reset_index(drop=True))
            st.text(" ")

    elif sub_option1 == 'Metadata Based Recommender':
        input = st.text_input("keyword")
        number3 = st.number_input("Insert a number", min_value=1, max_value=30, step=1, format="%d", key=2)
        if st.button('Show Recommended Courses'):
            recommend = get_recommendations2(input)
            st.table(recommend.iloc[0:number3].reset_index(drop=True))
            st.text(" ")

with tab3:
    st.write("Collaborative Filtering")

# <==== Code ends here ====>