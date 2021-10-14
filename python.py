import yfinance as yf
import streamlit as st
import psycopg2, os
import pandas as pd

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
    read_table = """SELECT left(date_Trunc('month', "published_at"::date),10) date, count(distinct "UID") articles from news_log where length("published_at") > 21 group by 1 having count("UID") > 100 order by 1;"""
    cur.execute(read_table)
    dat = pd.read_sql_query(read_table, con)
    cur.fetchall()
    print(cur.fetchall())
    print(dat)
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
        

st.write("""
## Articles by Month
""")
st.line_chart(dat)
st.write(dat.head())


