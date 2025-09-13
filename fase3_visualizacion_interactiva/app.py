import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# ---------------------------
# 1. Cargar dataset limpio
# ---------------------------
df = pd.read_csv(r"C:\Users\Yerko\OneDrive\Universidad\UNAB\8vo Trimestre\Ciencia de Datos\10. Pryecto\spacex-capstone\fase1_ingenieria_datos_src\spacex_launches_clean_v2.csv", sep=";")


# Asegurarnos de que landing_success sea categórico (para las gráficas)
df['landing_success'] = df['landing_success'].astype(str)

# ---------------------------
# 2. Inicializar la app Dash
# ---------------------------
app = dash.Dash(__name__)

# Opciones del Dropdown (sitios de lanzamiento)
sites = df['launchpad'].unique()
options = [{'label': 'Todos los sitios', 'value': 'ALL'}] + \
          [{'label': s, 'value': s} for s in sites]

# ---------------------------
# 3. Layout del Dashboard
# ---------------------------
app.layout = html.Div([
    html.H1("Panel de lanzamientos SpaceX", style={'textAlign': 'center'}),

    # Dropdown para seleccionar sitio
    dcc.Dropdown(id='site-dropdown',
                 options=options,
                 value='ALL',
                 placeholder="Selecciona un sitio de lanzamiento",
                 searchable=True),

    html.Br(),

    # Pie chart
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    # Slider para filtrar por payload
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=500,
                    marks={0: '0', 2500: '2.5k', 5000: '5k', 7500: '7.5k', 10000: '10k'},
                    value=[df['payload_mass_kg'].min(), df['payload_mass_kg'].max()]),

    html.Br(),

    # Scatter plot
    dcc.Graph(id='success-payload-scatter-chart')
])

# ---------------------------
# 4. Callbacks
# ---------------------------

# Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))
def update_pie(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(df, names='launchpad', values='landing_success',
                     title="Éxitos de lanzamiento por sitio")
    else:
        dff = df[df['launchpad'] == selected_site]
        fig = px.pie(dff, names='landing_success',
                     title=f"Éxitos/Fallos en {selected_site}")
    return fig

# Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')])
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    dff = df[(df['payload_mass_kg'] >= low) & (df['payload_mass_kg'] <= high)]
    if selected_site != 'ALL':
        dff = dff[dff['launchpad'] == selected_site]
    fig = px.scatter(dff, x='payload_mass_kg', y='landing_success',
                     color='rocket_name',
                     title="Relación Payload vs Éxito de aterrizaje")
    return fig

# ---------------------------
# 5. Ejecutar servidor
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
