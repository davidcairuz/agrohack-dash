# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

wanted_columns = ['Custo total','Depreciação','Faturamento Bruto','Receita Liquida','Lucro Bruto','Resultado']
graph_columns = ['Alimentação','Mão-de-Obra','Sanidade','Reposição','Impostos','Despesas Diversas','Pró-Labore','Depreciação']

df = pd.read_csv('clientes.csv')
df.columns = df.columns.str.strip()
us = df.iloc[0]

def plot_pie(df):
    us = df.iloc[0]
    pie_labels = graph_columns
    pie_values = [us[i] for i in pie_labels]

    pie_trace = go.Pie(labels=pie_labels, values=pie_values)
    return pie_trace

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], style={'backgroundColor':'#fafcff'})

home_layout = html.Div(children=[
    html.Link(href='https://fonts.googleapis.com/css?family=Oxygen&display=swap'),
    html.H1(children=df['Nome da Fazenda'][0], style={'text-align':'center', 'font-family': "'Oxygen', sans-serif", 'padding-top': '30px'}),

    # Grid Layout
    html.Div(children=[

        # Information block
        html.Div(children=[

            html.H3('Panorama geral', style={'font-family': "'Oxygen', sans-serif"}),

            # Information grid container (preenchido pela função update_value)
            html.Div(className='info-grid-container', id='info-grid-container'),

            # Atualizar informações
            html.Div(children=[
                html.Br(),
                html.H3('Atualizar informações',  style={'font-family': "'Oxygen', sans-serif"}),

                # Dropdown para seleção de atributo
                html.Span('Selecione um indicador'),
                html.Div(children=[
                    dcc.Dropdown(
                        id='atr-change',
                        options=[{'label': i, 'value': i} for i in graph_columns],
                        value='Custo total'
                    )
                ], className='dropdown-update'),
                
                html.Br(),

                # Campo para inserção do novo valor
                html.Span('Insira o novo valor do campo'),
                html.Div(children=[
                    dcc.Input(id='new-value', value=0, type='number'),
                    html.Button(id='submit-button', n_clicks=0, children='Atualizar', className='update-button'),
                ], className='input-newvalue', style={'display':'flex'})

            ], className='update-info'),
            
        ], className='information'),

        # Graph block
        html.Div(children=[
            dcc.Graph(
                id='proporcoes-pizza',
                figure={
                    'data': [
                        plot_pie(df)
                    ],
                    'layout': go.Layout(
                        autosize = False,
                        width=620,
                        height=620,
                        paper_bgcolor='#fafcff'
                    )
                }   
            )
        ], className='graph'),

        # Buttons block
        html.Div(children=[
            
            html.H3('Menu de opções',  style={'font-family': "'Oxygen', sans-serif"}),

            # Buttons grid container
            html.Div(children=[
                
                # Button 1
                html.Div(children=[
                    dcc.Link(html.Button('Nutrição', id='nutricao', className='button'), href='/nutricao')
                ], className='button1'),

                # Button 2
                html.Div(children=[
                    dcc.Link(html.Button('Mão de obra', id='mdo', className='button'), href='/mdo')

                ], className='button2'),

                # Button 3
                html.Div(children=[
                    dcc.Link(html.Button('Sanidade', id='sanidade', className='button'), href='/sanidade')
                ], className='button3'),

                # Button 4
                html.Div(children=[
                    dcc.Link(html.Button('Reposição', id='reposicao', className='button'), href='/reposicao')
                ], className='button4'),

                # Button 5
                html.Div(children=[
                    dcc.Link(html.Button('Pastejo', id='pastejo', className='button'), href='/pastejo')
                ], className='button5'),

                # Button 6
                html.Div(children=[
                    dcc.Link(html.Button('Genética', id='genetica', className='button'), href='/genetica')
                ], className='button6'),

                # Button 7
                html.Div(children=[
                    dcc.Link(html.Button('Resultados Gerais', id='resultados-gerais', className='button-large'), href='/resultados')
                ], className='button7'),

            ], className='buttons-grid-container'),
        
        ], className='buttons')

    ], className='main-grid-container')

])

