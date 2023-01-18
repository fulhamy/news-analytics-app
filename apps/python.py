import yfinance as yf
import streamlit as st
import psycopg2, os
import pandas as pd
import plotly.express as px
from PIL import Image
from webpixels import css, js
from webpixels.satoshi import satoshi

def load_data():
    """
    Connects to the database and loads the data.
    """
    # read database connection url from the environment variable
    DATABASE_URL = os.environ.get('DATABASE_URL')

    # create a new database connection
    con = psycopg2.connect(DATABASE_URL)

    # create a new cursor
    cur = con.cursor()
    read_table = """SELECT date, articles::int as articles, polarity, subjectivity as subjectivity
                    FROM mymatview3
                    WHERE articles > 10000
                    ORDER BY 1"""
    cur.execute(read_table)

    # read data from the database
    df = pd.read_sql_query(read_table, con)
    px_data = df.copy()

    # close the cursor
    cur.close()

    # close the database connection
    con.close()

    return df, px_data

def app():
    # add webpixels satoshi css
    css.add_stylesheet("https://cdn.jsdelivr.net/npm/@webpixels/satoshi@1.0.0/dist/webpixels-satoshi.min.css")
    # add webpixels satoshi js
    js.add_script("https://cdn.jsdelivr.net/npm/@webpixels/satoshi@1.0.0/dist/webpixels-satoshi.min.js")
    satoshi()
    
    st.set_page_config(page_title="ABC News Analysis", page_icon=Image.open("news_icon.png"), layout="wide")
    st.write("""
    # ABC News Analysis
    Public consciousness is shaped by the News. The purpose of this project is to shine a light on how Australia's public broadcaster influences the public square in the digital age.
    """)

    # load data from the database
    df, px_data = load_data()

    # set index as date
    df = df.set_index('date')
    data = df
    total_articles = int(df['articles'].sum())

    # Function to round to abbreviate a thousand with 'K'
    def convert_to_thousands(values):
        return [str(num/1000)+'K' for num in values]

    # Abbreviate article count with thousands
    px_data['articles_rounded'] = convert_to_thousands(px_data.articles.astype(int))

    col1, col2 = st.columns(2) 

    st.write("""
    ## Mass produced content, increasingly Subjective and Polarised
    """)
