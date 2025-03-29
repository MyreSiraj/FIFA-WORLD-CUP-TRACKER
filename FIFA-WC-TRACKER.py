import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

data = {
    "Year": [2022, 2018, 2014, 2010, 2006, 2002, 1998, 1994, 1990, 1986, 1982, 1978, 1974, 1970, 1966, 1962, 1958, 1954, 1950, 1938, 1934, 1930],
    "Winner": ["Argentina", "France", "Germany", "Spain", "Italy", "Brazil", "France", "Brazil", "Germany", "Argentina", 
               "Italy", "Argentina", "Germany", "Brazil", "United Kingdom", "Brazil", "Brazil", "Germany", "Uruguay", "Italy", 
               "Italy", "Uruguay"],
    "Runner-up": ["France", "Croatia", "Argentina", "Netherlands", "France", "Germany", "Brazil", "Italy", "Argentina", 
                  "West Germany", "West Germany", "Netherlands", "Netherlands", "Italy", "West Germany", "Czechoslovakia", 
                  "Sweden", "Hungary", "Brazil", "Hungary", "Czechoslovakia", "Argentina"]
}

df = pd.DataFrame(data)

winners_count = df["Winner"].value_counts().reset_index()
winners_count.columns = ["Country", "Wins"]

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center', 'color': 'white'}),

    dcc.Graph(id="world_map"),

    dcc.Dropdown(
        id="country_dropdown",
        options=[{"label": c, "value": c} for c in winners_count["Country"]],
        placeholder="Select a Country",
    ),
    html.Div(id="country_wins", style={'color': 'red'}),

    dcc.Dropdown(
        id="year_dropdown",
        options=[{"label": str(y), "value": y} for y in df["Year"].unique()],
        placeholder="Select a Year",
    ),
    html.Div(id="year_results", style={'color': 'red'}),
])

@app.callback(
    Output("world_map", "figure"),
    [Input("country_dropdown", "value"),
     Input("year_dropdown", "value")]
)
     
def update_map(selected_country, selected_year):

    filtered_df = winners_count.copy()

    if selected_country:
        filtered_df = filtered_df[filtered_df["Country"] == selected_country]
    
    if selected_year:
        year_data = df[df["Year"] == selected_year]
        winner = year_data["Winner"].values[0]
        runner_up = year_data["Runner-up"].values[0]
        
        filtered_df = pd.DataFrame({"Country": [winner, runner_up], "Wins": [1, 0]})

    fig = px.choropleth(
        filtered_df, 
        locations="Country", 
        locationmode="country names",
        color="Wins", 
        title="FIFA World Cup Wins",
        color_continuous_scale="reds",
        hover_name="Country",
        hover_data={"Country": False, "Wins": True}
    )
    
    return fig

@app.callback(
    Output("country_wins", "children"),
    Input("country_dropdown", "value")
)
def display_country_wins(selected_country):
    if selected_country:
        wins = winners_count[winners_count["Country"] == selected_country]["Wins"].values[0]
        return f"{selected_country} has won {wins} times."
    return "Select a country to see the number of wins."

@app.callback(
    Output("year_results", "children"),
    Input("year_dropdown", "value")
)
def display_year_results(selected_year):
    if selected_year:
        row = df[df["Year"] == selected_year]
        winner = row["Winner"].values[0]
        runner_up = row["Runner-up"].values[0]
        return f"In {selected_year}, {winner} won against {runner_up}."
    return "Select a year to see the winner and runner-up."

if __name__ == "__main__":
    app.run(debug=True)
