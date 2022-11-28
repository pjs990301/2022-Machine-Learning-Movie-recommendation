# <==== Importing Dependencies ====>

import pickle

import streamlit as st
import pandas as pd
import requests
import warnings
import time

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# <==== Code starts here ====>
smd1 = pickle.load(open('./pkl/smd1.pkl', 'rb'))
simple1 = pickle.load(open('./pkl/simple1.pkl', 'rb'))
similarity1 = pickle.load(open('./pkl/similarity1.pkl', 'rb'))

smd2 = pickle.load(open('./pkl/smd2.pkl', 'rb'))
simple2 = pickle.load(open('./pkl/simple2.pkl', 'rb'))
similarity2 = pickle.load(open('./pkl/similarity2.pkl', 'rb'))

smd3 = pickle.load(open('./pkl/recommendData.pkl', 'rb'))
collaboModel = pickle.load(open('./pkl/recommendModel.pkl', 'rb'))

gb = pickle.load(open('./pkl/clf1127_2.pkl', 'rb'))
multilabel = pickle.load(open('./pkl/MultiLabel.pkl', 'rb'))
vector = pickle.load(open('./pkl/vector.pkl', 'rb'))


def get_recommendations1(smd1, title):
    smd1 = smd1.reset_index()
    titles1 = smd1['title']
    indices1 = pd.Series(smd1.index, index=smd1['title'])
    idx = indices1[title]
    sim_scores = list(enumerate(similarity1[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles1.iloc[movie_indices]


def get_recommendations2(smd2, title):
    smd2 = smd2.reset_index()
    titles2 = smd2['title']
    indices2 = pd.Series(smd2.index, index=smd2['title'])

    idx = indices2[title]
    sim_scores = list(enumerate(similarity2[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles2.iloc[movie_indices]


def collabo(number):
    rank = []
    for columns, items in smd3.iterrows():
        test = []
        test.append(items[6])
        test.append(collaboModel.predict(number4, items[0])[3])
        rank.append(test)
    return rank


st.markdown("<h2 style='text-align: center; color: black;'>🎥 Movie Recommendation System 🎥</h2>",
            unsafe_allow_html=True)
st.markdown(
    "<h5 style='text-align: center; color: black;'>Recommend Movies using dataset consists of 45,000 movies by 270,000 users</h5>",
    unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Simple Recommender", "Content Based Filtering", "Collaborative Based Filtering", "Predict Genre"])

with tab1:
    number1 = st.number_input("Insert a number", min_value=1, max_value=250, step=1, format="%d", key=0)
    tab1_poster = simple1[["title", "year", "vote_count", "vote_average", "popularity"]].head(number1).reset_index(
        drop=False)
    simple = simple1[["title", "year", "vote_count", "vote_average", "popularity"]].head(number1).reset_index(drop=True)
    st.table(simple)

with tab2:
    sub_option1 = st.selectbox('Please select Sub Recommender!', ('Movie Description Based Recommender',
                                                                  'Metadata Based Recommender'))
    if sub_option1 == 'Movie Description Based Recommender':
        input = st.text_input("movie name")
        number2 = st.number_input("Insert a number", min_value=1, max_value=30, step=1, format="%d", key=1)
        if st.button('Show Recommended Movies'):
            if len(smd2[smd2['title'] == input]) == 0:
                st.error('Please re-enter the name of the movie', icon="🚨")
                with st.expander("See Movie list"):
                    temp2 = smd2[['title', 'overview']].reset_index(drop=True)
                    st.table(temp2[(temp2['title'].str.contains(input, na=False, case=False))])
                    st.write("\n")
            else:
                recommend = get_recommendations1(smd1, input)
                st.table(recommend[0:number2].reset_index(drop=True))

    elif sub_option1 == 'Metadata Based Recommender':
        input = st.text_input("keyword")
        if input:
            tab2_sub1 = smd2[smd2['title'].str.contains(input, na=False, case=False)]
            with st.expander("See Movie list"):
                st.table(tab2_sub1[['title', 'genres']].reset_index(drop=True))
                st.write("\n")
            movie = st.text_input("Movie Name", key=11)
            number3 = st.number_input("Insert a number", min_value=1, max_value=30, step=1, format="%d", key=2)

            if st.button('Show Recommended Movies', key=10):
                if len(smd2[smd2['title'] == movie]) == 0:
                    st.error('Please re-enter the name of the movie', icon="🚨")
                else:
                    recommend = get_recommendations2(smd2, movie)
                    st.table(recommend.iloc[0:number3].reset_index(drop=True))

with tab3:
    number4 = st.number_input("Insert a user id", min_value=1, max_value=671, step=1, format="%d", key=3)
    if st.button('Show Recommended Movies', key=31):
        col1, col2 = st.columns(2)
        with col1:
            st.write('User rating')
            temp = smd3[smd3['userId'] == number4]
            st.table(temp[['title', 'rating']].reset_index(drop=True))
        with col2:
            with st.spinner('Wait for it...'):
                df = pd.DataFrame(data=collabo(number4), columns=['title', 'score'])
                df.sort_values(ascending=False, by='score', inplace=True)
                df.drop_duplicates(subset=None, keep='first', inplace=True, ignore_index=False)
                time.sleep(7)
            st.write('Recommended Movie')
            st.table(df[0:20].reset_index(drop=True))

with tab4:
    radio = st.radio(
        "Filter",
        ('and', 'or'), horizontal=True)

    text1 = st.text_input("Enter Text 1")
    text2 = st.text_input("Enter Text 2")
    text3 = st.text_input("Enter Text 3")
    if text1:
        if text2:
            if text3:
                if radio == 'and':
                    tab4_sub1 = smd1[(smd1['description'].str.contains(text1, na=False, case=False)) & (
                        smd1['description'].str.contains(text2, na=False, case=False)) & (
                                         smd1['description'].str.contains(text3, na=False, case=False))]
                else:
                    target = [text1, text2, text3]
                    tab4_sub1 = smd1[smd1['description'].str.contains('|'.join(target), na=False, case=False)]
                st.success("Finding " + str(len(tab4_sub1)) + " Movies", icon='✅')
                with st.expander("See Movie list"):
                    st.table(tab4_sub1[['title', 'description']].reset_index(drop=True))
                    st.write("\n")
                movie = st.text_input("Movie Name", key=41)
                if st.button('Show Recommended Movies', key=40):
                    if len(smd1[smd1['title'] == movie]) == 0:
                        st.error('Please re-enter the name of the movie', icon="🚨")
                    else:
                        tab4_sub2 = smd1[smd1['title'] == movie]
                        tfidf_matrix = vector.transform(tab4_sub2['description'])
                        pred = gb.predict(tfidf_matrix)
                        inverse = multilabel.inverse_transform(pred)
                        st.write("The results of genre prediction through movie explanation : " + ' '.join(
                            map(str, inverse)))

                        # <==== Code ends here ====>
