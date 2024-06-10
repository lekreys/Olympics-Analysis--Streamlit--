import preprocessing  # Import modul preprocessing untuk memproses data Olimpiade
import plotly.express as px  # Import Plotly Express untuk membuat plot interaktif
import seaborn as sns  # Import Seaborn untuk membuat plot statistik
import numpy as np  # Import NumPy untuk manipulasi data numerik
import plotly.graph_objects as go  # Import Plotly Graph Objects untuk membuat plot kustom

def region_options():
    """
    Mendapatkan daftar pilihan wilayah dari data yang sudah diproses.
    
    Returns:
        list: Daftar pilihan wilayah.
    """
    data = preprocessing.clear_data()  # Mendapatkan data yang sudah diproses
    region_list = data["region"].unique().tolist()  # Mendapatkan daftar unik wilayah
    region_list.append("All")  # Menambahkan opsi "All" untuk semua wilayah
    return region_list

def sport_options():
    """
    Mendapatkan daftar pilihan olahraga dari data yang sudah diproses.
    
    Returns:
        list: Daftar pilihan olahraga.
    """
    data = preprocessing.clear_data()  # Mendapatkan data yang sudah diproses
    sport_list = data["Sport"].unique().tolist()  # Mendapatkan daftar unik olahraga
    sport_list.append("All")  # Menambahkan opsi "All" untuk semua olahraga
    return sport_list

def sport_options_nall():
    """
    Mendapatkan daftar pilihan olahraga dari data yang sudah diproses.
    
    Returns:
        list: Daftar pilihan olahraga.tanpa All options
    """
    data = preprocessing.clear_data()  # Mendapatkan data yang sudah diproses
    sport_list = data["Sport"].unique().tolist()  # Mendapatkan daftar unik olahraga
    return sport_list

def year_scale():
    """
    Menetapkan skala tahun dari data yang sudah diproses.
    
    Returns:
        list: Daftar dengan tahun minimum dan maksimum.
    """
    data = preprocessing.clear_data()  # Mendapatkan data yang sudah diproses
    list_min_max_year = [min(data["Year"]), max(data["Year"])]  # Mendapatkan tahun minimum dan maksimum
    return list_min_max_year

def plot_medal(country, fromm, to):
    """
    Menampilkan plot medali untuk wilayah, rentang tahun tertentu.
    
    Args:
        country (str): Wilayah yang akan dianalisis.
        fromm (int): Tahun awal rentang.
        to (int): Tahun akhir rentang.
    
    Returns:
        go.Figure: Plot medali menggunakan Plotly Graph Objects.
    """
    data = preprocessing.plot_data()  # Mendapatkan data medali yang sudah diproses
    data_subset = data[data["region"] == country]  # Mendapatkan subset data berdasarkan wilayah
    data_subset_year = data_subset[np.logical_and(data_subset["Year"] <= to, data_subset["Year"] >= fromm)]  # Mendapatkan subset data berdasarkan rentang tahun
    data_subset_year.columns = ["Year", "region", "gold", "silver", "bronze", "total"]  # Menyusun ulang nama kolom
    
    # Membuat plot menggunakan Plotly Graph Objects
    fig = go.Figure()
    # Menambahkan garis untuk setiap jenis medali
    fig.add_trace(go.Scatter(x=data_subset_year["Year"], y=data_subset_year["gold"], mode='lines+markers', name='Gold', line=dict(color='gold')))
    fig.add_trace(go.Scatter(x=data_subset_year["Year"], y=data_subset_year["silver"], mode='lines+markers', name='Silver', line=dict(color='silver')))
    fig.add_trace(go.Scatter(x=data_subset_year["Year"], y=data_subset_year["bronze"], mode='lines+markers', name='Bronze', line=dict(color='brown')))
    
    # Mengatur layout untuk plot
    fig.update_layout(title=f'Number of Medals {country}', xaxis=dict(title='Year'), yaxis=dict(title='Number of Medals'), width=1400, height=800)
    return fig

# Fungsi-fungsi lainnya telah dijelaskan dengan cukup baik dan tidak memerlukan komentar tambahan.

