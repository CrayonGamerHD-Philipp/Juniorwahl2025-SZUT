import pandas as pd
import streamlit as st
import plotly.express as px

# CSV-Datei laden
file_path = "Juniorwahl_2025_Auwertung_CSV_v1.csv"
df = pd.read_csv(file_path, encoding="UTF-8", delimiter=";")

# Spalten umbenennen
df.columns = [
    "Nr", "Erststimme", "Zweitstimme", "Vorherige Teilnahme", "Wahlabsicht",
    "Parteivertrauen", "Interesse an Politik", "Vorbereitung im Unterricht",
    "Parteiziele verstehen", "Zukunftssicht", "Geschlecht",
    "Plakat", "Wahlprogramme", "TV", "Zeitung", "Keine",
    "TikTok", "Instagram", "X", "YouTube",
    "Twitch", "Kein Socialmedia"
]

df.columns2 = [
    "Nr", "Erststimme", "Zweitstimme", "Vorherige Teilnahme", "Wahlabsicht",
    "Parteivertrauen", "Interesse an Politik", "Vorbereitung im Unterricht",
    "Parteiziele verstehen", "Zukunftssicht", "Geschlecht"
]

# Farbkodierung der Parteien
partei_farben = {
    "CDU": "#000000",  # Schwarz
    "Sandra Schmull / CDU": "#000000",
    "SPD": "#E3000F",  # Rot
    "Uwe Schmidt / SPD": "#E3000F",
    "Grünen": "#1FA12D",# Grün
    "Micheal Labetzke / Grünen": "#1FA12D",
    "FDP": "#FFD700",  # Gelb
    "AFD": "#009EE0",  # Hellblau
    "Arno Staschewski / AFD": "#009EE0",
    "Die Linke": "#BE3075",  # Magenta/Pink
    "Darius Hassanpour / Die Linke": "#BE3075",
    "BSW": "#0072A3",  # Dunkelblau
    "Volt": "#562885",  # Lila
    "Matthias Cornelsen / Volt": "#562885",
    "Tierschutz Partei": "#006400",  # Dunkelgrün
    "Die Partei": "#A0A0A0",  # Grau
    "MERA25": "#8B0000",  # Dunkelrot
    "Sonstige": "#808080",
    "Opposition": "#808080"
}

# Streamlit App UI
st.set_page_config(
    layout="wide",
    page_title="Juniorwahl 2025",
    page_icon="🗳️",
    initial_sidebar_state="expanded"
)
# CSS hinzufügen, um das Menü auszublenden
st.markdown(
    """
    <style>
        /* Versteckt das Streamlit-Menü (drei Punkte) */
        #MainMenu {visibility: hidden;}

        /* Versteckt den Deploy-Button */
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
    .info-box {
        background-color: #181b24;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .info-box h1 {
        color: #ffffff;
        font-size: 28px;
        text-align: center;
    }
    .info-box p, .info-box li {
        color: #ffffff;
        font-size: 18px;
        line-height: 1.5;
    }
    .info-box a {
        color: #1E90FF;
        font-weight: bold;
    }
</style>

<div class="info-box">
    <h1>📊 Digitale & Interaktive Auswertung der Juniorwahl am SZUT</h1>
    <p>
        Willkommen zur <b>digitalen und interaktiven Auswertung</b> der <b>Juniorwahl</b> 
        am <b>Schulzentrum Utbremen (SZUT)</b> zur <b>Bundestagswahl 2025</b>.  
    </p>
    <p>
        Die <b>Juniorwahl</b> gibt Schüler*innen die Möglichkeit, den demokratischen Wahlprozess hautnah zu erleben. 
        Auch wenn die Stimmen nicht in das offizielle Wahlergebnis einfließen, spiegeln sie die politische Meinung 
        der jungen Generation wider.
    </p>
    <h2>🛠️ So funktioniert die Auswertung:</h2>
    <ul>
        <li>Alle <b>Wahlergebnisse</b> der Juniorwahl am SZUT werden hier <b>visuell und interaktiv</b> dargestellt.</li>
        <li><b>Diagramme und Grafiken</b> zeigen die Verteilung der Stimmen sowie mögliche Koalitionen.</li>
        <li>Nutzer*innen können die Ergebnisse nach <b>verschiedenen Kriterien filtern und analysieren</b>.</li>
    </ul>
    <p>
        Diese Plattform bietet eine <b>transparente, verständliche und moderne</b> Möglichkeit, 
        die Wahlbeteiligung und politischen Trends am SZUT zu erkunden.
    </p>
    <p>
        🔗 <a href="https://www.szut.de/" target="_blank">Mehr über das Schulzentrum Utbremen</a>
    </p>
</div>
""", unsafe_allow_html=True)

