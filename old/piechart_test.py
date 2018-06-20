import plotly.offline as py
import plotly.graph_objs as go

fig = {
  "data": [
    {
      "values": [10, 50, 30, 10],
      "labels": [
        r"Data Extraction",
        r"Cleaning & Organizing Data",
        r"Refining Alanlytics Strategies",
        r"Developing Visualizations"
      ],
      # "domain": {"x": [0, .48]},
      "name": "GHG Emissions",
      # "hoverinfo":"label+percent+name",
      "hole": .4,
      "type": "pie",
      "textinfo":"text",
      "text":[
        r"Data Extraction",
        r"Cleaning & Organizing Data",
        r"Refining Alanlytics Strategies",
        r"Developing Visualizations"
      ],
      "textfont":dict(size=50)
    }],
  "layout": {
    "annotations": [
    {
        "font": {
            "size": 50
        },
        "showarrow": False,
        "text": "Total Time",
        "x": 0.5,
        "y": 0.5
    }
  ]
}
}
py.plot(fig, filename='donut')

print()