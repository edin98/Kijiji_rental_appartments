from dash import dcc, html, Dash, dash_table, callback, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv('Renting_properties_data_2.csv')
df = df.rename(columns={'Unnamed: 0': 'Id'})
df = df[['Id', 'address', 'price', 'area', 'sublocality', 'postal_code', 'location_type', 'location']]
df.set_index('Id')

by_sublocality = df.groupby('sublocality').mean(numeric_only=True).sort_values('price')
by_sublocality.drop('Id', inplace=True, axis=1)
by_sublocality.reset_index(inplace=True)

with open(
        '/Users/edinsonjimenezarita/Projects/WebScraping Project/Renting_properties_project/montreal_shapefile.geojson',
        encoding='utf-8') as shapefile:
    mtl_geojson = json.load(shapefile)
#The amount of boroughs in geojson are 33, but in our data is only 15
mtl_geojson['features'][0]['properties']['borough'] = 'Ahuntsic-Cartierville'
mtl_geojson['features'][8]['properties']['borough'] = 'Côte Saint-Luc'
mtl_geojson['features'][17]['properties']['borough'] = 'Côte-Des-Neiges—Notre-Dame-De-Grâce'
mtl_geojson['features'][20]['properties']['borough'] = 'LaSalle'
mtl_geojson['features'][11]['properties']['borough'] = 'Le Plateau-Mont-Royal'
mtl_geojson['features'][5]['properties']['borough'] = 'Le Sud-Ouest'
mtl_geojson['features'][21]['properties']['borough'] = 'Mercier-Hochelaga-Maisonneuve'
mtl_geojson['features'][26]['properties']['borough'] = 'Rosemont—La Petite-Patrie'
mtl_geojson['features'][28]['properties']['borough'] = 'Saint-Laurent'
mtl_geojson['features'][12]['properties']['borough'] = 'Saint-Léonard'
mtl_geojson['features'][30]['properties']['borough'] = 'Verdun'
mtl_geojson['features'][6]['properties']['borough'] = 'Ville-Marie'
mtl_geojson['features'][31]['properties']['borough'] = 'Villeray—Saint-Michel—Parc-Extension'
mtl_geojson['features'][32]['properties']['borough'] = 'Westmount'

mtlmap_fig = px.choropleth_mapbox(
    by_sublocality,
    geojson=mtl_geojson,
    locations='sublocality',
    featureidkey='properties.borough',
    color='price',
    mapbox_style='open-street-map',
    color_discrete_map={
        '> 600-700': '#ecd93b',
        '> 700-800': '#dfae5a',
        '> 800-900': '#df825a',
        '> 900-1000': '#CC0101',
        '> 1000-1100': '#A80101',
        '> 1100-1200': '#800e0e',
        '> 1200-1300': '#650e0e',
        '> 1300-1500': '#500e0e',
        '> 1500': '#350e0e',
    },
    zoom=9,
    center={'lat': 45.55, 'lon': -73.75},
    hover_name='sublocality'
)

mtlmap_fig.update_geos(fitbounds="locations")

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.H1('Hello Dash!', className='text-primary text-center')
    ]),

    dbc.Row([
        html.Div('My First App with Data, Graph, and Controls', className="text-primary text-center fs-3")
    ]),


    dbc.Row([

        dbc.Col([
            dash_table.DataTable(data=by_sublocality.to_dict('records'), page_size=10,
                                 style_table={'overflowX': 'auto'})
        ], width=7),

        dbc.Col([
            dcc.Graph(figure=mtlmap_fig, responsive=True)
        ], width=5),

        dbc.Col(html.Hr()),

        dbc.Row([
            dbc.RadioItems(options=[{"label": x, "value": x} for x in ['price', 'area']],
                           value='price',
                           inline=True,
                           id='radio-buttons-final')
        ]),

        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final')
        ], width=12),

        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=15, style_table={'overflowX': 'auto'})
        ], width=12)
    ]),

], fluid=True)


@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='sublocality', y=col_chosen, histfunc='avg')
    return fig


if __name__ == "__main__":
    app.run_server()