st.title("📊 Juniorwahl 2025 - Dynamische Auswertung")

# Erstelle Mehrfachauswahl-Filter für alle Kategorien links im Seitenbereich
st.sidebar.header("🔍 Filter Optionen")

filters = {}
for col in df.columns2[1:]:  # Erste Spalte "Nr" ignorieren
    unique_values = df[col].dropna().unique()
    if len(unique_values) > 1 and len(unique_values) < 20:  # Nur Kategorien mit wenigen Werten als Auswahloption
        filters[col] = st.sidebar.multiselect(f"{col}", options=["Alle"] + list(unique_values), default=["Alle"])

# Individuelle Mehrfachauswahl für Social Media & Informationsquellen mit "Alle" als Standard
social_columns = ["TikTok", "Instagram", "X", "YouTube", "Twitch", "Kein Socialmedia"]
info_columns = ["Plakat", "Wahlprogramme", "TV", "Zeitung", "Keine"]

filters["Social Media Nutzung"] = st.sidebar.multiselect("📱 Social Media Nutzung", options=["Alle"] + social_columns, default=["Alle"])
filters["Informationsquellen"] = st.sidebar.multiselect("📰 Informationsquellen", options=["Alle"] + info_columns, default=["Alle"])

# Filter anwenden
filtered_df = df.copy()
for col, values in filters.items():
    if "Alle" not in values:  # Nur filtern, wenn nicht "Alle" gewählt ist
        if col in ["Social Media Nutzung", "Informationsquellen"]:
            filtered_df = filtered_df[filtered_df[values].eq("WAHR").any(axis=1)]
        else:
            filtered_df = filtered_df[filtered_df[col].isin(values)]

# Sicherstellen, dass alle Parteien in den Farben enthalten sind
parteien_erststimme = filtered_df["Erststimme"].unique()
parteien_zweitstimme = filtered_df["Zweitstimme"].unique()


# Fehlende Parteien in der Farbzuordnung ergänzen (damit keine Fehler auftreten)
for partei in list(parteien_erststimme) + list(parteien_zweitstimme):
    if partei not in partei_farben:
        partei_farben[partei] = "#808080"  # Grau für unbekannte Parteien

# 🗳️ Wahl-Ergebnisse mit Tabs
st.write("### 🗳️ Wahlergebnisse")

tab1, tab2 = st.tabs(["📊 Kreisdiagramme", "📈 Balkendiagramme"])

with tab1:
    st.write("#### 📊 Erst- und Zweitstimmen als Kreisdiagramm")
    col1, col2 = st.columns(2)

    with col1:
        fig_erststimme = px.pie(
            filtered_df,
            names="Erststimme",
            title="Verteilung der Erststimmen",
            color="Erststimme",
            color_discrete_map=partei_farben
        )
        fig_erststimme.update_layout(
            title_font_size=22,
            legend_font_size=18
        )
        st.plotly_chart(fig_erststimme, use_container_width=True)

    with col2:
        fig_zweitstimme = px.pie(
            filtered_df,
            names="Zweitstimme",
            title="Verteilung der Zweitstimmen",
            color="Zweitstimme",
            color_discrete_map=partei_farben
        )
        fig_zweitstimme.update_layout(
            title_font_size=22,
            legend_font_size=16
        )
        st.plotly_chart(fig_zweitstimme, use_container_width=True)

