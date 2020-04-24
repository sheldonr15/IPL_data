from .sheets import data, headers
# import sheets
import pandas as pd

def load_dataset():
    df = pd.DataFrame(data, columns=headers)
    df["team1"] = df["team1"].replace("Rising Pune Supergiants", "Rising Pune Supergiant")
    df["team2"] = df["team2"].replace("Rising Pune Supergiants", "Rising Pune Supergiant")
    df["winner"] = df["winner"].replace("Rising Pune Supergiants", "Rising Pune Supergiant")
    df["city"] = df["city"].replace("Bangalore", "Bengaluru")
    df["city"].dropna(inplace=True)

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