import streamlit as st
import pandas as pd
import plotly.express as px
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamyearbyyearstats

def getList(dict,input_list):
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
        fig = px.line(combined_df, x=x_axis, y=stat_input, color='entity', markers=True)
    elif format == "Bar Graph":
        fig = px.bar(combined_df, x=x_axis, y=stat_input, color='entity', barmode='group')

    st.plotly_chart(fig)

    # elif format == "Table":
    #     st.write(combined_df[stat_input])

    

def getEntityStats(entity_list,mode,season_type):
    combined = []
    for entity in entity_list:
        entity_id = entity['id']
        entity_name = entity['full_name']

        if mode == 'Player':
            x_axis = "SEASON_ID"
            data = playercareerstats.PlayerCareerStats(entity_id, per_mode36='PerGame')
            stats_df = data.get_data_frames()[0] if season_type == 'Regular Season' else data.get_data_frames()[2]

        elif mode == 'Team':
            if season_type == 'Regular Season':
                x_axis = "YEAR"
                data = teamyearbyyearstats.TeamYearByYearStats(entity_id, per_mode_simple='PerGame')
                stats_df = data.get_data_frames()[0]
            else: 
                st.error('No Post Season stats for teams', icon="🚨")
                return
    
        stats_df = stats_df.copy()
        stats_df["entity"] = entity_name
        stats_df[x_axis] = stats_df[x_axis].apply(lambda x: int(x[:4]) + 1) # Convert '1996-97' to 1997
        combined.append(stats_df)
    combined_df = pd.concat(combined, ignore_index=True)

    return combined_df

def getData():
    input_list = user_input.split(",")
    MAX_INPUT = 2
    player_dict = players.get_players()
    team_dict = teams.get_teams()
    player_list = getList(player_dict,input_list)
    team_list = getList(team_dict,input_list)
    
    # PLAYER OPTION
    if mode == 'Player':

        # CHECK IF PLAYERS FOUND
        if not player_list:
            st.error('No Player(s) Found', icon="🚨")
            return
            
        # CHECK NUMBER OF PLAYERS
        if len(player_list) > MAX_INPUT:
            st.error('Too Many Players to Compare', icon="🚨")
            return
        
        combined_df = getEntityStats(player_list,mode,season_type)
        plotData(combined_df,stat_input,format,"SEASON_ID")
    # TEAM OPTION
    elif mode == "Team":

        # CHECK IF TEAMS FOUND
        if not team_list:
            st.error('No Team(s) Found', icon="🚨")
            return

        # CHECK NUMBER OF TEAMS
        if len(team_list) > MAX_INPUT:
            st.error('Too Many Teams to Compare', icon="🚨")
            return

        combined_df = getEntityStats(team_list,mode,season_type)
        plotData(combined_df,stat_input,format,"YEAR")
        

# FORUM / WEB PAGE

st.write(""" # NBA Stats """)

st.info('Seperate up to two players, OR two teams with a comma', icon="ℹ️")

mode = st.selectbox('Label',('Player','Team'),label_visibility="collapsed")

season_type = st.selectbox('Label',('Regular Season','Post Season'),label_visibility="collapsed")

stat_input = st.selectbox('Label',('PTS', 'REB', 'AST', 'STL','BLK'),label_visibility="collapsed")

format = st.selectbox('Label',('Line Graph','Bar Graph','Table'),label_visibility="collapsed")

user_input = st.text_input('Label',label_visibility='collapsed')

button = st.button('Add',on_click=getData)