with tab2:
    st.write("#### 📈 Erst- und Zweitstimmen als Balkendiagramm")
    col1, col2 = st.columns(2)

    # Korrigierte Version für Balkendiagramme
    erststimme_counts = filtered_df["Erststimme"].value_counts().reset_index()
    erststimme_counts.columns = ["Kandidat", "Anzahl"]
    erststimme_counts["Prozent"] = (erststimme_counts["Anzahl"] / erststimme_counts["Anzahl"].sum()) * 100

    zweitstimme_counts = filtered_df["Zweitstimme"].value_counts().reset_index()
    zweitstimme_counts.columns = ["Partei", "Anzahl"]
    zweitstimme_counts["Prozent"] = (zweitstimme_counts["Anzahl"] / zweitstimme_counts["Anzahl"].sum()) * 100

    with col1:
        fig_erststimme_bar = px.bar(
            erststimme_counts,
            x="Kandidat",
            y="Anzahl",
            text=erststimme_counts.apply(lambda row: f"{row['Prozent']:.1f}% ({row['Anzahl']})", axis=1),
            title="Erststimmen Verteilung",
            color="Kandidat",
            color_discrete_map=partei_farben
        )
        fig_erststimme_bar.update_layout(
            title_font_size=22,
            xaxis_tickfont_size=14,
            showlegend=False
        )
        st.plotly_chart(fig_erststimme_bar, use_container_width=True)

    with col2:
        fig_zweitstimme_bar = px.bar(
            zweitstimme_counts,
            x="Partei",
            y="Anzahl",
            text=zweitstimme_counts.apply(lambda row: f"{row['Prozent']:.1f}% ({row['Anzahl']})", axis=1),
            title="Zweitstimmen Verteilung",
            color="Partei",
            color_discrete_map=partei_farben
        )
        fig_zweitstimme_bar.update_layout(
            title_font_size=22,
            xaxis_tickfont_size=14,
            showlegend=False
        )
        st.plotly_chart(fig_zweitstimme_bar, use_container_width=True)

# 🔢 Berechnung möglicher Koalitionen
st.write("### 🤝 Mögliche Koalitionen")

# Berechnung der Parteien-Anteile in Prozent
total_stimmen = filtered_df["Zweitstimme"].count()
partei_anteile = filtered_df["Zweitstimme"].value_counts(normalize=True) * 100

# Definiere Koalitionsmöglichkeiten (ab 50% Mehrheit)
moegliche_koalitionen_2er = []
moegliche_koalitionen_3er = []
parteien = partei_anteile.index.tolist()

# Überprüfung von 2er- und 3er-Kombinationen
for i in range(len(parteien)):
    for j in range(i + 1, len(parteien)):
        summe = partei_anteile[parteien[i]] + partei_anteile[parteien[j]]
        if summe >= 50:
            moegliche_koalitionen_2er.append((parteien[i], parteien[j], summe))

        for k in range(j + 1, len(parteien)):
            summe = partei_anteile[parteien[i]] + partei_anteile[parteien[j]] + partei_anteile[parteien[k]]
            if summe >= 50:
                moegliche_koalitionen_3er.append((parteien[i], parteien[j], parteien[k], summe))

# Sortiere die Koalitionen nach Stimmenanteil (größte zuerst)
moegliche_koalitionen_2er = sorted(moegliche_koalitionen_2er, key=lambda x: x[2], reverse=True)
moegliche_koalitionen_3er = sorted(moegliche_koalitionen_3er, key=lambda x: x[3], reverse=True)

# Tab-System für die Darstellung
tab1, tab2 = st.tabs(["🔷 2er-Koalitionen", "🔶 3er-Koalitionen"])

def plot_koalition(labels, sizes, title):
    """Erstellt ein Plotly-Diagramm mit Opposition."""
    opposition = 100 - sum(sizes)
    labels.append("Opposition")
    sizes.append(opposition)
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "gray"][:len(labels)]  # Opposition immer in Grau

    fig = px.pie(
        names=labels,
        values=sizes,
        title=title,
        hole=0.3,
        color=labels,
        color_discrete_map=partei_farben
    )
    fig.update_layout(
        title_font_size=22,
        legend_font_size=16
    )
    return fig

