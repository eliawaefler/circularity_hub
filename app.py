import json
import time

import streamlit as st
from PIL import Image
import andu
import gabriel
import elia
from sqlalchemy import create_engine, text
# im terminal: streamlit run app.py
import neon
import neon_write_old_version
import sha256


def sha_pw():
    pw = str(st.session_state.user_pw)
    un = str(st.session_state.username)
    #st.subheader(f"{pw}{un}")
    return str(sha256.secure_hash(f"{pw}{un}"))


def checkpw() -> bool:
    try:
        user_from_db = neon.read_db(st.secrets['NEON_URL'],
                                    'users', condition=f"name = '{st.session_state.username}'")
    except:
        st.warning("user not found")
        return False
    #st.write(user_from_db[0][2])
    #st.write(sha_pw())
    if user_from_db[0][2] == sha_pw():
        elia.set_username()
        return True
    else:
        st.warning("incorrect Password")
        return False



def createuser() -> bool:
    try:
        uname = st.session_state.username
        existing_users = neon.read_db(st.secrets["NEON_URL"], "users")
        for user in existing_users:
            if user[1] == uname:
                st.error("username taken")
                return False
        next_id = len(existing_users) + 1
        data = {
            # 'id': int(sha256.sha_dez(f"{name}+{time.time()}")),   DAS Wäre für unique id
            'id': next_id,
            'name': st.session_state['username'],
            'pw_hash': sha_pw(),
            'email': st.session_state.email,
            'firma': st.session_state.corp,
            'geburtstag': st.session_state.birthday
        }
        with st.spinner("adding to db"):

            add_2_db_res = neon.write_to_db(st.secrets["NEON_URL"], "users", data)
            if add_2_db_res == "":
                st.success("entry added to db")
            else:
                st.error(add_2_db_res)
        return True
    except Exception as e:
        st.write(e)
        return False


def main():
    st.set_page_config(
        page_title="Circularity Hub", #:cyclone::hammer_and_pick::recycle:
        page_icon=":cyclone:",  # You can use emojis or path to an image file :repeat: oder :cyclone: :radio_button: :recycle: :hammer_and_pick:
        layout="wide",  # 'centered' or 'wide'
        initial_sidebar_state="expanded"  # 'auto', 'expanded', or 'collapsed'
    )
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ("Home", "UserSpace", "Community", "Speckle")) #"test_db", "newDBtest", "Map View",
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
        # Connection URL for SQLAlchemy
        connection_url = st.secrets["NEON_NEW"]
        engine = create_engine(connection_url)

        def add_to_circdb_(my_id, my_name, my_pet):
            query = text("INSERT INTO home (id, name, pet) VALUES (:id, :name, :pet)")
            with engine.connect() as conn:
                try:
                    conn.execute(query, {"id": my_id, "name": my_name, "pet": my_pet})
                    st.success("Added to database successfully!")
                except Exception as e:
                    st.error(f"Failed to add to database: {str(e)}")

        def add_to_circdb(my_id, my_name, my_pet):
            # Define the query for insertion
            insert_query = text("INSERT INTO home (id, name, pet) VALUES (:id, :name, :pet)")
            # Define the query for checking the entry
            check_query = text("SELECT * FROM home WHERE id = :id AND name = :name AND pet = :pet")
        
            with engine.connect() as conn:
                try:
                    # Insert the entry into the database
                    conn.execute(insert_query, {"id": my_id, "name": my_name, "pet": my_pet})
                    st.warning("Insertion step completed for table 'home', branch 'dev_branch'.")
        
                    # Check if the entry was successfully added
                    result = conn.execute(check_query, {"id": my_id, "name": my_name, "pet": my_pet}).fetchone()
                    st.warning("Verification step completed for table 'home', branch 'dev_branch'.")
        
                    if result:
                        st.success("Added to database successfully!")
                    else:
                        st.error("Entry was not added to the database.")
        
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
        new_id = st.text_input("Enter id:")
        new_name = st.text_input("Enter name:")
        new_pet = st.text_input("Enter pet:")
        if new_id:
            if new_name:
                if new_pet:
                    if st.button('Add Entry'):
                        add_to_circdb(new_id, new_name, new_pet)
        st.header('Existing Entries in Database')
        entries = fetch_entries()
        if entries:
            st.write(entries)
            for entry in entries:
                read_id, read_name, read_pet = entry
                print(f"ID: {read_id}, Name: {read_name}, Pet: {read_pet}")
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
                st.session_state.user_pw = str(hash(st.text_input("password", type="password")))
                if st.button("login"):
                    if checkpw():
                        #elia.user_space()
                        st.rerun()
                    else:
                        st.error("wrong pw / username")
            else:
                st.session_state.username = st.text_input("required: NEW username")
                st.session_state.user_pw = str(hash(st.text_input("required: NEW password", type="password")))
                st.session_state.email = st.text_input("required: EMAIL")
                st.session_state.corp = st.text_input("required: company")
                st.session_state.birthday = st.text_input("required: Birthday YYYY-MM-DD")
                if st.button("Create!"):
                    if createuser():
                        st.success("login")
                        st.session_state.user_logged_in = True
                        st.rerun()
                    else:
                        st.warning("didnt work")
    elif choice == "Speckle":
        gabriel.speckle()
    elif choice == "Community":
        andu.community_space()
        st.session_state.create_new_topic = False
if __name__ == "__main__":
    main()
