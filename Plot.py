import streamlit as st
import pandas as pd
import numpy as np
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamyearbyyearstats

def plotData(df,stat_input,format,x_axis):
    if format == "Line Graph":
        st.line_chart(df, x=x_axis, y=stat_input)
    elif format == "Bar Graph":
        st.bar_chart(df, x=x_axis, y=stat_input)
    else:
        new_df = df[[x_axis,stat_input]]
        st.write(new_df)

def compareData():
    player_input_list = player_input.split(",")
    if option1 == 'Player':
        player_dict = players.get_players()
        

def getData():
    
    if comparing:
        return compareData()

    if option1 == 'Player':
        
        # LOAD ALL PLAYERS INTO DICT
        player_dict = players.get_players()

        # FIND PLAYERS THAT MATCH INPUT
        player_list = [player for player in player_dict if player['full_name'].lower() == player_input.lower()]

        # CHECK IF PLAYER FOUND
        if not player_list:
            # NO PLAYER FOUND IN LIST
            st.error('No Player Found', icon="🚨")
            return
            
        # GET PLAYER AND PLAYER_ID
        player = player_list[0]
        player_id = player['id'] 

        # API CALL GETTING PLAYER STATS FROM PLAYER_ID
        data = playercareerstats.PlayerCareerStats(player_id, per_mode36='PerGame')

        if option2 == 'Regular Season': 

            # REGULAR SEASON DATA
            df = data.get_data_frames()[0]
            plotData(df,stat_input,format,x_axis="SEASON_ID")

        elif option2 == "Post Season":

            # POST SEASON DATA
            df = data.get_data_frames()[2]
            plotData(df,stat_input,format,x_axis="SEASON_ID")

    elif option1 == "Team":

        # LOAD ALL TEAMS INTO DICT
        team_dict = teams.get_teams()

        # FIND TEAMS THAT MATCH INPUT
        team_list = [team for team in team_dict if team['full_name'].lower() == player_input.lower()]

        # CHECK IF TEAM FOUND
        if not team_list:
            # NO TEAM FOUND IN LIST
            st.error('No Team Found', icon="🚨")
            return

        # GET TEAM AND TEAM_ID
        team = team_list[0]
        team_id = team['id']

        # API CALL GETTING TEAM STATS FROM TEAM_ID
        data = teamyearbyyearstats.TeamYearByYearStats(team_id, per_mode_simple='PerGame')

        if option2 == "Regular Season":

            # REGULAR SEASON DATA
            df = data.get_data_frames()[0]
            plotData(df,stat_input,format,x_axis="YEAR")
            
        elif option2 == "Post Season":
            pass


# FORUM / WEB PAGE

st.write(""" # NBA Stats""")

comparing = st.checkbox('Compare')

if comparing:
    st.info('Seperate Two Players or Teams with a Comma', icon="ℹ️")

option1 = st.selectbox('Label',('Player','Team'),label_visibility="collapsed")

option2 = st.selectbox('Label',('Regular Season','Post Season'),label_visibility="collapsed")

stat_input = st.selectbox('Label',('PTS', 'REB', 'AST', 'STL','BLK'),label_visibility="collapsed")

format = st.selectbox('Label',('Line Graph','Bar Graph','Table'),label_visibility="collapsed")

player_input = st.text_input('Label',label_visibility='collapsed')

button = st.button('Add',on_click=getData)