# Página de detalhes da nutrição
nutricao_layout = html.Div(children=[
    html.H1(children=df['Nome da Fazenda'][0] + ' - Nutrição', style={'text-align':'center'}),

    # Grid Layout
    html.Div(children=[
        
        # Simulação
        html.Div(children=[
            html.H3('Simulação'),

            # Simulação grid
            html.Div(children=[
                
                html.Div(children=[
                    html.Div(
                        [str(round(100.0*us['Alimentação']/us['Custo total'], 2)) + '%', html.H4(id="receitaText"), html.P("Nutrição / Custo Total")],
                        className="mini-container-simulation",
                    )
                ], className='total-relation', id="nutricao-por-custo"),

                html.Div(children=[
                    html.Div(
                        [str(round(100.0*us['Alimentação']/us['Faturamento Bruto'], 2)) + '%', html.H4(id="receitaText"), html.P("Nutrição / Renda Bruta")],
                        className="mini-container-simulation",
                    )
                ], className='rendabruta-relation', id="nutricao-por-bruto"),

                html.Div(children=[
                    html.Div(
                        ['R$ ' + str(us['Resultado']), html.H4(id="receitaText"), html.P("Resultado da op.")],
                        className="mini-container-simulation-large",
                    )
                ], className='lucro', id="resultados-operacao"),

                html.Div(children=[
                    html.P('Aumento de eficiência (%)'),
                    html.Div(children=[
                        dcc.Slider(
                            id='percent-slider-eficiency',
                            min=0,
                            max=100,
                            value=0,
                            marks={i: i for i in range(100, 10)},
                            step=5
                        ), 
                    ])
                ], className='slider1', style={'padding-right':'10px', 'padding-top':'10px'}),

                html.Div(children=[
                    html.P('Redução de custo (%)'),
                    html.Div(children=[
                        dcc.Slider(
                            id='percent-slider-cost',
                            min=0,
                            max=100,
                            value=0,
                            marks={i: i for i in range(100, 10)},
                            step=5
                        ),
                    ])
                ], className='slider2', style={'padding-left':'20px', 'padding-top':'10px'}),

            ], className='simulation-grid-container'),
            
            html.Div(children=[
                dcc.Graph(
                    id='graph-bar',
                    figure = {
                        'data': [
                            go.Bar(
                                x = ['Lucro real/ha', 'Lucro ótimo/ha'],
                                y = [df['Resultado'][0]/200, 988.98],
                                name = 'Lucro'
                            )    
                        ],
                    }
                )
            ], className='graph-bar', id='graph-barr')

        ], className='simulation'),

        # Informações detalhadas
        html.Div(children=[
            html.H3('Informações detalhadas'),
            html.Div(children=[
                # Information 1
                html.Div(children=[
                    html.Div(
                        ['R$ ' + str(us['Resultado']/200), html.H4(id="totalText"), html.P("Lucro por ha")],
                        id="lucro-por-ha",
                        className="mini-container-detailed",
                    )
                ], className='mini-container1'),
                
                # Information 2
                html.Div(children=[
                    html.Div(
                        ['R$ ' + str(round(us['Resultado']/(us['Número de Machos terminação'] * us['Peso Médio dos Animais (@)']), 2)), html.H4(id="depreText"), html.P("Lucro por @")],
                        id="depre",
                        className="mini-container-detailed",
                    )
                ], className='mini-container2'),

                # Information 3
                html.Div(children=[
                    html.Div(
                        ['R$ ' + str(round(us['Alimentação']/200, 2)), html.H4(id="fatText"), html.P("Nutrição por ha")],
                        id="fat",
                        className="mini-container-detailed",
                    )
                ], className='mini-container3'),
                
                # Information 4
                html.Div(children=[
                    html.Div(
                        ['R$ ' + str(round(us['Alimentação']/(us['Número de Machos terminação'] * us['Peso Médio dos Animais (@)']), 2)), html.H4(id="receitaText"), html.P("Nutrição por @")],
                        id="receita",
                        className="mini-container-detailed",
                    )
                ], className='mini-container4'),

            ], className='detailed-info-grid', id='detailed-info-grid')

        ], className='detailed-information'),

        # Startups
        html.Div(children=[
             html.H3("Recomendações"),

             html.Div(children=[
                 
                html.Div(children=[
                    dcc.Link(html.Img(src='assets/images/ylive biotecnologia.png'))
                ], className='startup1'),

                html.Div(children=[
                    dcc.Link(html.Img(src='assets/images/beef trader.png'))
                ], className='startup2'),
                
                html.Div(children=[
                    dcc.Link(html.Img(src='assets/images/Algae-Biotecnologia-removebg-preview.png'))
                ], className='startup3'),

             ], className='startup-grid-container'),

        ], className='startups'),

    ], className='detailed-grid-container')

])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/nutricao':
        return nutricao_layout
    elif pathname == '/mdo':
        return mdo_layout
    elif pathname == '/sanidade':
        return sanidade_layout
    elif pathname == '/reposicao':
        return reposicao_layout
    elif pathname == '/pastejo':
        return pastejo_layout
    elif pathname == '/genetica':
        return genetica_layout
    elif pathname == '/resultados':
        return resultados_layout
    else:
        return home_layout

@app.callback([Output('info-grid-container', 'children'),
               Output('proporcoes-pizza', 'figure')],
              [Input('submit-button', 'n_clicks')],
              [State('atr-change', 'value'),
               State('new-value', 'value')])
