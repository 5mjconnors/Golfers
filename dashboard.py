import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

PGA = pd.read_csv('top_80_players.csv', index_col = 0)

ages_col = PGA.pop('Age')
PGA.insert(2, 'Age', ages_col)

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
def generate_table(dataframe, max_rows=80):
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

app = dash.Dash(__name__, external_stylesheets=stylesheet)

fig = px.scatter(PGA, x = 'Avg_Drive_Dis', y = 'Points', opacity = 0.65, trendline = 'ols', trendline_color_override = 'darkblue')

app.layout = html.Div([
    html.H2("How do PGA Players' Strengths impact their FedExCup Points?", style = {'color': 'darkblue'}),
    html.P("Have you ever wondered what makes the best golfers in the world so good? This dashboard will help you get an idea of the variables that mean the most when it comes to competing on the PGA Tour."),
    html.Hr(),
    html.Div([
    html.H3("Introduction to the PGA and FedExCup:", style = {'color': 'darkblue'}),
    html.P("In the PGA, the best players in the world compete in weekend long tournaments throughout the year. They play at different golf courses every weekend and each golf course has its own challenges. Each course has a par score, which is the number of strokes that the course sets as a standard. A golfer's objective is to score the lowest score that he or she can on the course. To score well, a player must be playing all aspects of the game well (driving the ball off the tee, hitting the ball onto the green, chipping around the green, and putting the ball. If you are not familiar with how the game of golf works the following link will explain to you the basics:"),
    html.A('Basic introduction to the game of golf', href = 'https://simple.wikipedia.org/wiki/Golf'),
    html.Br(),
    html.Br(),
    html.P("The FedExCup is an overarching contest that is won by the best overall tournament player for any given season. According to the PGA, 'the FedExCup is a season-long points competition offering unprecedented bonus money and culminating with the FedExCup Playoffs in August.' Players obtain more FedExCup points the higher they place in any given tournament. Therefore, a player's FedExCup points at any point during a season is a great measure of how well he or she is doing overall in the current season's tournament play. For this dashboard we are focusing on men's PGA."),
    html.A('Click here for more detailed information on the FedExCup', href = 'https://www.pgatour.com/fedexcup/fedexcup-overview.html#:~:text=earning%20%2415%20million-,OVERVIEW,the%20FedExCup%20Playoffs%20in%20August.', target = '_blank'),
    ], style = {'width' : '48%', 'display': 'inline-block', 'vertical-align' : 'top'}),
    html.Div([], style = {'width' : '2%', 'display': 'inline-block', 'vertical-align' : 'top'}),
    html.Div([
    html.H3('Key Statistics in Golf:', style = {'color': 'darkblue'}),
    html.P("Before describing the key statistics in golf, we first have to define some basic terms. First of all, all distances in golf are measured in yards. Any number that is distance oriented (such as average drive distance) is measured in yards. Par is a term that describes the number of strokes it should take you to get the ball in the hole from the first to last shot. Hitting a green in regulation means that you are on the green after hitting ball two time less than par. For example, on a par 4 hitting a green in regulation means that it took you 2 strokes to get the ball on the green. Another term is sand save, which is when a player hits his or her ball out of a greenside bunker and hits the next shot into the hole. Now that we have defined these terms, we can present the statistics used in this dashboard:"),
    html.Ul([
        html.Ul([
            html.Li(["Average Driving Distance: the average distance of all shots hit with a player's driver"]),
            html.Li(["Average Putts Per Hole: the average number of putts that a player has on each hole"]),
            html.Li(["Driving Accuracy Percentage: the number of fairways hit off the tee / total tee shots"]),
            html.Li(["Greens in Regulation Percentage: greens hit in regulatiion / total holes played"]),
            html.Li(["Sand Save Percentage: number of sand saves / total number of sand shots"]),
        ])]),
    
    html.P("This dashboard allows you to choose which variable listed above you would like to see displayed on a regression model in relation with players' FedExCup points. This will allow you to see how tour players' strengths affect how well they do in tournament play (the higher number of FedExCup points a player has, the better he is in tournament play). The players' countries of origins and ages are also included in the data to interact with. You can choose countries of origin that you would like to see as well as an age range."),
        html.Ul([
            html.Ul([
                html.Li(["Important Note: some players do not have a specified age, so their age is replaced with the average age of PGA players (35)"], style = {'color': 'red'})])]),
    html.P("These statistics were scraped off the ESPN website:"),
    html.A('Click here to go to ESPN Site', href ='https://www.espn.com/golf/statistics/_/sort/cupPoints', target = '_blank'), # target means open link in new tab
    ], style = {'width' : '48%', 'display': 'inline-block'}),
    html.Hr(),
    html.Div([
    html.H3('FedExCup Points Based on Key Player Stats', style = {'color': 'darkblue'}),
    html.H6('Choose the variable you would like to see in relation to FedExCup Points:'),
    dcc.Dropdown(
        options=[
            {'label': 'Earnings', 'value': 'Earnings'},
            {'label': 'Average Drive Distance', 'value': 'Avg_Drive_Dis'},
            {'label': 'Average Putts Per Hole', 'value': 'Avg_Putts_Hole'},
            {'label': 'Driving Accuracy Percentage', 'value': 'Drive_Accuracy_Pctg'},
            {'label': 'Greens in Regulation Percentage', 'value': 'Greens_Reg_Pctg'},
            {'label': 'Sand Save Percentage', 'value': 'Sand_Save_Pct'}
        ],    
        value='Avg_Drive_Dis',
        id = 'variable_dropdown',
        style = {'width' : '325px',
                 'textAlign' : 'center'}),
    html.H6('Choose the countries of the players you would like to see displayed: (Refresh to reselect all)'), 
    dcc.Dropdown(
        options=[
            {'label': 'Argentina', 'value': 'Argentina'},
            {'label': 'Australia', 'value': 'Australia'},
            {'label': 'Canada', 'value': 'Canada'},
            {'label': 'Chile', 'value': 'Chile'},
            {'label': 'Chinese Taipei', 'value': 'Chinese Taipei'},
            {'label': 'Colombia', 'value': 'Colombia'},
            {'label': 'England', 'value': 'England'},
            {'label': 'Fiji', 'value': 'Fiji'},
            {'label': 'France', 'value': 'France'},
            {'label': 'Germany', 'value': 'Germany'},
            {'label': 'India', 'value': 'India'},
            {'label': 'Ireland', 'value': 'Ireland'},
            {'label': 'Italy', 'value': 'Italy'},
            {'label': 'Japan', 'value': 'Japan'},
            {'label': 'Mexico', 'value': 'Mexico'},
            {'label': 'New Zealand', 'value': 'New Zealand'},
            {'label': 'Northern Ireland', 'value': 'Northern Ireland'},
            {'label': 'Norway', 'value': 'Norway'},
            {'label': 'Scotland', 'value': 'Scotland'},
            {'label': 'South Africa', 'value': 'South Africa'},
            {'label': 'South Korea', 'value': 'South Korea'},
            {'label': 'Spain', 'value': 'Spain'},
            {'label': 'Sweden', 'value': 'Sweden'},
            {'label': 'United States', 'value': 'United States'},
            {'label': 'Venezuela', 'value': 'Venezuela'},
            {'label': 'Wales', 'value': 'Wales'},
            {'label': 'Zimbabwe', 'value': 'Zimbabwe'}
        ],
        value=['Australia', 'Canada', 'Chile', 'Chinese Taipei', 'Colombia', 'England', 'Ireland', 'Japan', 'Mexico', 'Northern Ireland', 'Norway', 'Scotland', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'United States', 'Argentina', 'Canada', 'Fiji', 'France', 'Germany', 'India', 'Italy', 'New Zealand', 'Venezuela', 'Wales', 'Zimbabwe'],
        multi = True,
        id = 'country_checklist',
        style = {'textAlign' : 'center'}),  
        html.H6('Choose a minimum player age to be included:'),
        dcc.Dropdown(
        options=[
            {'label': 15, 'value': 15},
            {'label': 16, 'value': 16},
            {'label': 17, 'value': 17},
            {'label': 18, 'value': 18},
            {'label': 19, 'value': 19},
            {'label': 20, 'value': 20},
            {'label': 21, 'value': 21},
            {'label': 22, 'value': 22},
            {'label': 23, 'value': 23},
            {'label': 24, 'value': 24},
            {'label': 25, 'value': 25},
            {'label': 26, 'value': 26},
            {'label': 27, 'value': 27},
            {'label': 28, 'value': 28},
            {'label': 29, 'value': 29},
            {'label': 30, 'value': 30},
            {'label': 31, 'value': 31},
            {'label': 32, 'value': 32},
            {'label': 33, 'value': 33},
            {'label': 34, 'value': 34},
            {'label': 35, 'value': 35},
            {'label': 36, 'value': 36},
            {'label': 37, 'value': 37},
            {'label': 38, 'value': 38},
            {'label': 39, 'value': 39},
            {'label': 40, 'value': 40},
            {'label': 41, 'value': 41},
            {'label': 42, 'value': 42},
            {'label': 43, 'value': 43},
            {'label': 44, 'value': 44},
            {'label': 45, 'value': 45},
            {'label': 46, 'value': 46},
            {'label': 47, 'value': 47},
            {'label': 48, 'value': 48},
            {'label': 49, 'value': 49},
            {'label': 50, 'value': 50},
            {'label': 51, 'value': 51},
            {'label': 52, 'value': 52},
            {'label': 53, 'value': 53},
            {'label': 54, 'value': 54},
            {'label': 55, 'value': 55},
            {'label': 56, 'value': 56},
            {'label': 57, 'value': 57},
            {'label': 58, 'value': 58},
            {'label': 59, 'value': 59},
            {'label': 60, 'value': 60}
        ],
        value= 15,
        id = 'min_age_checklist',
        style = {'width' : '75px'}),  
        html.H6('Choose a maximum player age to be included:'),
        dcc.Dropdown(
        options=[
            {'label': 15, 'value': 15},
            {'label': 16, 'value': 16},
            {'label': 17, 'value': 17},
            {'label': 18, 'value': 18},
            {'label': 19, 'value': 19},
            {'label': 20, 'value': 20},
            {'label': 21, 'value': 21},
            {'label': 22, 'value': 22},
            {'label': 23, 'value': 23},
            {'label': 24, 'value': 24},
            {'label': 25, 'value': 25},
            {'label': 26, 'value': 26},
            {'label': 27, 'value': 27},
            {'label': 28, 'value': 28},
            {'label': 29, 'value': 29},
            {'label': 30, 'value': 30},
            {'label': 31, 'value': 31},
            {'label': 32, 'value': 32},
            {'label': 33, 'value': 33},
            {'label': 34, 'value': 34},
            {'label': 35, 'value': 35},
            {'label': 36, 'value': 36},
            {'label': 37, 'value': 37},
            {'label': 38, 'value': 38},
            {'label': 39, 'value': 39},
            {'label': 40, 'value': 40},
            {'label': 41, 'value': 41},
            {'label': 42, 'value': 42},
            {'label': 43, 'value': 43},
            {'label': 44, 'value': 44},
            {'label': 45, 'value': 45},
            {'label': 46, 'value': 46},
            {'label': 47, 'value': 47},
            {'label': 48, 'value': 48},
            {'label': 49, 'value': 49},
            {'label': 50, 'value': 50},
            {'label': 51, 'value': 51},
            {'label': 52, 'value': 52},
            {'label': 53, 'value': 53},
            {'label': 54, 'value': 54},
            {'label': 55, 'value': 55},
            {'label': 56, 'value': 56},
            {'label': 57, 'value': 57},
            {'label': 58, 'value': 58},
            {'label': 59, 'value': 59},
            {'label': 60, 'value': 60}
        ],
        value= 60,
        id = 'max_age_checklist',
        style = {'width' : '75px'}),
            ], style = {'width' : '48%', 'display': 'inline-block', 'vertical-align' : 'top'}),
    html.Div([], style = {'width' : '2%', 'display': 'inline-block'}),
    html.Div([
    dcc.Graph(figure=fig, style = {'height' : '550px'}, id = 'pga_plot'), # dcc is used to put a graph on a dashboard (dash core components)
        ], style = {'width' : '48%', 'textAlign' : 'right', 'display': 'inline-block', 'vertical-align' : 'top'}),
    html.Hr(),
    html.H3("Table of Players in Selected Age Range and Countries - Sorted By FedExCup Points", style = {'color': 'darkblue'}),
    html.Div(id = 'table_div'), # this uses the formula defined above!!
    ]) #this changes aspects of the dashboard

