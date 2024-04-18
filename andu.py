import streamlit as st
import pandas as pd
import pydeck as pdk
# im terminal: streamlit run app.py


def community_space():

    st.title("Community Space")
    st.write("Share your Ideas with your Community")

    # Erstellen von Spalten für die Einträge
    col1, col2, col3 = st.columns(3)

    # Eintrag in der ersten Spalte
    with col1:
        st.subheader("Community Garden")
        st.write("A community garden with spaces for everyone to plant.")
        st.caption("Tags: #gardening #community #green")

    # Eintrag in der zweiten Spalte
    with col2:
        st.subheader("Sports Day")
        st.write("Weekly community sports day to promote health and well being.")
        st.caption("Tags: #health #sports #weekly")

    # Eintrag in der dritten Spalte
    with col3:
        st.subheader("Book Swap")
        st.write("A monthly book swap event in our local library.")
        st.caption("Tags: #books #library #swap")


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
