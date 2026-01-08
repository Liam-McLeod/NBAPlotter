from statistics import mode
import streamlit as st
import pandas as pd
import plotly.express as px
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

def getPlayerList(dict,input_list):
    list = []
    for input in input_list:
        # REMOVE WHITESPACE
        input = input.strip()
        for name in dict:
            if name['full_name'].lower() == input.lower():
                list.append(name)
    return list

def plotData(combined_df,stat_input,format,x_axis):

    if format == "Line Graph":
        fig = px.line(combined_df, x=x_axis, y=stat_input, color='player', markers=True)
    elif format == "Bar Graph":
        fig = px.bar(combined_df, x=x_axis, y=stat_input, color='player', barmode='group')

    st.plotly_chart(fig)

    # TODO TABLE FORMAT
    # elif format == "Table":
    #     st.write(combined_df[stat_input])

def getPlayerStats(player_list,season_type):
    combined = []
    x_axis = "SEASON_ID"
    for player in player_list:
        player_id = player['id']
        player_name = player['full_name']

        if stat_type == "Averages":
            playerData = playercareerstats.PlayerCareerStats(player_id, per_mode36='PerGame')
            stats_df = playerData.get_data_frames()[0] if season_type == 'Regular Season' else playerData.get_data_frames()[2]
        elif stat_type == "Totals":
            playerData = playercareerstats.PlayerCareerStats(player_id, per_mode36='Totals')
            stats_df = playerData.get_data_frames()[0] if season_type == 'Regular Season' else playerData.get_data_frames()[2]

        # TODO CUMULATIVE TOTALS
        # elif stat_type == "Totals (Cumulative)":

        stats_df = stats_df.copy()
        stats_df["player"] = player_name
        stats_df[x_axis] = stats_df[x_axis].apply(lambda x: int(x[:4]) + 1) # Convert '1996-97' to 1997

        combined.append(stats_df)
    combined_df = pd.concat(combined, ignore_index=True)

    return combined_df

def getData():
    player_input_list = user_input.split(",")
    MAX_INPUT = 4
    player_dict = players.get_players()
    player_list = getPlayerList(player_dict,player_input_list)

    # NO PLAYERS FOUND ERROR
    if not player_list:
        st.error('No Player(s) Found', icon="🚨")
        return
        
    # TOO MANY PLAYERS ERROR
    if len(player_list) > MAX_INPUT:
        st.error('Too Many Players to Compare', icon="🚨")
        return

    combined_df = getPlayerStats(player_list,season_type)

    # NO DATA FOUND ERROR (E.G. Bill Russell BLK)
    if combined_df[stat_input].isnull().all():
        st.error(f'No data Found for {stat_input}', icon="🚨")
        return

    plotData(combined_df,stat_input,format,"SEASON_ID")
    
# FORUM / WEB PAGE

st.write(""" # NBA Stat Plotter """)

st.info('Seperate up to 4 players with a comma', icon="ℹ️")

stat_type = st.selectbox('Label',('Averages','Totals','Totals (Cumulative)'), label_visibility="collapsed")

season_type = st.selectbox('Label',('Regular Season','Post Season'),label_visibility="collapsed")

stat_input = st.selectbox('Label',('PTS', 'REB', 'AST', 'STL','BLK'),label_visibility="collapsed")

format = st.selectbox('Label',('Line Graph','Bar Graph','Table'),label_visibility="collapsed")

user_input = st.text_input('Label',label_visibility='collapsed')

button = st.button('Compare',on_click=getData)