def num_analysis():
    """
    Melakukan analisis statistik terhadap data Olimpiade, termasuk jumlah olahraga unik, jumlah atlet unik,
    jumlah acara unik, jumlah wilayah unik, jumlah tim unik, dan jumlah permainan unik.
    
    Returns:
        list: Daftar yang berisi jumlah olahraga unik, jumlah atlet unik, jumlah acara unik, jumlah wilayah unik,
              jumlah tim unik, dan jumlah permainan unik.
    """
    data = preprocessing.clear_data()  # Mengambil data yang sudah diproses
    num_sport = data["Sport"].nunique()  # Jumlah olahraga unik
    num_athlete = data["Name"].nunique()  # Jumlah atlet unik
    num_event = data["Event"].nunique()  # Jumlah acara unik
    num_region = data["NOC"].nunique()  # Jumlah wilayah unik (National Olympic Committee)
    num_team = data["Team"].nunique()  # Jumlah tim unik
    num_games = data["Games"].nunique()  # Jumlah permainan unik
    return [num_sport, num_athlete, num_event, num_region, num_team, num_games]


def plot_participant():
    """
    Membuat plot interaktif menggunakan Plotly Express yang menampilkan jumlah peserta per tahun dalam Olimpiade.
    
    Returns:
        plotly.graph_objects.Figure: Plot interaktif jumlah peserta per tahun.
    """
    data = preprocessing.participant_data()  # Mengambil data jumlah peserta per tahun
    fig = px.line(data, x="Year", y="number country", width=1400, height=800)  # Membuat plot menggunakan Plotly Express
    return fig


def plot_city():
    """
    Membuat plot batang menggunakan Plotly Express yang menampilkan jumlah kota tuan rumah Olimpiade.
    
    Returns:
        plotly.graph_objects.Figure: Plot batang jumlah kota tuan rumah.
    """
    data = preprocessing.city_data()  # Mengambil data jumlah kota tuan rumah
    fig = px.bar(data, x='city', y='num', title='City count', width=1400, height=800)  # Membuat plot menggunakan Plotly Express
    return fig

def plot_season():
    """
    Membuat plot bar yang menampilkan jumlah acara Olimpiade yang diadakan setiap musim.

    Returns:
    plotly.graph_objs._figure.Figure: Objek plotly Figure yang berisi plot bar.
    """
    data = preprocessing.season_data()

    fig = px.bar(data, x='season', y='num', title='Season count', width=1400, height=800)

    return fig


def plot_sport():
    """
    Membuat plot interaktif menggunakan Plotly Express yang menampilkan jumlah olahraga dalam Olimpiade per tahun.
    
    Returns:
        plotly.graph_objects.Figure: Plot interaktif jumlah olahraga per tahun.
    """
    data = preprocessing.sport_data_count()[0]  # Mengambil data jumlah olahraga per tahun
    fig = px.line(data, x='Year', y='Sport', title='Sport count', width=1400, height=800)  # Membuat plot menggunakan Plotly Express
    return fig


def total_vil(fromm, too, country, sport):
    """
    Menghitung total atlet yang berpartisipasi dari suatu wilayah dan olahraga tertentu dalam rentang waktu yang ditentukan.
    
    Args:
        fromm (int): Tahun awal rentang waktu.
        too (int): Tahun akhir rentang waktu.
        country (str): Wilayah yang akan dianalisis.
        sport (str): Olahraga yang akan dianalisis.
    
    Returns:
        list: Daftar yang berisi total jumlah atlet dan data atlet yang berpartisipasi.
    """
    data = preprocessing.total_athlete(fromm, too, country, sport)  # Mendapatkan data atlet berpartisipasi
    total = data["Name"].nunique()  # Menghitung total jumlah atlet unik
    return [total, data]  # Mengembalikan total dan data atlet


