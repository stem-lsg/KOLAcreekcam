# My Dash app code will live here
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load and prep data
df = pd.read_csv("creekcamdata.csv", parse_dates=["date"])
df.rename(columns={"date": "Date"}, inplace=True)

# Add missing dates from the Sunday before the first record
start_date = df["Date"].min()
sunday_before = start_date - pd.Timedelta(days=start_date.weekday() + 1)
full_dates = pd.DataFrame({"Date": pd.date_range(start=sunday_before, end=df["Date"].max())})
df = full_dates.merge(df, on="Date", how="left")

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Creek Cam Calendar Heatmaps"

# Create calendar heatmaps for each category
heatmaps = []
for col in df.columns[1:]:
    temp_df = df[["Date", col]].copy()
    temp_df[col].fillna(0, inplace=True)  # Fill missing values with 0
    temp_df["Week"] = temp_df["Date"].dt.isocalendar().week
    temp_df["Weekday"] = temp_df["Date"].dt.weekday
    temp_df["Year"] = temp_df["Date"].dt.year

    fig = px.density_heatmap(
        temp_df,
        x="Weekday",
        y="Week",
        z=col,
        color_continuous_scale="YlOrBr",
        title=f"Calendar Heatmap: {col}",
        labels={
            "Weekday": "Day of Week",
            "Week": "Week Number",
            col: "Count"
        }
    )
    fig.update_layout(
        margin=dict(t=40, b=20),
        height=400
    )
    fig.update_yaxes(autorange="reversed")
    heatmaps.append(html.Div([dcc.Graph(figure=fig)], style={"marginBottom": "50px"}))

# Layout
app.layout = html.Div([
    html.H1("Creek Cam Calendar Heatmaps", style={"textAlign": "center"}),
    *heatmaps
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
