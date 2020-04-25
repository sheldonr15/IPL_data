import pandas as pd
import plotly.express as px
from .preprocess import df, team_city
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



def main():
    st.sidebar.title("MENU")
    home_val = st.sidebar.checkbox("Most Wins on Homeground")
    if home_val is True:
        st.header("Most Wins Per Season")
        year_home_win = st.slider(
            label="Select Year",
            min_value=int(df["season"].min()),
            max_value=int(df["season"].max()),
        )
        st.header(f"Most Homeground Wins in the year {year_home_win}")
        most_home_wins(df, year_home_win)

        st.header("Most Homeground Wins in all seasons ( 2008 - 2019 )")
        most_home_wins(df, 0)

    compare_val = st.sidebar.checkbox("Compare Wins Per Team")
    if compare_val is True:
        option1 = st.selectbox("Select Team 1", pd.unique(df["team1"]))
        option2 = st.selectbox("Select Team 2", pd.unique(df["team1"].loc[df["team1"]!=option1]))
        st.subheader(f"Comparing Wins per Season between {option1} and {option2}")
        compare_wins(option1, option2)

    batandfield_val = st.sidebar.checkbox("Stadiums preferring Bat first or Field first")
    if batandfield_val is True:
        st.subheader("Win Percentage for Stadiums when batting / fielding first")
        bat_field("all")

        st.subheader("Stats of stadiums with ")
        select = ["Bat First", "Field First"]
        select_option = st.selectbox("Select Bat or Field", select)
        if select_option is "Only Bat First":
            batandfield_option = "bat"
        else:
            batandfield_option = "field"
        
        bat_field(batandfield_option)

