import pandas as pd
import plotly.express as px
from src.preprocess import df, team_city
import streamlit as st


def plot(fig):
    st.plotly_chart(fig, use_container_width=True)

def most_home_wins(df, year: int):
    df4all = df[["id", "season", "city", "winner"]]
    df4all["TF"] = 0
    for index, row in df4all.iterrows():
        for team in team_city:
            if (row.winner == team) and (str(row.city) in team_city[team]):
                df4all.at[index, "TF"] = 1
    df_final = df4all[df4all["TF"]==1]
    if year!=0 and year!=2009:
        df_plot2 = df_final.groupby(["season", "winner"])["TF"].count().reset_index().sort_values(by=["TF"], ascending=False)
        df_plot3 = df_plot2.loc[df_plot2["season"]==year]
        fig = px.bar(df_plot3, x="winner", y="TF", hover_data=["TF"], labels={"winner": "Team", "TF":f"Number of wins at homeground in {year}"}) 
        plot(fig) 
    elif year==2009:
        st.write("No homeground matches since games weren't held in India")              
    else:
        df_plot = df_final.groupby(["winner"])["TF"].count().reset_index().sort_values(by=["TF"], ascending=False)
        fig = px.bar(df_plot, x="winner", y="TF", hover_data=["TF"], labels={"winner": "Team", "TF":"Number of wins at homeground"})
        plot(fig)

def compare_wins(option1, option2):
    def wps(year):
        df_year = df["winner"].loc[df["season"]==year].value_counts().rename_axis('teams').reset_index(name='wins')
        df_year["season"] = year
        return df_year

    frames = [None]*12
    for i in range(2008, 2020):
        frames[i-2008] = wps(i)

    df_plot = pd.concat(frames)
    df_plot2 = df_plot.loc[df_plot["teams"].isin([option1, option2])]
    fig = px.line(df_plot2, x="season", y="wins", color="teams")
    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
        )
    )
    fig.data[0].update(mode='markers+lines')
    fig.data[1].update(mode='markers+lines')
    plot(fig)

def bat_field(decision):
    df["bat/field"] = "NO"
    df.loc[(df["toss_winner"] == df["winner"]) & (df["toss_decision"] == "bat"), "bat/field"] = "bat"
    df.loc[(df["toss_winner"] == df["winner"]) & (df["toss_decision"] == "field"), "bat/field"] = "field"
    df.loc[(df["bat/field"] == "NO") & (df["toss_decision"] == "field"), "bat/field"] = "bat"
    df.loc[(df["bat/field"] == "NO") & (df["toss_decision"] == "bat"), "bat/field"] = "field"
    
    df_batfield = df.groupby(["venue", "bat/field"]).size().reset_index(name='counts')
    df_total_matches = df_batfield.groupby(["venue"])["counts"].sum().reset_index(name="total_matches")
    df_batfield2 = df_batfield.copy()
    stad_matches = dict(zip(df_total_matches.venue, df_total_matches.total_matches))
    for index, row in df_batfield2.iterrows():
        for stadium in stad_matches:
            if row.venue == stadium:
                df_batfield2.at[index, "total_m"] = int(stad_matches[stadium])

    df_batfield2["total_m"] = df_batfield2["total_m"].astype(int)
    df_batfield2["perc_of_wins"] = round((df_batfield2["counts"]/df_batfield2["total_m"])*100,2)
        
    if decision == "all":
        fig  = px.bar(df_batfield2, y = "venue", x="perc_of_wins", orientation="h", color="bat/field", height=1000, labels={"venue":"Stadiums", "perc_of_wins":"Win percentage"})
        
    else:
        sorted_bf = df_batfield2.loc[df_batfield2["bat/field"]==str(decision)][:11].sort_values(by="perc_of_wins", ascending=True)
        fig  = px.bar(sorted_bf, y = "venue", x="perc_of_wins", orientation="h", opacity=0.7, labels={"venue":"Stadiums", "perc_of_wins":f"Win percentage with {decision} first"}, width=1000)       

    plot(fig)
    # st.plotly_chart(fig, use_container_width=False)

