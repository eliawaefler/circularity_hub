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
            height: 250px;             /* Feste Höhe */
            display: flex;
            flex-direction: column;
            justify-content: space-between;  /* Inhalt am Anfang und Tags am Ende */
            margin-bottom: 20px;      /* Abstand zwischen den Boxen */
        }
        .large {
            background-color: #f0f0f0;  /* Hellgrauer Hintergrund */
            padding: 20px;
            border-radius: 10px;
            height: 600px;             /* Feste Höhe */
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
                <h4>Speckle</h4>
                <p>Informationen rund um den Workflow mit Speckle.</p>
                <p style='opacity: 0.6;'>#digitalezwillinge #bim #speckleintegration</p>
            </div>
            """, unsafe_allow_html=True)

    # Eintrag in der zweiten Spalte
    with col2:
        st.markdown("""
            <div class='box'>
                <h4>Best Practice</h4>
                <p>Anwendungsfälle der Community.</p>
                <p style='opacity: 0.6;'>#outofthebox #buildingsmart</p>
            </div>
            """, unsafe_allow_html=True)

    # Eintrag in der dritten Spalte
    with col3:
        st.markdown("""
            <div class='box'>
                <h4>Events</h4>
                <p>Seien dabei und lerne vieles Neues dazu!</p>
                <p style='opacity: 0.6;'>#community #learn #havefun #events</p>
            </div>
            """, unsafe_allow_html=True)

    # Eintrag von Planer
    with st.container():
        st.markdown("""
               <div class='large'>
                   <h4>Integration von Second Hand Bauteilen in den Planungsprozess</h4>
                   <p>Ich bin ein Fan von dieser Plattform die den Austausch und die Beschaffung von Second Hand Bauteilen erleichtert!!! Über die Integration mit Speckle kann ich mein digitales Modell direkt auf die Plattform hochladen. Dieser Schritt ist entscheidend, denn dadurch wird automatisch eine Abgleichung aller Bauteile meines Modells mit dem verfügbaren Angebot auf der Plattform durchgeführt. Die Plattform präsentiert mir umgehend alle verfügbaren Bauteile, die den spezifischen Anforderungen meines digitalen Zwillings entsprechen. Diese präzise Übereinstimmung ermöglicht es mir, schnell die passenden Bauteile zu identifizieren. Ich kann diese Bauteile direkt über die Plattform reservieren. Wichtig dabei ist, dass nicht nur die Geometrie der Bauteile, sondern auch die zugehörigen Attribute, die das Bauteil definieren, nahtlos in meine Autorensoftware geladen werden. Dies erfolgt wiederum über die Speckle-Schnittstelle. Durch diesen einfachen und automatisierten Workflow wird der gesamte Planungsprozess erheblich erleichtert. Die Möglichkeit, spezifische Anforderungen direkt mit dem Angebot abzugleichen und die benötigten Bauteile effizient in die Planungssoftware zu integrieren, spart Zeit und fördert die Verwendung von nachhaltigen Materialien. Dieser Ansatz unterstützt nicht nur eine umweltfreundliche Bauweise, sondern optimiert auch die Kosten- und Ressourceneffizienz meines Projekts.</p>
                   <p style='opacity: 0.6;'>#DigitaleZwillinge #BIM #SpeckleIntegration #automatisiertebauteilsuche</p>
               </div>
               """, unsafe_allow_html=True)

    # Eintrag von Bauherrn
    with st.container():
        st.markdown("""
               <div class='large'>
                   <h4>Strategische Planung für die Wiederverwendung von Bauteilen</h4>
                   <p>Als Bauherr in der strategischen Planungsphase eines Neubaus steht für mich Nachhaltigkeit im Vordergrund. Um diesem Anspruch gerecht zu werden, nutze ich eine besondere Funktion unserer Plattform: die Lokalisierung potenzieller Second Hand Bauteile in meiner direkten Umgebung. Durch die Eingabe meines Standorts in die Plattform kann ich sofort alle relevanten Bauwerke einsehen, die in den kommenden Jahren möglicherweise wiederverwendbare Bauteile anbieten werden. Diese frühzeitige Identifizierung potenzieller Quellen ermöglicht es mir, meine Planung entsprechend auszurichten und langfristige Kooperationen zu initiieren. Diese proaktive Herangehensweise ist nicht nur wirtschaftlich sinnvoll, sondern trägt auch maßgeblich zu einer umweltfreundlichen Bauweise bei. Ich möchte diese Plattform nutzen, um mit Gleichgesinnten in Kontakt zu treten, die ebenfalls an der Integration von Second Hand Materialien interessiert sind. Gemeinsam können wir Synergien schaffen und die Verfügbarkeit solcher Materialien in unserer Branche fördern. Ich lade alle Interessierten ein, sich mit mir über die Möglichkeiten auszutauschen und unsere Ressourcen zu bündeln, um unsere Bauvorhaben nachhaltiger und effizienter zu gestalten. Vielen Dank für Ihre Aufmerksamkeit und Ihr Engagement für eine grünere Bauwelt.</p>
                   <p style='opacity: 0.6;'>#strategisch #neartoyou #nachhaltig</p>
               </div>
               """, unsafe_allow_html=True)

    # Eintrag von Handwerker
    with st.container():
        st.markdown("""
               <div class='large'>
                   <h4>Effizienzsteigerung durch präzise Bauteil-Identifikation im Handwerk</h4>
                   <p>Liebe Handwerker-Gemeinschaft, als Handwerker arbeite ich eng mit Planern und Bauherren zusammen, um die Nachhaltigkeit und Effizienz unserer Bauprojekte zu maximieren. Ein wesentlicher Aspekt meiner Arbeit besteht darin, die von Planern oder Bauherren spezifizierten, wiederverwendbaren Bauteile effektiv zu integrieren. Für jedes Projekt erhalte ich eine Liste mit Bauteilen, die wiederverwendet werden sollen. Diese Bauteile sind sowohl im Architektenplan als auch auf unserer Plattform mit einer Global Trade Item Number (GTIN) gekennzeichnet. Diese systematische Kennzeichnung ermöglicht es mir, die Bauteile physisch vor Ort zu markieren und genau zu identifizieren. Dank der GTIN kann ich jedes Bauteil exakt zuordnen und sicherstellen, dass es gemäß den Planungsvorgaben eingebaut wird. Diese präzise Methode erleichtert die Montage, vermeidet Verwechslungen und fördert eine effiziente Arbeitsweise. Diese Vorgehensweise ist nicht nur zeitsparend, sondern trägt auch dazu bei, Fehlerquellen zu minimieren und die Qualität unserer Bauausführungen zu sichern. Ich schätze die Möglichkeiten, die unsere Plattform bietet, um nachhaltig und präzise zu arbeiten, und empfehle jedem Handwerker, diesen Ansatz zu verfolgen. Lasst uns gemeinsam die Vorteile der digitalen Vernetzung nutzen und unsere Bauprojekte effizienter und umweltfreundlicher gestalten!</p>
                   <p style='opacity: 0.6;'>#GTIN #workflow #zusammenarbeit</p>
               </div>
               """, unsafe_allow_html=True)

    # Button zum Hinzufügen neuer Beiträge
    if st.button('Add New Post'):
        set_create_new_topic 
        new_topic()


def new_topic():
    st.header("Create a new Topic")
    title = st.text_input("Type title, or paste a link here")
    category = st.selectbox("Select a category", ["Anwendungsfälle", "Workflow", "News"])

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