@app.callback(
    Output(component_id="table_div", component_property="children"), #children that displays in the divider
    [Input(component_id="country_checklist", component_property="value")],
    [Input(component_id="min_age_checklist", component_property="value")],
    [Input(component_id="max_age_checklist", component_property="value")])

def update_table(countries, minage, maxage):
    PGA2 = PGA[PGA.Country.isin(countries)].sort_values('Points', ascending = False)
    PGA2 = PGA2[PGA.Age >= minage]
    PGA2 = PGA2[PGA.Age <= maxage]
    return generate_table(PGA2)

@app.callback(
    Output(component_id="pga_plot", component_property="figure"), #you want to update the figure
    [Input(component_id="variable_dropdown", component_property="value")],
    [Input(component_id="country_checklist", component_property="value")],
    [Input(component_id="min_age_checklist", component_property="value")],
    [Input(component_id="max_age_checklist", component_property="value")])

def var_plot(variable, countries, minage, maxage):
    PGA2 = PGA[PGA.Country.isin(countries)].sort_values('Country')
    PGA2 = PGA2[PGA.Age >= minage]
    PGA2 = PGA2[PGA.Age <= maxage]
    fig = px.scatter(PGA2, x = variable, y = 'Points', opacity = 0.65, trendline = 'ols', trendline_color_override = 'red', title = str(len(PGA2)) + ' Players in Selected Criteria')
    fig.update_layout(title_x = 0.5)  
    return fig

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)

