import streamlit as st
from PIL import Image
import andu
import gabriel
import elia
from sqlalchemy import create_engine, text
# im terminal: streamlit run app.py
import neon_write


def checkpw() -> None:
    try:
        user_from_db = neon_write.read_db("user_table", f"name='{st.session_state.userpw}'")
    except:
        st.warning("user not found")
        return
    if user_from_db.pw_hash == st.session_state.user_pw:
        elia.set_username()
    else:
        st.warning("incorrect Password")
        return


def createuser() -> None:
    try:
        uname = st.session_state.username
        # user_id = str(hash(uname))
        neon_write.write_to_db("user_table", [(str(hash(uname)),
                                               str(st.session_state.birthday),
                                               str(uname),
                                               str(st.session_state.corp),
                                               str(st.session_state.email),
                                               str(hash(st.session_state.user_pw)))])
        return True
    except Exception as e:
        st.write(e)

        return False

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ("Home", "Map View", "UserSpace", "Community", "Speckle", "test_db"))
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "user_pw" not in st.session_state:
        st.session_state.user_pw = False
    if "user_space" not in st.session_state:
        st.session_state.user_space = "menu"
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
    if choice == "Home":
        st.title("Circularity Hub")
        st.write("Die Plattform für zirkuläres Bauen.")
        st.image(Image.open("images/circ.webp"), caption="circular building industry")
    
    elif choice == "test_db":
        id = 50
        # Connection URL for SQLAlchemy
        connection_url = st.secrets["NEON_NEW"]
        engine = create_engine(connection_url)

        def add_to_circdb(name, pet):
            id += 1
            query = text("INSERT INTO home (id, name, pet) VALUES (:id :name, :pet)")
            with engine.connect() as conn:
                try:
                    conn.execute(query, {"id": id, "name": name, "pet": pet})
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
        if name:
            if pet:
                if st.button('Add Entry'):
                    add_to_circdb(name, pet)

        st.header('Existing Entries in Database')
        entries = fetch_entries()
        if entries:
            st.write(entries)
            for entry in entries:
                id, name, pet = entry
                print(f"ID: {id}, Name: {name}, Pet: {pet}")

        else:
            st.write("No entries found.")


    elif choice == "Map View":
        elia.show_map()

    elif choice == "UserSpace":
        st.title(f"welcome {st.session_state.username}")
        if st.session_state.user_logged_in:
            elia.user_space()
        else:
            if st.toggle("login/signup"):
                st.session_state.username = st.text_input("username")
                st.session_state.user_pw = st.text_input("password", type="password", on_change=checkpw)
            else:
                st.session_state.username = st.text_input("NEW username")
                st.session_state.user_pw = str(hash(st.text_input("NEW password", type="password")))
                st.session_state.email = st.text_input("EMAIL")
                st.session_state.corp = st.text_input("company")
                st.session_state.birthday = st.text_input("Birthday")
                if st.button("Create!"):
                    if createuser():
                        st.success("login")
                    else:
                        st.warning("didnt work")

    elif choice == "Speckle":
        gabriel.speckle()

    elif choice == "Community":
        andu.community_space()
        st.session_state.create_new_topic = False


if __name__ == "__main__":
    main()
