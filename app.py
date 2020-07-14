from flask import Flask
import pandas as pd ;
import dash
import dash_core_components as dcc ; import dash_html_components as html
import dash_table ; from dash.dependencies import Output, Input
import pickle

################################## APP SETTING ###############################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Inscripciones de POSGRADOS'
server = app.server # the Flask app
################################## APP SETTING ###############################
#################################### PYTHON ##################################
cat_features = ['profesion', 'sitlabor', 'niveleduc', 'ecivil', 'region']

with open('assets/profesion.pkl', 'rb') as cat_feature:
    profesiones = pickle.load(cat_feature)

with open('assets/sitlabor.pkl', 'rb') as cat_feature:
    sitlaborales = pickle.load(cat_feature)

with open('assets/niveleduc.pkl', 'rb') as cat_feature:
    niveleducativos = pickle.load(cat_feature)

with open('assets/ecivil.pkl', 'rb') as cat_feature:
    eciviles = pickle.load(cat_feature)

with open('assets/region.pkl', 'rb') as cat_feature:
    regiones = pickle.load(cat_feature)

sexos = ['F','M']

#profesiones.append('otro')


profesiones.sort()
sitlaborales.sort()
niveleducativos.sort()
eciviles.sort()
regiones.sort()

anti_rng = (0, 80)
edad_rng = (14, 98)
ries_rng = (0, 974)
exig_rng = (0, 9133300)

#################################### MODEL ##################################
with open('assets\cat_model.pkl', 'rb') as f_catboost:
    model = pickle.load(f_catboost)
#################################### TABLA ##################################
def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
#################################### TABLA ##################################
################################## APP LAYOUT ################################
app.layout = html.Div([
    html.Div([
        html.H2('Desafio Integrador', className='four columns'),
        html.H4('Grupo I', className='eight columns'),

    ], className='row'),
    html.Hr(className='linea'),

    html.Div([
        html.Div([
            html.Label('Antiguedad Laboral'),
            dcc.Slider(id='sl-antiguedad',
                       marks={i: str(i) for i in range(0,anti_rng[1]+1,10) },
                       min=anti_rng[0], max=anti_rng[1],
                       dots=True, step=1, tooltip={'always_visible': False, 'placement':'top'},
                       ),
                ],className='six columns'),
            html.Div([
                html.Label('Riesgo'),
                dcc.Input(id='sl-riesgo', type='number')
            ], className='three columns'),

            html.Div([
                html.Label('Exigencia'),
                dcc.Input(id='sl-exigencia', type='number')
            ], className='three columns'),


        ],className='row'),

    html.Div([

    ],className='row'),


    html.Div([
        html.Label('Situación Laboral', className='row'),
        dcc.RadioItems(
            id='rb-sitlab',
            options=[{'label': sitlaborales[k], 'value': sitlaborales[k]} for k in range(len(sitlaborales))],
            labelStyle={'display': 'inline-block', 'margin-right': '15px'},
            className='niveles'
        ),
    ], className='row'),

    # DROPDOWN PROFESION
    html.Div([
        html.Div([
            html.Label('Profesión', className='row'),
            dcc.Dropdown(options=[{'label': profesiones[k], 'value': profesiones[k]} for k in range(len(profesiones))],
                         id = 'dr-profesion', value='', clearable=False,
                         ),
                ], className='six columns'),

        html.Div([
            html.Label('Nivel Educativo', className='row'),
            dcc.Dropdown(options=[{'label': niveleducativos[k], 'value': niveleducativos[k]} for k in range(len(niveleducativos))],
                         id='rb-nivel', value='', clearable=False,),
        ], className='six columns'),

    ], className='row'),

    html.Hr(className='linea'),


    html.Div([
            html.Label('Edad'),
            dcc.Slider(id='sl-edad',
                       marks={i: str(i) for i in range(0,edad_rng[1],5) },
                       min=edad_rng[0], max=edad_rng[1],
                       dots=True, step=1, tooltip={'always_visible': False, 'placement': 'top'},
                       ),
        ], className='row'),

    html.Div([
        html.Div([
            html.Label('Sexo', className='row'),
            dcc.Dropdown(options=[{'label': sexos[k], 'value': sexos[k]} for k in range(len(sexos))],
                         id='rb-sexo', value='', clearable=False, ),
        ], className='three columns'),

        html.Div([
            html.Label('Estado Civil', className='row'),
            dcc.Dropdown(options=[{'label': eciviles[k], 'value': eciviles[k]} for k in range(len(eciviles))],
                         id='rb-estcivil', value='', clearable=False, ),
        ], className='three columns'),

        html.Div([
            html.Label('Region', className='row'),
            dcc.Dropdown(options=[{'label': regiones[k], 'value': regiones[k]} for k in range(len(regiones))],
                         id='rb-region', value='', clearable=False, ),
        ], className='three columns'),

        html.Div([
            html.Label('Nacionalidad', className='row'),
            dcc.Dropdown(options=[{'label': k, 'value': k} for k in ['Argentino','Extranjero']],
                         id='rb-nacionalidad', value='', clearable=False),
        ], className='three columns'),
    ],className='row'),

    # guardamos el array en un hidden DIV
    html.Div([html.P(id='profesion-el'),html.P(id='edad-el'),html.P(id='riesgo-el'),html.P(id='exigencia-el'),html.P(id='antig-el'),html.P(id='sitlabor-el'),
              html.P(id='nivel-el'),html.P(id='sexo-el'),html.P(id='ecivil-el'),html.P(id='region-el'),html.P(id='nacionalidad-el')
              ],hidden=True),

    html.Hr(className='linea2'),

    html.Div([html.H5(id='model-predict'),
              html.Label('Prediccion para' )]
             ,className='Row'),

    # TABLA DE DATOS
    dash_table.DataTable(
        id='tabla-datos',

    ),

],className='cuerpo')

