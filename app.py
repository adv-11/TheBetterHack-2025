import streamlit as st

app = st.Page(
    page = "views/migration_strategy_page.py",
    title = "App",
    default = True
)

code = st.Page(
    page="views/migrated_code.py",
    title="Code"
)

st.set_page_config(layout="wide")

#Navigation bar
pg = st.navigation(pages=[app, code])

st.sidebar.text("Navigation")

pg.run()