import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calmap
import dash
from dash import html
import os

# --- Load and preprocess data ---
df = pd.read_csv("creekcamdata.csv", parse_dates=["date"])
df.rename(columns={"date": "Date"}, inplace=True)

df.set_index("Date", inplace=True)
df = df.asfreq("D")
df.fillna(0, inplace=True)

# --- Ensure heatmaps are saved into assets ---
os.makedirs("assets/heatmaps", exist_ok=True)
os.makedirs("assets/select_images", exist_ok=True)

# --- Generate calendar heatmaps ---
for col in df.columns:
    fig = calmap.calendarplot(
        df[col],
        cmap="YlGnBu",
        fillcolor="lightgray",
        linewidth=0.5,
        fig_kws={"figsize": (14, 4)}
    )
    plt.suptitle(f"Calendar Heatmap: {col}", fontsize=16)
    plt.savefig(f"assets/heatmaps/{col}_calendar_heatmap.png", bbox_inches='tight')
    plt.close()

# --- Build Dash layout ---
app = dash.Dash(__name__)
app.title = "Creek Cam Calendar Heatmaps"
server = app.server

heatmap_divs = []

for col in df.columns:
    heatmap_path = f"/assets/heatmaps/{col}_calendar_heatmap.png"
    ref_image_path = f"/assets/select_images/{col}.jpg"

    components = [html.H3(f"Calendar Heatmap: {col}", style={"textAlign": "center"})]

    if os.path.exists(f"assets/select_images/{col}.jpg"):
        components.append(html.Img(src=ref_image_path, style={"width": "100%", "marginBottom": "20px"}))

    components.append(html.Img(src=heatmap_path, style={"width": "100%"}))

    heatmap_divs.append(html.Div(components, style={"marginBottom": "50px"}))

# --- Layout ---
app.layout = html.Div([
    html.H1("Creek Cam Calendar Heatmaps", style={"textAlign": "center"}),
    *heatmap_divs
])

if __name__ == "__main__":
    app.run_server(debug=True)


# # My Dash app code will live here
# import pandas as pd
# import dash
# from dash import dcc, html
# import plotly.express as px

# # Load and prep data
# df = pd.read_csv("creekcamdata.csv", parse_dates=["date"])
# df.rename(columns={"date": "Date"}, inplace=True)

# # Add missing dates from the Sunday before the first record
# start_date = df["Date"].min()
# sunday_before = start_date - pd.Timedelta(days=start_date.weekday() + 1)
# full_dates = pd.DataFrame({"Date": pd.date_range(start=sunday_before, end=df["Date"].max())})
# df = full_dates.merge(df, on="Date", how="left")

# # Dash app instance
# app = dash.Dash(__name__)
# app.title = "Barebones Heatmap Test"
# server = app.server

# # Create calendar heatmaps for each category
# heatmaps = []
# for col in df.columns[1:]:
#     temp_df = df[["Date", col]].copy()
#     temp_df[col].fillna(0, inplace=True)  # Fill missing values with 0
#     temp_df["Week"] = temp_df["Date"].dt.isocalendar().week
#     temp_df["Weekday"] = temp_df["Date"].dt.weekday
#     temp_df["Year"] = temp_df["Date"].dt.year

#     fig = px.density_heatmap(
#         temp_df,
#         x="Weekday",
#         y="Week",
#         z=col,
#         color_continuous_scale="YlOrBr",
#         title=f"Calendar Heatmap: {col}",
#         labels={
#             "Weekday": "Day of Week",
#             "Week": "Week Number",
#             col: "Count"
#         }
#     )
#     fig.update_layout(
#         margin=dict(t=40, b=20),
#         height=400
#     )
#     fig.update_yaxes(autorange="reversed")
#     heatmaps.append(html.Div([dcc.Graph(figure=fig)], style={"marginBottom": "50px"}))

# # Layout
# app.layout = html.Div([
#     html.H1("Creek Cam Calendar Heatmaps", style={"textAlign": "center"}),
#     *heatmaps
# ])

# # Run the app
# if __name__ == "__main__":
#     app.run_server(debug=True)
