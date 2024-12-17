import streamlit as st
import pandas as pd
import pickle
import nltk

nltk.download('punkt_tab')

songs=pd.read_csv('./Dataset/Bollywood-Songs-Dataset(2017-23).csv')
with open('./Pickle/similarity.pkl', 'rb') as file:
    similarity=pickle.load(file)

music_list=songs['music_name'].values
sorted(music_list)

st.header('Recommended Musics')

left_sidebar=st.sidebar

selected_music=left_sidebar.selectbox(label='Select Music', options=music_list, index=None)



if(selected_music==None):
    left_sidebar.write("No music is select")
else:
    music_index=songs[songs['music_name']==selected_music].index[0]
    left_sidebar.image(songs.iloc[music_index].thumbnail, width=320)
    left_sidebar.write(f'**Music Title:** <br> {songs.iloc[music_index].music_name}', unsafe_allow_html=True)
    left_sidebar.write(f'**Singer:** <br> {songs.iloc[music_index].singer}', unsafe_allow_html=True)
    left_sidebar.write(f'**Release:** <br> {songs.iloc[music_index].release}', unsafe_allow_html=True)


def recommend(song):
    song_index=songs[songs['music_name']==song].index[0]
    distances=similarity[song_index]
    song_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    song_details={
        'music_name':[],
        'release':[],
        'singer':[],
        'thumbnail':[]
    }
    c=0
    for i in song_list:
        if(i[1]>=0.5 and i[1]!=1 and c<5):
            c+=1
            song_details['music_name'].append(songs.iloc[i[0]].music_name)
            song_details['release'].append(songs.iloc[i[0]].release)
            song_details['singer'].append(songs.iloc[i[0]].singer)
            song_details['thumbnail'].append(songs.iloc[i[0]].thumbnail)
    return song_details
if selected_music!=None:
    song_details=recommend(selected_music)

if(selected_music!=None):
    title=song_details['music_name']
    release=song_details['release']
    singer=song_details['singer']
    url=song_details['thumbnail']
    l=len(title)
    for i in range(l):
        if(title[i]!=selected_music):
            left_col, right_col=st.columns(2)
            left_col.image(url[i], width=200)
            right_col.write(f'**Music Title:** {title[i]}', unsafe_allow_html=True)
            right_col.write(f'**Singer:** {singer[i]}', unsafe_allow_html=True)
            right_col.write(f'**Release:** {release[i]}', unsafe_allow_html=True)
