from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/star_chart', methods=['GET'])
def generate_star_chart():
    df = pd.read_csv('finaleee.csv')
    stars = df.to_dict('records')
    inclination = 89.764
    eccentricity = 0.72

    chart_data = {
        "data": [],
        "layout": {
            "title": "Star Chart from Kepler-22b Perspective",
            "geo": {
                "projection": {
                    "type": "azimuthal equidistant",
                    "scale": 150
                },
                "showland": False,
                "showlakes": False,
                "showocean": False,
                "showrivers": False,
                "showcountries": False,
                "showcoastlines": False,
                "showframe": False,
                "bgcolor": "black",
                "lataxis": {
                    "showgrid": True,
                    "gridcolor": "white",
                    "range": [-90, 90],
                    "tickvals": [-90, -60, -30, 0, 30, 60, 90],
                    "ticktext": ["90°S", "60°S", "30°S", "Equator", "30°N", "60°N", "90°N"],
                    "tickfont": {"color": "white"}
                },
                "lonaxis": {
                    "showgrid": True,
                    "gridcolor": "white",
                    "range": [-180, 180],
                    "tickvals": [-180, -120, -60, 0, 60, 120, 180],
                    "tickfont": {"color": "white"}
                }
            },
            "plot_bgcolor": "black",
            "paper_bgcolor": "black",
            "titlefont": {"color": "white"},
            "showlegend": False,
        }
    }

    valid_distances = [s['distance (pc)'] for s in stars if pd.notnull(s['distance (pc)'])]
    max_distance = np.max(valid_distances) if valid_distances else 1

    for star in stars:
        l = star['l (deg)']
        b = star['b (deg)']
        distance = star['distance (pc)']
        
        if pd.isnull(l) or pd.isnull(b) or pd.isnull(distance):
            continue

        transparency = np.exp(-distance / max_distance) if distance <= max_distance else 0
        transparency = np.clip(transparency, 0.02, 0.9)

        color = (
            1,
            1,
            1,
            transparency
        )
        
        size = 5 * (1 - (distance / max_distance)) ** 0.8
        
        chart_data["data"].append({
            "type": "scattergeo",
            "mode": "markers",
            "lon": [l],
            "lat": [b],
            "marker": {
                "color": f'rgba(255, 255, 255, {transparency})',
                "size": size,
                "line": {
                    "width": 0.5,
                    "color": f'rgba(255, 255, 255, {transparency})'
                }
            }
        })

    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)