with tab1:
    if moegliche_koalitionen_2er:
        # Zeige die **4 größten** Koalitionen direkt an
        cols = st.columns(4)
        for index, koalition in enumerate(moegliche_koalitionen_2er[:4]):  # Zeigt nur die 4 größten
            labels = [koalition[0], koalition[1]]
            sizes = [partei_anteile[koalition[0]], partei_anteile[koalition[1]]]
            title = f"{koalition[0]} + {koalition[1]} ({koalition[2]:.1f}%)"
            with cols[index % 4]:
                st.plotly_chart(plot_koalition(labels, sizes, title), use_container_width=True)

        # Restliche Koalitionen in einem ausklappbaren Bereich anzeigen
        if len(moegliche_koalitionen_2er) > 4:
            with st.expander("➕ Weitere 2er-Koalitionen anzeigen"):
                for koalition in moegliche_koalitionen_2er[4:]:  # Zeigt die restlichen an
                    labels = [koalition[0], koalition[1]]
                    sizes = [partei_anteile[koalition[0]], partei_anteile[koalition[1]]]
                    title = f"{koalition[0]} + {koalition[1]} ({koalition[2]:.1f}%)"
                    st.plotly_chart(plot_koalition(labels, sizes, title), use_container_width=True)
    else:
        st.write("❌ **Keine 2er-Koalitionen mit Mehrheit gefunden.**")

with tab2:
    if moegliche_koalitionen_3er:
        # Zeige die **4 größten** Koalitionen direkt an
        cols = st.columns(4)
        for index, koalition in enumerate(moegliche_koalitionen_3er[:4]):  # Zeigt nur die 4 größten
            labels = [koalition[0], koalition[1], koalition[2]]
            sizes = [partei_anteile[koalition[0]], partei_anteile[koalition[1]], partei_anteile[koalition[2]]]
            title = f"{koalition[0]} + {koalition[1]} + {koalition[2]} ({koalition[3]:.1f}%)"
            with cols[index % 4]:
                st.plotly_chart(plot_koalition(labels, sizes, title), use_container_width=True)

        # Restliche Koalitionen in einem ausklappbaren Bereich anzeigen
        if len(moegliche_koalitionen_3er) > 4:
            with st.expander("➕ Weitere 3er-Koalitionen anzeigen"):
                for koalition in moegliche_koalitionen_3er[4:]:  # Zeigt die restlichen an
                    labels = [koalition[0], koalition[1], koalition[2]]
                    sizes = [partei_anteile[koalition[0]], partei_anteile[koalition[1]], partei_anteile[koalition[2]]]
                    title = f"{koalition[0]} + {koalition[1]} + {koalition[2]} ({koalition[3]:.1f}%)"
                    st.plotly_chart(plot_koalition(labels, sizes, title), use_container_width=True)
    else:
        st.write("❌ **Keine 3er-Koalitionen mit Mehrheit gefunden.**")

# 📊 Weitere Diagramme für Parteivertrauen, Wahlabsicht, etc.
st.write("### 📊 Grafische Auswertung")

col3, col4 = st.columns(2)

