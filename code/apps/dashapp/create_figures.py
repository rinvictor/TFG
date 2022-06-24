import plotly.express as px


def create_temperature_fig(dataframe):
    fig = px.line(dataframe, x="date", y="value", color="sensorID", symbol="location", markers=True)
    fig.update_layout(xaxis_title="Date", yaxis_title="Temperature (ºC)")
    return fig


def create_humidity_fig(dataframe):
    fig = px.line(dataframe, x="date", y="value", color="sensorID", symbol="location", markers=True)
    fig.update_layout(xaxis_title="Date", yaxis_title="Humidity")
    return fig


def create_temperature_fig_telegram(dataframe, title):
    fig = px.line(dataframe, x="date", y="value", color="sensorID", title=title)
    fig.update_layout(xaxis_title="Date", yaxis_title="Temperature (ºC)")
    return fig


def create_humidity_fig_telegram(dataframe, title):
    fig = px.line(dataframe, x="date", y="value", color="sensorID", title=title)
    fig.update_layout(xaxis_title="Date", yaxis_title="Humidity")
    return fig


def create_irrigation_data_fig(dataframe):
    fig = px.bar(dataframe, x="date", y="value")
    fig.update_layout(xaxis_title="Date", yaxis_title="Liters used")
    return fig


def create_irrigation_data_fig_telegram(dataframe, title):
    fig = px.bar(dataframe, x="date", y="value")
    fig.update_layout(xaxis_title="Date", yaxis_title="Liters used", title=title)
    return fig
