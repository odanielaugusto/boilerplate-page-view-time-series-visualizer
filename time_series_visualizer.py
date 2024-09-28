import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1 - Importando os dados e definindo o índice
df = pd.read_csv("boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# 2 - Limpando os dados, removendo os 2.5% superiores e inferiores
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # 3 - Desenhando o gráfico de linhas
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['value'], color='r', linewidth=1)

    # Definindo título e rótulos
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Salvando e retornando a figura
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # 4 - Modificando os dados para gráfico de barras agrupado por ano e mês
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Criando DataFrame com a média das visualizações diárias por mês
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # 5 - Desenhando o gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(10, 6), legend=True).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months", labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    # Salvando e retornando a figura
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # 6 - Preparando os dados para os box plots (Trends por ano e Sazonalidade por mês)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')  # Ordenar meses corretamente

    # 7 - Desenhando dois box plots lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # Box plot por ano (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Box plot por mês (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Salvando e retornando a figura
    fig.savefig('box_plot.png')
    return fig
    