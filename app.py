import streamlit as st
from PIL import Image
import andu
import gabriel
import elia
from sqlalchemy import create_engine, text
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

        # Load the database settings from Streamlit's secrets
        PGHOST = st.secrets["PGHOST"]
        PGDATABASE = st.secrets["PGDATABASE"]
        PGUSER = st.secrets["PGUSER"]
        PGPASSWORD = st.secrets["PGPASSWORD"]
        PGPORT = st.secrets.get("PGPORT", "5432")  # Default PostgreSQL port

        # Connection URL for SQLAlchemy
        connection_url = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}?sslmode=require'
        engine = create_engine(connection_url)

        def add_to_db(name, pet):
            query = text("INSERT INTO home (name, pet) VALUES (:name, :pet)")
            with engine.connect() as conn:
                try:
                    conn.execute(query, {"name": name, "pet": pet})
                    st.success("Added to database successfully!")
                except Exception as e:
                    st.error(f"Failed to add to database: {str(e)}")

        def fetch_entries():
            query = text("SELECT * FROM home;")
            try:
                with engine.connect() as conn:
                    result = conn.execute(query)
                    return result.fetchall()
            except Exception as e:
                st.error(f"Failed to fetch data: {str(e)}")
                return []

        st.title('Neon Database Interaction')

        st.header('Add New Entry to Database')
        name = st.text_input("Enter name:")
        pet = st.text_input("Enter pet:")
        if st.button('Add Entry'):
            add_to_db(name, pet)

        st.header('Existing Entries in Database')
        entries = fetch_entries()
        if entries:
            for id, name, pet in entries:
                st.write(f"ID: {id}, Name: {name}, Pet: {pet}")
        else:
            st.write("No entries found.")


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
