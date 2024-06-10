import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessing
import helper
import plotly.express as px

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(layout="wide")

# Menampilkan logo Olimpiade di sidebar
st.sidebar.image("olympics.png", use_column_width=True)
st.sidebar.title("OLYMPICS")

# Memilih opsi untuk menampilkan halaman
page = st.sidebar.radio("Options", ["medals", "overall analysis", "Athlete"])

def page_medals():
    # Menampilkan halaman analisis medali
    st.title("Medal Analysis")
    st.markdown("---")

    # Memilih wilayah dan musim
    col1, col2 = st.columns(2)
    with col1:
        region_input = st.selectbox("Select the region", options=helper.region_options())
    with col2:
        season_input = st.selectbox("Select the Season", options=["All Season", "Summer", "Winter"])

    # Memilih rentang tahun
    year_from, year_to = st.slider("Year", min_value=helper.year_scale()[0], max_value=helper.year_scale()[1], value=(1988, 2015))

    # Menampilkan tabel total medali berdasarkan pilihan pengguna
    dataset = preprocessing.subset_and_display_medal(season=season_input, region=region_input, from_year=year_from, to_year=year_to)
    st.title(f"Total Medals {region_input} ({year_from} - {year_to})")
    st.table(dataset)
    st.markdown("---")

    # Menampilkan plot medali
    st.title("Plotting Medals")
    st.plotly_chart(helper.plot_medal(region_input, year_from, year_to))

def overall_analysis():
    # Menampilkan analisis umum
    st.title("Top Statistics")
    st.markdown("---")

    # Menampilkan statistik umum
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Region")
        st.title(helper.num_analysis()[3])
        st.header("Athlete")
        st.title(helper.num_analysis()[1])
    with col2:
        st.header("Event")
        st.title(helper.num_analysis()[2])
        st.header("Sport")
        st.title(helper.num_analysis()[0])
    with col3:
        st.header("Games")
        st.title(helper.num_analysis()[5])
        st.header("Team")
        st.title(helper.num_analysis()[4])
    st.markdown("---")

    # Menampilkan top 50 negara peserta
    st.title("Top 50 Participant Countries:")
    st.table(data=preprocessing.country_game().head(50))
    st.markdown("---")

    # Menampilkan partisipan tahunan
    st.title("Yearly Participants")
    st.plotly_chart(helper.plot_participant())
    st.markdown("---")

    # Menampilkan kota tuan rumah
    st.title("Host City:")
    st.plotly_chart(helper.plot_city())
    st.markdown("---")

    # Menampilkan musim
    st.title("Season:")
    st.plotly_chart(helper.plot_season())
    st.markdown("---")

    # Menampilkan total atlet
    st.title("Total Athlete:")
    col1, col2 = st.columns(2)
    with col1:
        athlete_sort = st.selectbox(label="Sort By:", options=["Region", "Total Athlete"])
    with col2:
        ascending_athlete = st.selectbox(label="Ascending:", options=[True, False])
    st.table(preprocessing.athlete_per_country_data(sort=athlete_sort, ascending_pram=ascending_athlete))
    st.markdown("---")

    # Menampilkan partisipan per game
    st.title("Participants per Game:")
    st.plotly_chart(helper.vil_games_participant())

    # Menampilkan data olahraga per tahun
    st.title("Sport by Year:")
    st.table(preprocessing.sport_data_count()[0])
    st.title("Plotting:")
    st.plotly_chart(helper.plot_sport())
    st.markdown("---")

def Athlate_page():
    # Menampilkan analisis data atlet
    st.title("Athlete Data Analysis")
    st.markdown("---")

    # Memilih negara dan olahraga
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Country:", options=helper.region_options())
    with col2:
        sport = st.selectbox("Sport:", options=helper.sport_options())

    # Memilih rentang tahun
    fromm, too = st.slider("Year:", min_value=helper.year_scale()[0], max_value=helper.year_scale()[1], value=(1988, 2015))

    # Menampilkan total jumlah atlet
    col1, col2 = st.columns(2)
    with col1:
        st.write("")
        st.subheader("Total Number of Athletes:")
    with col2:
        st.title(helper.total_vil(fromm, too, country, sport)[0])

    col1, col2, col3 = st.columns([1, 6, 1])  # Mengatur kolom dengan perbandingan lebar 1:6:1

    with col2:
        st.dataframe(helper.total_vil(fromm , too , country , sport)[1])

    # Menampilkan plot data atlet
    st.title("Plot")
    st.plotly_chart(helper.sport_vil(fromm, too, country, sport))
    st.markdown("---")

    # Menampilkan top 20 atlet
    st.title("Top 20 Athletes:")
    st.table(preprocessing.top_medal())

    # Menampilkan plot top 20 atlet
    st.title("Plot:")
    st.plotly_chart(helper.top_medal_vil())
    st.markdown("---")

    # Menampilkan top 30 atlet berdasarkan olahraga
    st.title("Top 30 Athletes by Each Sport")
    sport = st.selectbox("Sport :", options=helper.sport_options())
    too = st.slider("Year:", min_value=helper.year_scale()[0], max_value=helper.year_scale()[1])
    st.table(preprocessing.data_sport_top(sport, too))
    st.plotly_chart(helper.top30_medal_vil(sport, too))
    st.markdown("---")

    # Menampilkan komposisi gender
    st.title("Gender Composition:")
    st.table(preprocessing.sex_data())
    st.title("Plot:")
    st.plotly_chart(helper.sex_vil())
    st.markdown("---")

    # Menampilkan komposisi gender berdasarkan olahraga
    st.title("Gender Composition by Sport:")
    sportt = st.selectbox("Select Sport:", options=helper.sport_options())
    st.table(preprocessing.sex_data_sport(sport=sportt))
    st.title("Plot:")
    st.plotly_chart(helper.sex_vil_sport(sportt))

    # Menampilkan tinggi vs berat badan atlet
    st.title("Height vs Weight:")
    sporttt = st.selectbox("select sport :  " , options=helper.sport_options_nall())
    regionn = st.selectbox("region :  " , options=helper.region_options())


    st.plotly_chart(helper.plot_height_weight(sport=sporttt , region=regionn))   






    

if page == "medals" : 
    page_medals()
elif page == "overall analysis" : 
    overall_analysis()
elif page == "Athlete":
    Athlate_page()
