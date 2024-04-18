import streamlit as st
import pandas as pd
import pydeck as pdk
import andu
import gabriel
import elia
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
        elia.show_map()

    elif choice == "UserSpace":
        st.title(f"welcome {st.session_state.username}")
        if st.session_state.user_pw:
            elia.user_space()
        else:
            st.session_state.username = st.text_input("username")
            st.session_state.user_pw = st.text_input("password", type="password", on_change=elia.set_username)
    elif choice == "Speckle":
        gabriel.speckle()

    elif choice == "Community":
        andu.community_space()
        st.session_state.create_new_topic = False

if __name__ == "__main__":
    main()
