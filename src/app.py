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