def sport_vil(fromm, too, country, sport):
    """
    Menghasilkan plot bar interaktif yang menampilkan jumlah atlet yang berpartisipasi dalam suatu olahraga tertentu
    dari suatu wilayah dalam rentang waktu yang ditentukan.
    
    Args:
        fromm (int): Tahun awal rentang waktu.
        too (int): Tahun akhir rentang waktu.
        country (str): Wilayah yang akan dianalisis.
        sport (str): Olahraga yang akan dianalisis.
    
    Returns:
        plotly.graph_objects.Figure: Plot bar interaktif jumlah atlet per olahraga.
    """
    data = preprocessing.total_athlete(fromm, too, country, sport)  # Mendapatkan data atlet berpartisipasi
    sportt = data["Sport"].value_counts().to_frame()  # Menghitung jumlah atlet per olahraga
    sport_final = sportt.reset_index()  # Mengatur ulang indeks
    sport_final.columns = ['sport', 'num']  # Menyusun ulang nama kolom
    fig = px.bar(sport_final, x='sport', y='num', title='Sport count', width=1400, height=800)  # Membuat plot menggunakan Plotly Express
    return fig


def top_medal_vil():
    """
    Menghasilkan plot bar bertumpuk yang menampilkan jumlah total medali yang diterima oleh atlet-atlet teratas
    dalam Olimpiade, termasuk medali emas, perak, dan perunggu.
    
    Returns:
        plotly.graph_objects.Figure: Plot bar bertumpuk jumlah total medali.
    """
    total_medal_athlete = preprocessing.top_medal()  # Mendapatkan data atlet teratas
    fig = go.Figure()  # Membuat objek plot baru
    # Menambahkan bar untuk masing-masing jenis medali
    fig.add_trace(go.Bar(x=total_medal_athlete["Name"], y=total_medal_athlete["medal_Gold"], name='Gold', marker_color='gold'))
    fig.add_trace(go.Bar(x=total_medal_athlete["Name"], y=total_medal_athlete["medal_Silver"], name='Silver', marker_color='silver'))
    fig.add_trace(go.Bar(x=total_medal_athlete["Name"], y=total_medal_athlete["medal_Bronze"], name='Bronze', marker_color='brown'))
    # Mengatur layout untuk plot bar bertumpuk
    fig.update_layout(barmode='stack', title='"The Number of Medals Received by Athletes"', xaxis=dict(title='Atlet name'), yaxis=dict(title='Total Medals'), width=1400, height=800)
    return fig
def top30_medal_vil(sport, too):
    """
    Menghasilkan plot bar bertumpuk yang menampilkan jumlah total medali yang diterima oleh 30 atlet teratas dalam suatu olahraga
    tertentu pada tahun tertentu, termasuk medali emas, perak, dan perunggu.
    
    Args:
        sport (str): Olahraga yang akan dianalisis.
        too (int): Tahun dalam rentang waktu yang akan dianalisis.
    
    Returns:
        plotly.graph_objects.Figure: Plot bar bertumpuk jumlah total medali untuk 30 atlet teratas.
    """
    total_medal_athlete = preprocessing.data_sport_top(sport, too)  # Mendapatkan data medali atlet teratas
    fig = go.Figure()  # Membuat objek plot baru
    # Menambahkan bar untuk masing-masing jenis medali
    fig.add_trace(go.Bar(x=total_medal_athlete["Name"], y=total_medal_athlete["medal_Gold"], name='Gold', marker_color='gold'))
    fig.add_trace(go.Bar(x=total_medal_athlete["Name"], y=total_medal_athlete["medal_Silver"], name='Silver', marker_color='silver'))
    fig.add_trace(go.Bar(x=total_medal_athlete["Name"], y=total_medal_athlete["medal_Bronze"], name='Bronze', marker_color='brown'))
    # Mengatur layout untuk plot bar bertumpuk
    fig.update_layout(barmode='stack', title=sport, xaxis=dict(title='Atlet Name'), yaxis=dict(title='Total Medals'), width=1400, height=800)
    # Menampilkan plot
    return fig


