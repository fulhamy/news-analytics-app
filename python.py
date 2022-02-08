# main app to run application
import streamlit as st
from multiapp import MultiApp
from apps import python # import your app modules here


st.set_page_config(layout="wide",page_title='Paper Tale',page_icon=icon)

app = MultiApp()

# Add all your application here
app.add_app("Home", python.app)

# The main app
app.run()
