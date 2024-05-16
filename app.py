import streamlit as st
from PIL import Image
import andu
import gabriel
import elia
import pandas as pd
from sqlalchemy import create_engine
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

        # Load secrets
        db_url = st.secrets["connections"]["neon"]["url"]

        # Initialize database connection using SQLAlchemy
        engine = create_engine(db_url)

        def add_to_db(name, pet):
            sql_command = "INSERT INTO home (name, pet) VALUES (:name, :pet)"
            parameters = {'name': name, 'pet': pet}
            with engine.connect() as conn:
                try:
                    # Begin a transaction
                    with conn.begin():
                        # Execute the SQL command with parameters
                        conn.execute(sql_command, parameters)
                    st.success("Added to database successfully!")
                except Exception as e:
                    st.error(f"Failed to add to database: {str(e)}")
                    st.error("Check that the types and values are correct for the database schema.")

        # User interface for adding new entries
        st.header("Add New Entry")
        name = st.text_input("Name:")
        pet = st.text_input("Pet:")

        if st.button("Add to Database"):
            add_to_db(name, pet)
            st.success("Added to database successfully!")

        # Display existing entries
        st.header("Existing Entries")
        query = "SELECT * FROM home;"
        df = pd.read_sql(query, engine)
        st.write(df)
            
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
