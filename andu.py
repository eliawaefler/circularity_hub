import streamlit as st
import pandas as pd
import pydeck as pdk
# im terminal: streamlit run app.py


def community_space():

    st.title("Community Space")
    st.write("Share your Ideas with your Community")

    # CSS für die individuellen Beitragsboxen
    st.markdown("""
        <style>
        .box {
            background-color: #f0f0f0;  /* Hellgrauer Hintergrund */
            padding: 20px;
            border-radius: 10px;
            height: 400px;             /* Feste Höhe */
            display: flex;
            flex-direction: column;
            justify-content: space-between;  /* Inhalt am Anfang und Tags am Ende */
            margin-bottom: 20px;      /* Abstand zwischen den Boxen */
        }
        </style>
        """, unsafe_allow_html=True)

    # Erstellen von Spalten für die Einträge
    col1, col2, col3 = st.columns(3)

    # Eintrag in der ersten Spalte
    with col1:
        st.markdown("""
            <div class='box'>
                <h4>Community Garden</h4>
                <p>A community garden with spaces for everyone to plant.</p>
                <p style='opacity: 0.6;'>#gardening #community #green</p>
            </div>
            """, unsafe_allow_html=True)

    # Eintrag in der zweiten Spalte
    with col2:
        st.markdown("""
            <div class='box'>
                <h4>Sports Day</h4>
                <p>Weekly community sports day to promote health and wellbeing.</p>
                <p style='opacity: 0.6;'>#health #sports #weekly</p>
            </div>
            """, unsafe_allow_html=True)

    # Eintrag in der dritten Spalte
    with col3:
        st.markdown("""
            <div class='box'>
                <h4>Book Swap</h4>
                <p>A monthly book swap event in our local library.</p>
                <p style='opacity: 0.6;'>#books #library #swap</p>
            </div>
            """, unsafe_allow_html=True)

    # Button zum Hinzufügen neuer Beiträge
    if st.button('Add New Post'):
        create_new_topic()
        new_topic()


def new_topic():
    st.header("Create a new Topic")
    title = st.text_input("Type title, or paste a link here")
    category = st.selectbox("Select a category", ["Category 1", "Category 2", "Category 3"])

    # Tags functionality
    if 'tags' not in st.session_state:
        st.session_state.tags = []  # Initialize tags if not present
    new_tag = st.text_input("Add a tag", key="tag_input")
    if new_tag:
        st.session_state.tags.append(new_tag)  # Add new tag
        st.write(st.session_state.tags)  # Display tags
        st.session_state.tag_input = ''  # Reset input field

    content = st.text_area("Content", height=200)
    if st.button("Create Topic"):
        if title and category and content:
            st.success(f"Topic '{title}' created in '{category}' with tags {st.session_state.tags}.")
            # You might want to reset fields or handle the new topic (e.g., store it somewhere)
        else:
            st.error("Please fill out all fields to create a topic.")

def set_create_new_topic():
    st.session_state.create_new_topic = True