with col3:
    fig1 = px.histogram(filtered_df, x="Parteivertrauen", title="Vertrauen in Parteien", color="Parteivertrauen")
    fig1.update_layout(
        title_font_size=22,
        legend_font_size=16
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(filtered_df, names="Zukunftssicht", title="Wie sehen die Schüler die Zukunft?")
    fig2.update_layout(
        title_font_size=22,
        legend_font_size=16
    )
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    fig3 = px.histogram(filtered_df, x="Geschlecht", title="Geschlechterverteilung", color="Geschlecht")
    fig3.update_layout(
        title_font_size=22,
        legend_font_size=16
    )
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.histogram(filtered_df, x="Wahlabsicht", title="Wahlbeteiligung", color="Wahlabsicht")
    fig4.update_layout(
        title_font_size=22,
        legend_font_size=16
    )
    st.plotly_chart(fig4, use_container_width=True)

# 📱 Nutzung von Social Media zur Information
st.write("### 📱 Nutzung von Social Media zur Information")

social_counts = filtered_df[social_columns].apply(lambda x: (x == "WAHR").sum())

fig_social = px.bar(social_counts, x=social_counts.index, y=social_counts.values, title="Social Media Nutzung (Gefiltert)", labels={"y": "Anzahl Personen"})
fig_social.update_layout(
    title_font_size=22,
    legend_font_size=16
)
st.plotly_chart(fig_social, use_container_width=True)

# ❓ Analyse aller Fragen mit Geschlechter-Aufteilung (nur zusammengefasste Social Media & Infoquellen)
st.write("### ❓ Analyse aller Fragen nach Geschlechtern")

# **Dropdown-Menü für Fragen + Zusammenfassungen für Social Media & Informationsquellen**
fragen_liste = [frage for frage in df.columns[1:] if frage not in ["Geschlecht"] + social_columns + info_columns]  # Einzelne Social-Media- und Info-Optionen entfernen
fragen_liste.insert(0, "📱 Social Media Nutzung")  # Nur zusammengefasst
fragen_liste.insert(1, "📰 Informationsquellen")  # Nur zusammengefasst

# Benutzer wählt eine Frage aus
frage = st.selectbox("Wähle eine Frage:", fragen_liste)

if frage:
    vorhandene_geschlechter = filtered_df["Geschlecht"].dropna().unique()

    if frage == "📱 Social Media Nutzung":
        st.write("📱 **Zusammenfassung aller Social Media Nutzungen nach Geschlecht**")

        social_data = filtered_df.melt(id_vars=["Geschlecht"], value_vars=social_columns, var_name="Social Media", value_name="Nutzung")
        social_data = social_data[social_data["Nutzung"] == "WAHR"].drop(columns=["Nutzung"])

        social_counts = social_data.groupby(["Social Media", "Geschlecht"]).size().reset_index(name="Anzahl")

        for geschlecht in vorhandene_geschlechter:
            for platform in social_columns:
                if not ((social_counts["Social Media"] == platform) & (social_counts["Geschlecht"] == geschlecht)).any():
                    social_counts = pd.concat([social_counts, pd.DataFrame({"Social Media": [platform], "Geschlecht": [geschlecht], "Anzahl": [0]})])

        fig_social = px.bar(
            social_counts,
            x="Social Media",
            y="Anzahl",
            color="Geschlecht",
            barmode="group",
            title="Social Media Nutzung nach Geschlecht"
        )
        fig_social.update_layout(
            title_font_size=22,
            legend_font_size=16
        )
        st.plotly_chart(fig_social, use_container_width=True)

    elif frage == "📰 Informationsquellen":
        st.write("📰 **Zusammenfassung aller Informationsquellen nach Geschlecht**")

        info_data = filtered_df.melt(id_vars=["Geschlecht"], value_vars=info_columns, var_name="Informationsquelle", value_name="Nutzung")
        info_data = info_data[info_data["Nutzung"] == "WAHR"].drop(columns=["Nutzung"])

        info_counts = info_data.groupby(["Informationsquelle", "Geschlecht"]).size().reset_index(name="Anzahl")

        for geschlecht in vorhandene_geschlechter:
            for quelle in info_columns:
                if not ((info_counts["Informationsquelle"] == quelle) & (info_counts["Geschlecht"] == geschlecht)).any():
                    info_counts = pd.concat([info_counts, pd.DataFrame({"Informationsquelle": [quelle], "Geschlecht": [geschlecht], "Anzahl": [0]})])

        fig_info = px.bar(
            info_counts,
            x="Informationsquelle",
            y="Anzahl",
            color="Geschlecht",
            barmode="group",
            title="Informationsquellen nach Geschlecht"
        )
        fig_info.update_layout(
            title_font_size=22,
            legend_font_size=16
        )
        st.plotly_chart(fig_info, use_container_width=True)

    else:
        antworten_counts = filtered_df.groupby([frage, "Geschlecht"]).size().reset_index(name="Anzahl")

        for geschlecht in vorhandene_geschlechter:
            for antwort in filtered_df[frage].dropna().unique():
                if not ((antworten_counts[frage] == antwort) & (antworten_counts["Geschlecht"] == geschlecht)).any():
                    antworten_counts = pd.concat([antworten_counts, pd.DataFrame({frage: [antwort], "Geschlecht": [geschlecht], "Anzahl": [0]})])

        fig_frage = px.bar(
            antworten_counts,
            x=frage,
            y="Anzahl",
            color="Geschlecht",
            barmode="group",
            title=f"Antwortverteilung für: {frage} nach Geschlecht"
        )
        fig_frage.update_layout(
            title_font_size=22,
            legend_font_size=16
        )
        st.plotly_chart(fig_frage, use_container_width=True)

# 📋 Gefilterte Ergebnisse als Tabelle
st.write("### 📋 Gefilterte Ergebnisse")
st.dataframe(filtered_df, height=500)

st.markdown("---")  # Trennlinie
st.markdown("🚀 powered by Philipp Hethey  |  ITA24", unsafe_allow_html=True)