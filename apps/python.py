import yfinance as yf
import streamlit as st
import psycopg2, os
import pandas as pd
import plotly.express as px
from PIL import Image

def app():

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
        fig = px.bar(px_data, x='date', y='articles',text='articles_rounded',title="Count of Articles by Year")
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True)

        # Sort by Date for Polarity and Subjectivity charts
        px_data = px_data.sort_values(by=['date'], ascending=True)
        fig1 = px.line(px_data, x='date', y=px_data.polarity.round(4),text=px_data.polarity.round(4),title="Polarity by Year" )
        st.plotly_chart(fig1, use_container_width=True
