import streamlit as st
import pandas as pd
import plotly.express as px
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

def getPlayerList(player_lookup,player_input_list):
    results = []
    for raw_name in player_input_list:
        name = raw_name.strip().lower()
        if name in player_lookup:
            results.append(player_lookup[name])
    return results

def plotData(combined_df,stat_input,format,x_axis):
    if format == "Line Graph":
        fig = px.line(combined_df, x=x_axis, y=stat_input, color='player', markers=True)
        fig.update_layout(title=f"{stat_input} by Season",xaxis_title="Season",yaxis_title=stat_input,legend_title="Player",hovermode="x unified")
        st.plotly_chart(fig)
    elif format == "Bar Graph":
        fig = px.bar(combined_df, x=x_axis, y=stat_input, color='player', barmode='group')
        fig.update_layout(title=f"{stat_input} by Season",xaxis_title="Season",yaxis_title=stat_input,legend_title="Player",hovermode="x unified")
        st.plotly_chart(fig)
    elif format == "Table":
        table_df = combined_df.pivot_table(index=x_axis, columns='player', values=stat_input).reset_index()
        st.dataframe(table_df,width='stretch')

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

        elif stat_type == "Totals (Cumulative)":
            playerData = playercareerstats.PlayerCareerStats(player_id, per_mode36='Totals')
            stats_df = playerData.get_data_frames()[0] if season_type == 'Regular Season' else playerData.get_data_frames()[2]
            stats_df[stat_input] = stats_df[stat_input].cumsum()

        stats_df = stats_df.copy()
        
        # KEEP ONE ROW PER SEASON, USE TOT IF IT EXISTS. THIS HAPPENS WHEN A PLAYER PLAYS FOR MULTIPLE TEAMS IN A SEASON (i.E. TRADES)
        if "TEAM_ABBREVIATION" in stats_df.columns:
            stats_df = (stats_df.sort_values("TEAM_ABBREVIATION").drop_duplicates(subset=["SEASON_ID"], keep="last"))

        # ADD PLAYER NAME COLUMN FOR PLOTTING PURPOSES AND CONVERT SEASON_ID TO INT
        stats_df["player"] = player_name
        stats_df[x_axis] = stats_df[x_axis].apply(lambda x: int(x[:4]) + 1) # Convert '1996-97' to 1997

        combined.append(stats_df)

    # COMBINE ALL PLAYER DATAFRAMES  
    combined_df = pd.concat(combined, ignore_index=True)
    # SORT BY X AXIS
    combined_df = combined_df.sort_values(by=[x_axis])
    return combined_df

def getData():
    MAX_INPUT = 4
    # USER INPUT
    player_input_list = [x.strip() for x in user_input.split(",") if x.strip()]
    # LOAD ALL PLAYERS
    player_list = players.get_players()

    # CREATE PLAYER LOOKUP DICTIONARY FOR FASTER SEARCHING
    player_lookup = {p['full_name'].lower(): p for p in player_list} # {'lebron james': {player_data}, ...}
    selected_players = getPlayerList(player_lookup,player_input_list)

    # NO PLAYERS FOUND ERROR
    if not selected_players:
        st.warning('No matching players found. Check spelling and try again.', icon="🚨")
        return
        
    # TOO MANY PLAYERS ERROR
    if len(selected_players) > MAX_INPUT:
        st.warning('You can compare up to 4 players at once.', icon="🚨")
        return
        
    # GET PLAYER STATS
    combined_df = getPlayerStats(selected_players,season_type)

    # NO DATA FOUND ERROR (E.G. Bill Russell BLK)
    if combined_df[stat_input].isnull().all():
        st.warning(f'No data Found for {stat_input}', icon="🚨")
        return

    plotData(combined_df,stat_input,format,"SEASON_ID")
    
# FORUM / WEB PAGE

st.write(""" # NBA Stat Plotter """)

st.info('Seperate up to 4 players with a comma', icon="ℹ️")

stat_type = st.selectbox('Statisic Type',('Season Averages','Season Totals','Career Cumulative Totals'))

season_type = st.selectbox('Season Type',('Regular Season','Post Season'),)

stat_input = st.selectbox('Statistic',('PTS', 'REB', 'AST', 'STL','BLK','FGM','FTM'))

format = st.selectbox('Format',('Line Graph','Bar Graph','Table'))

user_input = st.text_input('Players',placeholder="Lebron James, Stephen Curry")

button = st.button('Compare',width='stretch',on_click=getData)
