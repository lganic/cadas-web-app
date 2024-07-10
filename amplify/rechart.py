import pandas as pd
import json

# Read CSV file
df = pd.read_csv('Classsifications.csv', encoding='utf-8-sig')

# Group by date and category
grouped = df.groupby(['time per 12 hours', 'events.classifications.keyword: Descending'])['Number of audio clips'].sum().unstack(fill_value=0).reset_index()

# Prepare data for Plotly
chart_data = {
    'dates': grouped['time per 12 hours'].tolist(),
    'categories': grouped.columns[1:].tolist(),
    'values': [grouped[category].tolist() for category in grouped.columns[1:]]
}

# Save as JSON
with open('data/chart_data.json', 'w') as json_file:
    json.dump(chart_data, json_file)
