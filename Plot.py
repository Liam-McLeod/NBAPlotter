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

def getData():
    input_list = user_input.split(",")
    
    if option1 == 'Player':
        player_dict = players.get_players()

        player_list = []
        for p in input_list:
            for player in player_dict:
                if player['full_name'].lower() == p.lower():
                    player_list.append(player)

        # CHECK IF PLAYERS FOUND
        if not player_list:
            # NO PLAYER FOUND IN LIST
            st.error('No Player(s) Found', icon="🚨")
            return
        
        dataframes = []
        for p in player_list:
            # PLAYER ID
            player_id = p['id']
            # API CALL GETTING PLAYER STATS FROM PLAYER ID
            data = playercareerstats.PlayerCareerStats(player_id, per_mode36='PerGame')
            if option2 == 'Regular Season':
                # REGULAR SEASON STATS
                df = data.get_data_frames()[0]
            elif option2 == 'Post Season':
                # POST SEASON STATS
                df = data.get_data_frames()[2]
            dataframes.append(df)


        final_df = pd.DataFrame()
        for df in dataframes:
            #final_df.insert(0,df.iat[0,0],df[stat_input])
            plotData(df,stat_input,format,x_axis="SEASON_ID")
        #st.write(final_df)

    elif option1 == "Team":
        # LOAD ALL TEAMS INTO DICT
        team_dict = teams.get_teams()

        team_list = []
        for t in input_list:
            for team in team_dict:
                if team['full_name'].lower() == t.lower():
                    team_list.append(team)

        # CHECK IF TEAM FOUND
        if not team_list:
            # NO TEAM FOUND IN LIST
            st.error('No Team(s) Found', icon="🚨")
            return

        dataframes = []
        for t in team_list:
            # TEAM ID
            team_id = t['id']
            # API CALL GETTING TEAM STATS FROM TEAM ID
            data = teamyearbyyearstats.TeamYearByYearStats(team_id, per_mode_simple='PerGame')
            if option2 == 'Regular Season':
                # REGULAR SEASON STATS
                df = data.get_data_frames()[0]
            elif option2 == 'Post Season':
                # POST SEASON STATS
                st.error('No Post Season stats for teams', icon="🚨")
                return
            dataframes.append(df)

        final_df = pd.DataFrame()
        for df in dataframes:
            #final_df.insert(0,df.iat[0,0],df[stat_input])
            plotData(df,stat_input,format,x_axis="YEAR")
        #st.write(final_df)

# FORUM / WEB PAGE

st.write(""" # NBA Stats""")

st.info('Seperate Up to four players, OR two teams with a comma', icon="ℹ️")

option1 = st.selectbox('Label',('Player','Team'),label_visibility="collapsed")

option2 = st.selectbox('Label',('Regular Season','Post Season'),label_visibility="collapsed")

stat_input = st.selectbox('Label',('PTS', 'REB', 'AST', 'STL','BLK'),label_visibility="collapsed")

format = st.selectbox('Label',('Line Graph','Bar Graph','Table'),label_visibility="collapsed")

user_input = st.text_input('Label',label_visibility='collapsed')

button = st.button('Add',on_click=getData)
