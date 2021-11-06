import yfinance as yf
import streamlit as st
import psycopg2, os
import pandas as pd
import plotly.figure_factory as ff

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
The public consciousness is shaped by the News. The purpose of this project is to shine a light on how Australia's public broadcaster has directed the public square in the digital age.
""")

try:
    # create a new database connection by calling the connect() function
    con = psycopg2.connect(DATABASE_URL)

    #  create a new cursor
    cur = con.cursor()
    read_table = """SELECT date_trunc('year', date) as date, sum(articles) as articles from mymatview2 group by 1 order by 1"""
    cur.execute(read_table)
    df = pd.read_sql_query(read_table, con)
    df = df.set_index('date')
    data = df
    total_articles = int(df['articles'].sum())
    cur.fetchall()
    print(cur.fetchall())
    print(data)
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

st.write("""
## Articles by Year
""")
st.bar_chart(data,width=1)

st.plotly_chart(data, use_container_width=True)



