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

# Dash app instance
app = dash.Dash(__name__)
app.title = "Barebones Heatmap Test"
server = app.server

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


# import dash
# from dash import dcc, html
# import plotly.express as px
# import pandas as pd
# import datetime

# # Sample dummy dataset
# dates = pd.date_range(start="2025-05-01", end="2025-05-15", freq="D")
# data = pd.DataFrame({
#     "Date": dates,
#     "TestColumn": [i % 7 for i in range(len(dates))]
# })

# # Dash app instance
# app = dash.Dash(__name__)
# app.title = "Barebones Heatmap Test"
# server = app.server

# # Basic calendar-style heatmap
# data["Week"] = data["Date"].dt.isocalendar().week
# data["Weekday"] = data["Date"].dt.weekday

# fig = px.density_heatmap(
#     data,
#     x="Weekday",
#     y="Week",
#     z="TestColumn",
#     color_continuous_scale="YlGnBu",
#     title="Sample Calendar Heatmap",
#     labels={"Weekday": "Day of Week", "Week": "Week Number"}
# )
# fig.update_yaxes(autorange="reversed")

# # App layout
# app.layout = html.Div([
#     html.H2("Barebones Test Heatmap", style={"textAlign": "center"}),
#     dcc.Graph(figure=fig)
# ])

# # Gunicorn-compatible server entry
# if __name__ == "__main__":
#     app.run_server(debug=True)
