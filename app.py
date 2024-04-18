import streamlit as st
import pandas as pd
import pydeck as pdk
from andu import *
from gabriel import *
from elia import *
# im terminal: streamlit run app.py


def main():
    st.sidebar.title("Navigation")

    choice = st.sidebar.radio("Go to", ("Home", "Map View", "UserSpace", "Community", "Speckle"))
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "user_pw" not in st.session_state:
        st.session_state.user_pw = False

    if choice == "Home":
        st.title("Circularity Hub")
        st.write("Die Plattform für zirkuläres Bauen.")
        st.image("")

    elif choice == "Map View":
        st.title("Map View")
        st.write("Die besten Materiallager für dein Projekt.")
        show_map()

    elif choice == "UserSpace":
        st.title(f"welcome {st.session_state.username}")
        if st.session_state.userpw:
            user_space()
        else:
            st.session_state.username = st.text_input("username")
            st.session_state.user_pw = st.text_input("password", type="password", on_change=set_username)
    elif choice == "Speckle":
        speckle()

    elif choice == "Community":
        community_space()


if __name__ == "__main__":
    main()
