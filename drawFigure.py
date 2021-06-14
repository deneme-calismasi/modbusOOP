import plotly.express as px
import pandas as pd


class DrawFigure():
    @staticmethod
    def draw_figure():
        df = pd.read_csv('C:/Users/halilerhan.orun/IdeaProjects/modbusOOP/sensor_no.csv')
        fig = px.line(df, x='Time', y='Temp', title='Temperature °C - Time', color='Sensor No')

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        return fig.show()

    @staticmethod
    def close_figure():
        df = pd.read_csv('C:/Users/halilerhan.orun/IdeaProjects/modbusOOP/sensor_no.csv')
        fig = px.line(df, x='Time', y='Temp', title='Temperature °C - Time', color='Sensor No')

        return fig.close()
