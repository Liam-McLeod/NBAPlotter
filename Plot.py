import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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


def plotData(Data,stat_input,format,x_axis):

    # GRAPH
    if format == "Line Graph" or format == "Bar Graph":
        
        fig = plt.Figure(figsize = (5, 5), dpi = 100)
        ax = fig.add_subplot(111)

        for name, df in Data.items():
            if df[stat_input].isnull().all():
                # NO DATA FOR STAT INPUT (eg. Bill Russell BLK)
                st.error('No data found for Stat: '+ stat_input + ' For: ' + name, icon="🚨")
                return

            #1960-61 BECOMES 1961 --- 2004-05 BECOMES 2005
            df[x_axis] = df[x_axis].apply(lambda x: int(x[:4])+1)

        # LINE GRAPH
            if format == "Line Graph":
                # PLOT STAT FROM DATAFRAME AND LABEL EACH LINE WITH NAME
                df.plot(kind='line',x=x_axis,y=stat_input,label=name,ax=ax)

            # BAR GRAPH
            if format == "Bar Graph":
                # PLOT STAT FROM DATAFRAME AND LABEL EACH BAR GROUP WITH NAME
                ax.bar(df[x_axis],df[stat_input],label=name)
        ax.legend()
        # FINAL PLOT
        st.pyplot(fig)

    # TABLE
    elif format == "Table":
        counter = 1
        final_df = pd.DataFrame()
        for name,df in Data.items():
            # INSERT SEASON ID(s)
            final_df.insert(len(final_df.columns),"SEASON_ID"+str(counter),df[x_axis])
            # INSERT STAT INPUT
            final_df.insert(len(final_df.columns), name+" "+stat_input,df[stat_input])
            counter+=1
        # DISPLAY FINAL TABLE
        st.write(final_df)

def getData():
    input_list = user_input.split(",")

    # PLAYER OPTION
    if option1 == 'Player':

        # LOAD ALL PLAYERS INTO DICT
        player_dict = players.get_players()
        # GET PLAYER LIST FROM PLAYER DICT
        player_list = getList(player_dict,input_list)

        # CHECK IF PLAYERS FOUND
        if not player_list:
            st.error('No Player(s) Found', icon="🚨")
            return
            
        # CHECK NUMBER OF PLAYERS
        if len(player_list) > 4:
            st.error('Too Many Players to Compare', icon="🚨")
            return
        
        # GET DATAFRAMES FOR ALL PLAYERS AND ADD TO DICTIONARY WITH PLAYER NAME
        # player['fullname']:df --- (String):(Dataframe)
        playerData = {}
        for player in player_list:
            # PLAYER ID
            player_id = player['id']
            # API CALL GETTING PLAYER STATS FROM PLAYER ID
            data = playercareerstats.PlayerCareerStats(player_id, per_mode36='PerGame')
            if option2 == 'Regular Season':
                # REGULAR SEASON STATS
                df = data.get_data_frames()[0]
            elif option2 == 'Post Season':
                # POST SEASON STATS
                df = data.get_data_frames()[2]
            playerData.update({player['full_name']:df})

        # PLOT PLAYER DATA
        plotData(playerData,stat_input,format,x_axis="SEASON_ID")

    # TEAM OPTION
    elif option1 == "Team":
        # LOAD ALL TEAMS INTO DICT
        team_dict = teams.get_teams()
        # GET TEAM LIST
        team_list = getList(team_dict,input_list)

        # CHECK IF TEAMS FOUND
        if not team_list:
            st.error('No Team(s) Found', icon="🚨")
            return

        # CHECK NUMBER OF TEAMS
        if len(team_list) > 2:
            st.error('Too Many Teams to Compare', icon="🚨")
            return

        # GET DATAFRAMES FOR ALL TEAMS AND ADD TO DICTIONARY WITH TEAM NAME
        # team['fullname']:df --- (String):(Dataframe)
        teamData = {}
        for team in team_list:
            # TEAM ID
            team_id = team['id']
            # API CALL GETTING TEAM STATS FROM TEAM ID
            data = teamyearbyyearstats.TeamYearByYearStats(team_id, per_mode_simple='PerGame')
            if option2 == 'Regular Season':
                # REGULAR SEASON STATS
                df = data.get_data_frames()[0]
            elif option2 == 'Post Season':
                # POST SEASON STATS
                st.error('No Post Season stats for teams', icon="🚨")
                return
            teamData.update({team['full_name']:df})

        # PLOT TEAM DATA
        plotData(teamData,stat_input,format,x_axis="YEAR")

# FORUM / WEB PAGE

st.write(""" # NBA Stats """)

st.info('Seperate Up to four players, OR two teams with a comma', icon="ℹ️")

option1 = st.selectbox('Label',('Player','Team'),label_visibility="collapsed")

option2 = st.selectbox('Label',('Regular Season','Post Season'),label_visibility="collapsed")

stat_input = st.selectbox('Label',('PTS', 'REB', 'AST', 'STL','BLK'),label_visibility="collapsed")

format = st.selectbox('Label',('Line Graph','Bar Graph','Table'),label_visibility="collapsed")

user_input = st.text_input('Label',label_visibility='collapsed')

button = st.button('Add',on_click=getData)
