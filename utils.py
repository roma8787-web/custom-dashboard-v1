import plotly.express as px

def genera_commento_ai(df, colonna):
    media = df[colonna].mean()
    massimo = df[colonna].max()
    minimo = df[colonna].min()
    return f"La media di {colonna} è {media:.2f}, il massimo è {massimo:.2f}, il minimo è {minimo:.2f}."

def crea_grafico(df, colonna):
    fig = px.histogram(df, x=colonna, title=f"Distribuzione di {colonna}")
    return fig