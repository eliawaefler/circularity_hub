import streamlit as st
from PIL import Image
import andu
import gabriel
import elia
# im terminal: streamlit run app.py


def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ("Home", "Map View", "UserSpace", "Community", "Speckle", "test_db"))
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "user_pw" not in st.session_state:
        st.session_state.user_pw = False
    if "user_space" not in st.session_state:
        st.session_state.user_space = "menu"
    if choice == "Home":
        st.title("Circularity Hub")
        st.write("Die Plattform für zirkuläres Bauen.")
        st.image(Image.open("images/circ.webp"), caption="circular building industry")
    
    elif choice == "test_db":   
        # Initialize connection.
        conn = st.connection("neon", type="sql")
        
        # Perform query.
        df = conn.query('SELECT * FROM home;', ttl="10m")
        
        # Print results.
        for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")
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
