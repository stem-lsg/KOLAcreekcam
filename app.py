import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calmap # pip install calmap
import dash
from dash import html
import base64
import os

# --- Load and preprocess data ---
df = pd.read_csv("creekcamdata.csv", parse_dates=["date"])
df.rename(columns={"date": "Date"}, inplace=True)

df.set_index("Date", inplace=True)
df = df.asfreq("D")
df.fillna(0, inplace=True)

# --- Ensure folders exist ---
os.makedirs("heatmaps", exist_ok=True)
image_folder = "select_images"

# --- Encode image files ---
def encode_image(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{encoded}"

# --- Generate calendar heatmaps and collect layout ---
app = dash.Dash(__name__)
app.title = "Creek Cam Calendar Heatmaps"
server = app.server

heatmap_divs = []

for col in df.columns:
    # Plot and save calendar heatmap
    fig = calmap.calendarplot(
        df[col],
        cmap="YlGnBu",
        fillcolor="lightgray",
        linewidth=0.5,
        fig_kws=dict(figsize=(14, 4))
    )
    plt.suptitle(f"Calendar Heatmap: {col}", fontsize=16)
    heatmap_path = f"heatmaps/{col}_calendar_heatmap.png"
    plt.savefig(heatmap_path)
    plt.close()

    # Add corresponding reference image if available
    col_image_path = os.path.join(image_folder, f"{col}.jpg")
    image_components = []

    if os.path.exists(col_image_path):
        encoded_col_image = encode_image(col_image_path)
        image_components.append(html.Img(
            src=encoded_col_image,
            style={"width": "100%", "height": "auto", "marginBottom": "20px"}
        ))

    # Encode heatmap
    encoded_heatmap = encode_image(heatmap_path)

    # Build div
    heatmap_divs.append(html.Div([
        html.H3(f"Calendar Heatmap: {col}", style={"textAlign": "center"}),
        *image_components,
        html.Img(src=encoded_heatmap, style={"width": "100%", "height": "auto"})
    ], style={"marginBottom": "50px"}))

# --- App Layout ---
app.layout = html.Div([
    html.H1("Creek Cam Calendar Heatmaps", style={"textAlign": "center"}),
    *heatmap_divs
])

# --- Run ---
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