def sex_vil():
    """
    Menghasilkan plot garis yang menampilkan komposisi gender peserta Olimpiade dari waktu ke waktu.
    
    Returns:
        plotly.graph_objects.Figure: Plot garis komposisi gender peserta Olimpiade per tahun.
    """
    sex_compotation = preprocessing.sex_data()  # Mendapatkan data komposisi gender
    fig = go.Figure()  # Membuat objek plot baru
    # Menambahkan garis untuk jumlah peserta laki-laki
    fig.add_trace(go.Scatter(x=sex_compotation["Year"], y=sex_compotation["Male"], mode='lines+markers', name='Male', line=dict(color='blue')))
    # Menambahkan garis untuk jumlah peserta perempuan
    fig.add_trace(go.Scatter(x=sex_compotation["Year"], y=sex_compotation["Female"], mode='lines+markers', name='Female', line=dict(color='red')))
    # Menambahkan garis untuk jumlah total peserta
    fig.add_trace(go.Scatter(x=sex_compotation["Year"], y=sex_compotation["Total"], mode='lines+markers', name='Total', line=dict(color='white')))
    # Mengatur layout untuk plot garis
    fig.update_layout(title='Number of Participants Per Year', xaxis=dict(title='Year'), yaxis=dict(title='Participant Count'), width=1400, height=800)
    # Menampilkan plot
    return fig


def sex_vil_sport(sport):
    """
    Menghasilkan plot bar grup yang menampilkan komposisi gender peserta Olimpiade dalam suatu olahraga tertentu dari waktu ke waktu.
    
    Args:
        sport (str): Olahraga yang akan dianalisis.
    
    Returns:
        plotly.graph_objects.Figure: Plot bar grup komposisi gender peserta Olimpiade per tahun untuk olahraga tertentu.
    """
    sex_compotation = preprocessing.sex_data_sport(sport)  # Mendapatkan data komposisi gender untuk olahraga tertentu
    fig = go.Figure()  # Membuat objek plot baru
    # Menambahkan bar untuk jumlah peserta laki-laki
    fig.add_trace(go.Bar(x=sex_compotation["Year"], y=sex_compotation["Male"], name='Male', marker_color='blue'))
    # Menambahkan bar untuk jumlah peserta perempuan
    fig.add_trace(go.Bar(x=sex_compotation["Year"], y=sex_compotation["Female"], name='Female', marker_color='red'))
    # Mengatur layout untuk plot bar grup
    fig.update_layout(barmode='group', title=sport, xaxis=dict(title='Year'), yaxis=dict(title='Number of Participants'), width=1400, height=800)
    # Menampilkan plot
    return fig
def plot_height_weight(sport, region):
    """
    Menghasilkan scatter plot yang menampilkan hubungan antara tinggi dan berat badan peserta Olimpiade dalam suatu olahraga dan wilayah tertentu.
    
    Args:
        sport (str): Olahraga yang akan dianalisis.
        region (str): Wilayah yang akan dianalisis.
    
    Returns:
        plotly.graph_objects.Figure: Scatter plot hubungan tinggi dan berat badan peserta Olimpiade.
    """
    data = preprocessing.data_height_vs_weight(sport=sport, region=region)  # Mendapatkan data tinggi dan berat badan
    fig = go.Figure()  # Membuat objek plot baru
    # Menambahkan scatter plot untuk peserta laki-laki
    fig.add_trace(go.Scatter(
        x=data[data['Sex'] == 'M']['Height'],
        y=data[data['Sex'] == 'M']['Weight'],
        mode='markers',
        name='Male',
        marker=dict(color='blue', symbol='circle', size=10)
    ))
    # Menambahkan scatter plot untuk peserta perempuan
    fig.add_trace(go.Scatter(
        x=data[data['Sex'] == 'F']['Height'],
        y=data[data['Sex'] == 'F']['Weight'],
        mode='markers',
        name='Female',
        marker=dict(color='red', symbol='circle', size=10)
    ))
    # Mengatur layout untuk scatter plot
    fig.update_layout(
        title='Height and Weight of Participants',
        xaxis=dict(title='Height'),
        yaxis=dict(title='Weight'),
        width=1400,  # Lebar grafik
        height=800  # Tinggi grafik
    )
    # Mengembalikan objek plot
    return fig

def vil_games_participant():

    data = preprocessing.data_games_count()


    fig = px.line(data, x='Games', y='Participant Count', title='Participant / Athlete Count', 
                width=1400, height=800, markers=True)

    # Customize the layout
    fig.update_layout(
        title={
            'text': 'Participant / Athlete Count',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Games',
        yaxis_title='Count',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Customize the lines and markers
    fig.update_traces(
        line=dict(color='royalblue', width=4),
        marker=dict(color='red', size=10)
    )

    # Show the figure


    return fig