################################## APP LAYOUT ###################################
################################## CALL BACKS ###################################
@app.callback(
    [
        Output('antig-el', 'children'),
        Output('edad-el', 'children'),
        Output('riesgo-el', 'children'),
        Output('exigencia-el', 'children'),
        Output('profesion-el', 'children'),
        Output('sitlabor-el', 'children'),
        Output('nivel-el', 'children'),
        Output('sexo-el', 'children'),
        Output('ecivil-el', 'children'),
        Output('region-el', 'children'),
        Output('nacionalidad-el', 'children'),
    ],
    [
        Input('sl-antiguedad', 'value'),
        Input('sl-edad', 'value'),
        Input('sl-riesgo', 'value'),
        Input('sl-exigencia', 'value'),
        Input('dr-profesion', 'value'),
        Input('rb-sitlab', 'value'),
        Input('rb-nivel', 'value'),
        Input('rb-sexo', 'value'),
        Input('rb-estcivil', 'value'),
        Input('rb-region', 'value'),
        Input('rb-nacionalidad', 'value')
    ])
def set_selected(antig_el,edad_el,riesgo_el,exigencia_el,profesion_el,sitlabor_el, nivel_el, sexo_el, ecivil_el,region_el, nacionalidad_el):
    return antig_el, edad_el, riesgo_el, exigencia_el,profesion_el,sitlabor_el, nivel_el, sexo_el, ecivil_el, region_el, nacionalidad_el

@app.callback(
    [
        Output('tabla-datos', 'data'),
        Output('tabla-datos', 'columns'),
        Output('model-predict','children')
    ],
    [Input('sl-antiguedad', 'value'),
     Input('sl-edad', 'value'),
     Input('sl-riesgo', 'value'),
     Input('sl-exigencia', 'value'),
     Input('dr-profesion', 'value'),
     Input('rb-sitlab', 'value'),
     Input('rb-nivel', 'value'),
     Input('rb-sexo', 'value'),
     Input('rb-estcivil', 'value'),
     Input('rb-region', 'value'),
     Input('rb-nacionalidad', 'value')
     ])

def set_display_children(antig_el, edad_el, riesgo_el, exigencia_el, profesion_el,sitlabor_el,nivel_el, sexo_el,ecivil_el,region_el,nacionalidad_el):
    global model
    new = []
    salected_colu = ['Antigüedad','Edad','Riesgo','Exigencia','Profesión','Situación Laboral','Nivel Educativo','Sexo','Estado Civil','Región','Nacionalidad']
    salected_data = pd.DataFrame([[antig_el, edad_el, riesgo_el, exigencia_el, profesion_el,sitlabor_el,
                     nivel_el, sexo_el,ecivil_el,region_el,nacionalidad_el]],columns = salected_colu)

    new.append(antig_el)
    new.append(edad_el)
    new.append(riesgo_el)
    new.append(exigencia_el)

    for i in profesiones:
        if i == profesion_el: new.append(1)
        else:                      new.append(0)

    for i in sitlaborales:
        if i == sitlabor_el:  new.append(1)
        else:                      new.append(0)

    for i in niveleducativos:
        if i == nivel_el:  new.append(1)
        else:                   new.append(0)

    for i in sexos:
        if i == sexo_el:  new.append(1)
        else:                  new.append(0)

    for i in eciviles:
        if i == ecivil_el:  new.append(1)
        else:                  new.append(0)

    for i in regiones:
        if i == region_el:  new.append(1)
        else:                  new.append(0)

    if nacionalidad_el == 'Argentino':         new.append(1)
    else:                                           new.append(0)


    try:        result = model.predict(new)
    except:     result = 'Complete todos los datos'

    return [salected_data.to_dict('records'),
            [{"name": salected_colu[i], "id": salected_colu[i]} for i in range(len(salected_colu))],
            'Clase predicha: '+str(result[0]),
            ]


################################### APP LOOP ####################################
if __name__ == '__main__':
    app.run_server(debug=True)