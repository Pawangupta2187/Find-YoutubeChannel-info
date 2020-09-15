import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import math
from youtube_stats import YTstats
import numpy as np

API_KEY=""



def _access_sorted_data(channel_id):
    # file = "carryminati.json"
    # data = None
    # with open(file, 'r') as f:
    #     data = json.load(f)

    # channel_id, stats = data.popitem()
    # channel_statistics = stats['channel_statistics']
    # video_data = stats['video_data']
    # print("access method call")
    #uncoment when we call to api direct
    API_KEY = "AIzaSyCwQ3WJ4ieNE3M_YXi3N0ShL59oyN0i0xo"
    yt = YTstats(API_KEY, channel_id)
    channel_statistics = yt.get_channel_statitics()
    video_data = yt.get_channel_video_data()

    sorted_vids = sorted(video_data.items(), key=lambda item: int(item[1]["viewCount"]), reverse=True)
    stats = []
    for video in sorted_vids:
        print(video[1]['thumbnails']['default']['url'])
        thumbnail = video[1]['thumbnails']['default']['url']
        video_id = video[0]
        title = video[1]['title']
        views = int(video[1]['viewCount'])
        likes = int(video[1]['likeCount'])
        dislikes = int(video[1]['dislikeCount'])
        comments = int(video[1]['commentCount'])
        description = video[1]['description']

        stats.append([video_id, title, views, likes, dislikes, comments,thumbnail,description])
    df = pd.DataFrame(stats, columns=['video_id', 'title', 'views', 'likes', 'dislikes', 'comments','thumbnail','description'])
    print(df.head(10))
    #video_data = yt.get_channel_video_data()
    # print(video_data.popitem()[1].get('channelTitle',channel_id))
    try:
        return df.head(10),video_data.popitem()[1].get('channelTitle',channel_id),channel_statistics
    except:
        return None,None,None



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Youtube stats'

#html start here ____---

app.layout = html.Div(children=[
    html.Div([
        html.H4('Find Youtube Channel Statistic', style={'color': 'white', 'fontSize': '5vh'}),

            html.Div(className="form text-center", children=[
                dbc.Input(id='input-1-state', type='text', placeholder="Enter Channel Id" , value=''),
                html.Button(className="btn btn-primary", id='submit-button-state', n_clicks=1, children='Submit'),
                # html.Div(id='output-state')
                # html.Div(id='output-state')
            ],style={'width':'50%', 'margin-left': '25%','margin-top':'70px'}),


      #  html.P('Example P', className='my-class', id='my-p-element')
    ], style={'background-image': 'linear-gradient(red,white)', 'margin': 5,'height':'400px','text-align':'center','border-radius':'15px','content-align':'center'})
    ,
html.Div( className="card", children=[
    html.Div(className="card-body text-center" , children=[
        html.Div(className="card-deck",children=[
            html.Div(className="card",children=[
                html.Div(className="card-body text-center",children=[
                    html.Div(className="card-text text-white",children="Channel Name",style={'text-decoration': 'underline'}),
                    html.Div(className="card-text text-white ",id="title",style={'font-weight': 'bold'})

                ])
            ],style={'background-color':'#3366cc'}),

            html.Div(className="card", children=[
                html.Div(className="card-body text-center", children=[
                    html.Div(className="card-text text-white", children="Subscriber",style={'text-decoration': 'underline'}),
                    html.Div(className="card-text text-white ",id="subscriber",style={'font-weight': 'bold'})

                ])
            ],style={'background-color':'#dc3912'}),

            html.Div(className="card", children=[
                html.Div(className="card-body text-center", children=[
                    html.Div(className="card-text text-white", children="Videos",style={'text-decoration': 'underline'}),
                    html.Div(className="card-text text-white v",id="videos",style={'font-weight': 'bold'})

                ])
            ], style={'background-color': '#ff9900'}),

            html.Div(className="card bg-primary", children=[
                html.Div(className="card-body text-center", children=[
                    html.Div(className="card-text text-white", children="Views",style={'text-decoration': 'underline'}),
                    html.Div(className="card-text text-white ",id="views",style={'font-weight': 'bold'})

                ])
            ], style={'background-color': '#dc3912'})
        ]),


    ])
]),




    html.Div(className='graph_box cD',id='graph'),




html.Div( className="card", children=[
    html.Div(className="card-body text-center" , children=[
        html.Div(className="card-deck",id="cardMain1",children=[
        ]),
    ])
],style={'background-color':'white'}),

html.Div( className="card", children=[
    html.Div(className="card-body text-center" , children=[
        html.Div(className="card-deck",id="cardMain2",children=[
        ]),
    ])
],style={'background-color':'white'}),




])




@app.callback([ Output('title', 'children'), Output('subscriber', 'children'),Output('videos', 'children'),Output('views', 'children'),Output('graph', 'children'),Output('cardMain1', 'children'),Output('cardMain2', 'children')],
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value'),
               ])
