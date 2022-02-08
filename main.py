# main app to run application
import streamlit as st
from multiapp import MultiApp
from apps import python # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Home", python.app)

# The main app
app.run()
