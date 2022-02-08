## https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4#:~:text=As%20mentioned%20already%20streamlit%20does,app%20using%20a%20radio%20button.

import yfinance as yf
import streamlit as st
import psycopg2, os
import pandas as pd
import plotly.express as px
from PIL import Image

def app():
            icon = Image.open("news_icon.png")

            # read database connection url from the enivron variable we just set.
            DATABASE_URL = os.environ.get('DATABASE_URL')

            con = None

            hide_streamlit_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        </style>
                        """
            st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

            st.write("""
            # ABC News 
            Public consciousness is shaped by the News. The purpose of this project is to shine a light on how Australia's public broadcaster influences the public square in the digital age.
            """)

            try:
                # create a new database connection by calling the connect() function
                con = psycopg2.connect(DATABASE_URL)

                #  create a new cursor
                cur = con.cursor()
                read_table = """SELECT date, articles::int as articles, polarity,subjectivity as subjectivity from mymatview3 where articles > 5000  order by 1"""  
                cur.execute(read_table)
                df = pd.read_sql_query(read_table, con)
                px_data = pd.read_sql_query(read_table, con)
                df = df.set_index('date')
                data = df
                total_articles = int(df['articles'].sum())

                 # close the communication with the HerokuPostgres
                cur.close()
            except Exception as error:
                print('Could not connect to the Database.')
                print('Cause: {}'.format(error))

            finally:
                # close the communication with the database server by calling the close()
                if con is not None:
                    con.close()
                    print('Database connection closed.')

            # st.metric(label="Articles", value=int(Total), delta=None)

            # Sort data before converting to a string for readability

            px_data = px_data.sort_values(by=['articles'], ascending=True)

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
            st.plotly_chart(fig1, use_container_width=True)

            fig2 = px.line(px_data, x='date', y=px_data.subjectivity.round(4),text=px_data.subjectivity.round(4),title="Subjectivity by Year" )
            st.plotly_chart(fig2, use_container_width=True)