def win_margin():
    high_avg_margin_runs = (df.loc[df["win_by_runs"]!=0].groupby(["winner"])["win_by_runs"].mean()).sort_values(ascending=False).reset_index()
    high_avg_margin_wickets = (df.loc[df["win_by_wickets"]!=0].groupby(["winner"])["win_by_wickets"].mean()).sort_values(ascending=False).reset_index()
    fig = px.line(high_avg_margin_runs, x="winner", y="win_by_runs", labels={"winner":"Teams", "win_by_runs":"Average Win Margin (Runs)"})
    fig.data[0].update(mode='markers+lines')
    fig2 = px.line(high_avg_margin_wickets, x="winner", y="win_by_wickets", labels={"winner":"Teams", "win_by_wickets":"Average Win Margin (Wickets)"})
    fig2.data[0].update(mode='markers+lines')

    plot(fig)
    plot(fig2)

def streak():
    df_final = df_plot = pd.DataFrame(columns = ["season", "team", "streak"])

    for year in range(df["season"].min(), (df["season"].max())+1):
        team_list = list(df.loc[df["season"]==year, "team1"].unique())
        plot_dict = {}

        for team in team_list:
            df_filter_team = df.loc[df["season"]==year][(df["team1"]==str(team)) | (df["team2"]==str(team))]
            df_filter_team.sort_values(by="date", inplace=True)

            groups = df_filter_team["winner"].ne(df_filter_team["winner"].shift()).cumsum()
            df_agg = (   df_filter_team.groupby(groups,sort=False).agg(winner=('winner','first'),
                                                                       length=('winner','size'))
                        .sort_values('length',ascending=False)
                        .drop_duplicates('winner')
                      )
            value = df_agg.loc[df_agg["winner"]==str(team), "length"].iloc[0]

            plot_dict[team] = value

        key_max = max(plot_dict.keys(), key=(lambda k: plot_dict[k]))

        dict_to_df = {}
        data = []
        for team in plot_dict:
            if plot_dict[team] == plot_dict[key_max]:
                dict_to_df["season"] = year
                dict_to_df["team"] = team
                dict_to_df["streak"] = plot_dict[team]
                data.append(dict_to_df)
                df_plot = df_plot.append(data, True)

        df_final = pd.concat([df_final, df_plot])

    df_final.drop_duplicates(inplace=True)
    df_final.reset_index(inplace=True, drop=True)
    
    fig = px.bar(df_final, x="season", y="streak", color="team", barmode='group', height=400, 
                 labels = {"season":"Season", "streak":"Duration of streak (in number of games)"})
    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
        )
    )
    plot(fig)


def main():
    st.sidebar.title("MENU")
    home_val = st.sidebar.checkbox("Most Wins on Homeground")
    if home_val is True:
        st.header("Most Homeground Wins Per Season")
        year_home_win = st.slider(
            label="Select Year",
            min_value=int(df["season"].min()),
            max_value=int(df["season"].max()),
        )
        st.header(f"Most Homeground Wins in the year {year_home_win}")
        most_home_wins(df, year_home_win)

        st.header("Most Homeground Wins in all seasons ( 2008 - 2019 )")
        most_home_wins(df, 0)

    compare_val = st.sidebar.checkbox("Compare Team Wins Per Season")
    if compare_val is True:
        option1 = st.selectbox("Select Team 1", pd.unique(df["team1"]))
        option2 = st.selectbox("Select Team 2", pd.unique(df["team1"].loc[df["team1"]!=option1]))
        st.subheader(f"Comparing Wins per Season between {option1} and {option2}")
        compare_wins(option1, option2)

    batandfield_val = st.sidebar.checkbox("Stadiums preferring Bat first or Field first")
    if batandfield_val is True:
        st.subheader("Win Percentage for Stadiums when batting / fielding first")
        bat_field("all")

        st.subheader("[Top 10] Win percentage of stadiums with ")
        select = ["Bat First", "Field First"]
        select_option = st.selectbox("Select Bat or Field", select)
        if select_option is "Bat First":
            batandfield_option = "bat"
        else:
            batandfield_option = "field"
        
        bat_field(batandfield_option)

    win_margin_val = st.sidebar.checkbox("Teams with highest win margins in runs / wickets")
    if win_margin_val is True:
        win_margin()

    streak_val = st.sidebar.checkbox("Longest winning streak per season")
    if streak_val is True:
        streak()