def update_output_videos(n_clicks, input1):
    print("pawan "+input1)
    # yt = YTstats(API_KEY, input1)
    # print(input1)
    # #channel_id = "UCj22tfcQrWG7EMEKS0qLeEg"
    # yt = YTstats(API_KEY, input1)
    #
    # channel_statistics = yt.get_channel_statitics()
    # video_data = yt.get_channel_video_data()
    # # channel_stats=yt.dump()
    # print("pawan fdfs"+channel_statistics)
    # channel_title=video_data.popitem()[1].get('channelTitle', channel_id)
    #return "Chanel nam is : ".format(channel_name)
    if(input1):
        top10videos, channel_name ,channel_stats = _access_sorted_data(input1)



        lis1 = []
        lis2 = []
        subscriber = None
        videos = None
        views = None
        try:
            subscriber = millify(channel_stats['subscriberCount'])
            videos = millify(channel_stats['videoCount'])
            views = millify(channel_stats['viewCount'])
        except:
            return None, None, None, None, None, None, html.Div(className='container text-center',
                                                                children="Data does not exist for this channel id")

        # for i in range(len(top10videos)):
        #     print(top10videos.iloc[i]['comments'])

        for i in range(len(top10videos)):
            if i < 5:
                lis1.append(dbc.Card(
                    [
                        dbc.CardImg(src=top10videos.iloc[i]['thumbnail'], top=True),
                        dbc.CardBody(
                            [
                                html.H4(top10videos.iloc[i]['title'], className="card-title"),
                                html.P([
                                    html.B("Views.: "),
                                    top10videos.iloc[i]['views']
                                ],
                                    className="card-text",
                                ),
                                html.P([
                                    html.B("Likes.: "),
                                    top10videos.iloc[i]['likes']
                                ],
                                    className="card-text",
                                ),
                                html.P([
                                    html.B("Dislikes.: "),
                                    top10videos.iloc[i]['dislikes']
                                ],
                                    className="card-text",
                                ),
                                html.P([
                                    html.B("Comments.: "),
                                    top10videos.iloc[i]['comments']
                                ],
                                    className="card-text",
                                ),
                                dbc.Button("Go to channel", color="primary"),
                            ]
                        ),
                    ],
                    style={"width": "18rem"},
                )
                )

            else:
                lis2.append(dbc.Card(
                    [
                        dbc.CardImg(src=top10videos.iloc[i]['thumbnail'], top=True),
                        dbc.CardBody(
                            [
                                html.H4(top10videos.iloc[i]['title'], className="card-title"),
                                html.P([
                                    html.B("Views.: "),
                                    top10videos.iloc[i]['views']
                                ],
                                    className="card-text",
                                ),
                                html.P([
                                    html.B("Likes.: "),
                                    top10videos.iloc[i]['likes']
                                ],
                                    className="card-text",
                                ),
                                html.P([
                                    html.B("Dislikes.: "),
                                    top10videos.iloc[i]['dislikes']
                                ],
                                    className="card-text",
                                ),
                                html.P([
                                    html.B("Comments.: "),
                                    top10videos.iloc[i]['comments']
                                ],
                                    className="card-text",
                                ),
                                dbc.Button("Go to channel", color="primary"),
                            ]
                        ),
                    ],
                    style={"width": "18rem"},
                )
                )


        # for i in range(len(top10videos)):
        #     lis.append( html.Div(className='card',children=[
        #
        #     html.Div(className="card-title text-white",children=top10videos.iloc[i]['title']),
        #     html.Div(className="card-body",children=[
        #         html.Img(className="card-img-top",src=top10videos.iloc[i]['thumbnail'])
        #     ])],style={'background-color': 'grey'}
        #
        #     )
        #                 )

        return channel_name,subscriber,videos,views,\
               dcc.Graph(figure={
                'data': [
                    {'x': top10videos['title'], 'y': top10videos['views'], 'type': 'bar', 'name': 'views'},

                ],
                'layout': {
                    'title': 'Top 10 videos'
                }
            }
        ), lis1, lis2
    else:
        return None,None,None,None,None,None,None





# @app.callback([Output('subscriber', 'children'),Output('videos', 'children'),Output('views', 'children')],
#               [Input('submit-button-state', 'n_clicks')],
#               [State('input-1-state', 'value'),
#                ])
# def updatechannelstats(n_clicks,input1):
#     if(input1):
#         channel_stats = _access_channel_stats(input1)
#         subscriber=millify(channel_stats['subscriberCount'])
#         videos=millify(channel_stats['videoCount'])
#         view = millify(channel_stats['viewCount'])
#         return subscriber, videos,view
#     else:
#         return 0,0,0


millnames = ['',' Thousand',' Million',' Billion',' Trillion']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


if __name__ == '__main__':
    app.run_server(debug=True)
