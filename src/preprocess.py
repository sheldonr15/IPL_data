# from .sheets import data, headers
# import sheets
import pandas as pd
from datetime import datetime

def load_dataset():
    # df = pd.DataFrame(data, columns=headers)
    df = pd.read_csv("data/matches.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["city"] = df["city"].fillna("Dubai")
    df["team1"] = df["team1"].replace("Rising Pune Supergiants", "Rising Pune Supergiant")
    df["team2"] = df["team2"].replace("Rising Pune Supergiants", "Rising Pune Supergiant")
    df["winner"] = df["winner"].replace("Rising Pune Supergiants", "Rising Pune Supergiant")
    df["city"] = df["city"].replace("Bangalore", "Bengaluru")
    # df["city"].dropna(inplace=True)
    df["venue"] = df["venue"].replace("Rajiv Gandhi International Stadium, Uppal", "Rajiv Gandhi Intl. Cricket Stadium")
    df["venue"] = df["venue"].replace("Punjab Cricket Association IS Bindra Stadium, Mohali", "Punjab Cricket Association Stadium")
    df["venue"] = df["venue"].replace("Punjab Cricket Association Stadium, Mohali", "Punjab Cricket Association Stadium")
    df["venue"] = df["venue"].replace("M Chinnaswamy Stadium", "M. Chinnaswamy Stadium")
    df["venue"] = df["venue"].replace("Feroz Shah Kotla", "Feroz Shah Kotla Ground")
    df["venue"] = df["venue"].replace("MA Chidambaram Stadium, Chepauk", "M. A. Chidambaram Stadium")
    df["venue"] = df["venue"].replace("IS Bindra Stadium", "Punjab Cricket Association Stadium")
    df["venue"] = df["venue"].replace("ACA-VDCA Stadium", "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium")

    team_city = {
        'Sunrisers Hyderabad': ['Hyderabad', 'Visakhapatnam'],
        'Mumbai Indians': 'Mumbai',
        'Gujarat Lions': ['Rajkot', 'Kanpur'],
        'Rising Pune Supergiant': 'Pune',
        'Royal Challengers Bangalore': 'Bengaluru',
        'Kolkata Knight Riders': 'Kolkata',
        'Delhi Daredevils': 'Delhi',
        'Kings XI Punjab': ['Chandigarh', 'Mohali', 'Indore', 'Dharamsala'],
        'Chennai Super Kings': ['Chennai', 'Ranchi'],
        'Rajasthan Royals': ['Jaipur', 'Ahmedabad'],
        'Deccan Chargers': ['Hyderabad', 'Visakhapatnam'],
        'Kochi Tuskers Kerala': 'Kochi',
        'Pune Warriors': 'Pune',
        'Delhi Capitals': 'Delhi'
    }    
    return df, team_city

df, team_city = load_dataset()