def update_value(n_clicks, field, new_value):
    if n_clicks > 0:
        df[field][0] = new_value

    us = df.iloc[0]

    return [
        # Information 1
        html.Div(children=[
            html.Div(
                ['R$ ' + str(us['Custo total']), html.H4(id="totalText"), html.P("Custo total")],
                id="total",
                className="mini-container",
            )
        ], className='info1'),
        
        # Information 2
        html.Div(children=[
            html.Div(
                ['R$ ' + str(us['Depreciação']), html.H4(id="depreText"), html.P("Depreciação")],
                id="depre",
                className="mini-container",
            )
        ], className='info2'),

        # Information 3
        html.Div(children=[
            html.Div(
                ['R$ ' + str(us['Faturamento Bruto']), html.H4(id="fatText"), html.P("Faturamento")],
                id="fat",
                className="mini-container",
            )
        ], className='info3'),
        
        # Information 4
        html.Div(children=[
            html.Div(
                ['R$ ' + str(us['Receita Liquida']), html.H4(id="receitaText"), html.P("Receita Líquida")],
                id="receita",
                className="mini-container",
            )
        ], className='info4'),

        # Information 5
        html.Div(children=[
            html.Div(
                ['R$ ' + str(us['Lucro Bruto']), html.H4(id="brutoText"), html.P("Lucro Bruto")],
                id="bruto",
                className="mini-container",
            )
        ], className='info5'),

        # Information 6
        html.Div(children=[
            html.Div(
                ['R$ ' + str(us['Resultado']), html.H4(id="resultText"), html.P("Resultado da op.")],
                id="result",
                className="mini-container",
            )
        ], className='info6'),
    ], {'data': [
        plot_pie(df)
    ], 'layout': go.Layout(
                        autosize = False,
                        width=620,
                        height=620,
                        paper_bgcolor='#fafcff'
                    )}

@app.callback([Output('detailed-info-grid', 'children'), Output('nutricao-por-custo', 'children'), Output('nutricao-por-bruto', 'children'), Output('resultados-operacao', 'children'), Output('graph-bar', 'figure')],
              [Input('percent-slider-eficiency', 'value'),
               Input('percent-slider-cost', 'value')])
def simulate(eficiency, cost):
    if (eficiency != 0 or cost != 0):
        df['Alimentação'] = df['Alimentação'] - ((cost/100) * df['Alimentação'])
        df['Peso Médio dos Animais (@)'] = df['Peso Médio dos Animais (@)'] + ((eficiency/100) * df['Peso Médio dos Animais (@)'])

        df['Faturamento Bruto'] = df['Faturamento Bruto'] + ((eficiency/100) * df['Faturamento Bruto'])
        df['Resultado'] = df['Faturamento Bruto'] - df['Custo total']

    us = df.iloc[0]

    return [
        # Information 1
        html.Div(children=[
            html.Div(
                ['R$ ' + str(round(us['Resultado']/200, 2)), html.H4(id="totalText"), html.P("Lucro por ha")],
                id="lucro-por-ha",
                className="mini-container-detailed",
            )
        ], className='mini-container1'),
        
        # Information 2
        html.Div(children=[
            html.Div(
                ['R$ ' + str(round(us['Resultado']/(us['Número de Machos terminação'] * us['Peso Médio dos Animais (@)']), 2)), html.H4(id="depreText"), html.P("Lucro por @")],
                id="depre",
                className="mini-container-detailed",
            )
        ], className='mini-container2'),

        # Information 3
        html.Div(children=[
            html.Div(
                ['R$ ' + str(round(us['Alimentação']/200, 2)), html.H4(id="fatText"), html.P("Nutrição por ha")],
                id="fat",
                className="mini-container-detailed",
            )
        ], className='mini-container3'),
        
        # Information 4
        html.Div(children=[
            html.Div(
                ['R$ ' + str(round(us['Alimentação']/(us['Número de Machos terminação'] * us['Peso Médio dos Animais (@)']), 2)), html.H4(id="receitaText"), html.P("Nutrição por @")],
                id="receita",
                className="mini-container-detailed",
            )
        ], className='mini-container4')
    ], [
        html.Div(
            [str(round(100.0*us['Alimentação']/us['Custo total'], 2)) + '%', html.H4(id="receitaText"), html.P("Nutrição / Custo Total")],
            className="mini-container-simulation",
        )
    ], [
        html.Div(
            [str(round(100.0*us['Alimentação']/us['Faturamento Bruto'], 2)) + '%', html.H4(id="receitaText"), html.P("Nutrição / Renda Bruta")],
            className="mini-container-simulation",
        )
    ], [
        html.Div(
            ['R$ ' + str(round(us['Resultado'], 2)), html.H4(id="receitaText"), html.P("Resultado da op.")],
            className="mini-container-simulation-large",
        )
    ], {
        'data': [
            go.Bar(
                x = ['Lucro real/ha', 'Lucro ótimo/ha'],
                y = [df['Resultado'][0]/200, 988.98],
                name = 'Lucro'
            )
        ],
    }

if __name__ == '__main__':
    app.run_server(debug=True)