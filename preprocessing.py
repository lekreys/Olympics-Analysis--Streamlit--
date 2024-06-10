import pandas as pd
import numpy as np
import helper
import seaborn as sns

def dataset():
    """
    Memuat dan menggabungkan dataset atlet dan wilayah.

    Returns:
    DataFrame: Dataset yang digabungkan.
    """
    athlete_url = "data/athlete_events.csv" 
    noc_url = "data/noc_regions.csv"

    athlete = pd.read_csv(athlete_url)
    regions = pd.read_csv(noc_url)

    dataset = athlete.merge(regions , how="left" , on="NOC")

    return dataset

def clear_data():
    """
    Membersihkan dataset dengan menghapus duplikat dan kolom yang tidak perlu.

    Returns:
    DataFrame: Dataset yang sudah dibersihkan.
    """
    df = dataset()
    df_no_dup = df.drop_duplicates()
    df = df_no_dup.drop("notes" , axis=1)

    return df

def medal_data(dataframe):
    """
    Menghitung jumlah total medali yang dimenangkan oleh setiap wilayah.

    Args:
    dataframe (DataFrame): DataFrame input yang berisi data acara atlet.

    Returns:
    DataFrame: DataFrame dengan total jumlah medali untuk setiap wilayah.
    """
    df = dataframe
    dummies_data = pd.get_dummies(df , columns=["Medal"] , prefix="medal")

    medall_ttly = dummies_data.drop_duplicates(subset=["Name" ,"Year" , "Sport" , "Event" , "NOC" , "Season"])
    medals = medall_ttly.groupby("region")[["medal_Gold"	,"medal_Silver" , "medal_Bronze"]].sum()
    medals["total"] = medals["medal_Silver"] + medals["medal_Bronze"] + medals["medal_Gold"]
    all_medals = medals.sort_values(by=["total"] , ascending=False).reset_index()
    all_medals.columns = ["Region" , "Gold" , "Silver" , "Bronze" , "Total"]

    return all_medals

def subset_and_display_medal(region="Overall", season="All Season", from_year=helper.year_scale()[0], to_year=helper.year_scale()[1]):
    """
    Menghasilkan subset dataset berdasarkan kriteria yang ditentukan dan menampilkan jumlah medali untuk setiap wilayah.

    Args:
    region (str): Wilayah untuk menyaring dataset. Defaultnya adalah "Overall".
    season (str): Musim untuk menyaring dataset. Defaultnya adalah "All Season".
    from_year (int): Tahun awal rentang. Defaultnya adalah tahun minimum dalam dataset.
    to_year (int): Tahun akhir rentang. Defaultnya adalah tahun maksimum dalam dataset.

    Returns:
    DataFrame: DataFrame yang menampilkan jumlah medali untuk setiap wilayah dalam filter yang ditentukan.
    """
    dataset = clear_data()
    dataset = dataset[np.logical_and(dataset["Year"] >= from_year, dataset["Year"] <= to_year)]

    if season == "All Season":
        data = dataset.copy()
    else:
        data = dataset[dataset["Season"] == season]

    newdata = medal_data(data)

    if region == "All":
        display_medal = newdata.copy()
    else:
        display_medal = newdata[newdata["Region"] == region]

    return display_medal

def plot_data():
    """
    Menghitung total medali yang dimenangkan setiap tahun dan setiap wilayah.

    Returns:
    DataFrame: DataFrame yang menampilkan total medali untuk setiap tahun dan wilayah.
    """
    data = clear_data()
    dummies = pd.get_dummies(data , columns=["Medal"] , prefix="medal")

    medall_year = dummies.drop_duplicates(subset=["Name" ,"Year" , "Sport" , "Event" , "NOC" , "Season"])

    total = medall_year.groupby(["Year" , "region"])[["medal_Gold"	,"medal_Silver" , "medal_Bronze"]].sum()
    dataper_y = total.reset_index()

    dataper_y["total"] = dataper_y["medal_Gold"] + dataper_y["medal_Silver"] + dataper_y["medal_Bronze"]
    return dataper_y


def country_game():
    """
    Menghitung jumlah permainan Olimpiade yang diadakan di setiap negara.

    Returns:
    DataFrame: DataFrame yang menampilkan jumlah permainan Olimpiade untuk setiap negara.
    """
    data = clear_data()

    games_num = data.groupby(["NOC"])["Games"].count().reset_index()
    games_num = games_num.sort_values(by="Games" , ascending=False , ignore_index=True)
    return games_num

def participant_data():
    """
    Menghitung jumlah negara yang berpartisipasi dalam Olimpiade setiap tahun.

    Returns:
    DataFrame: DataFrame yang menampilkan jumlah negara yang berpartisipasi setiap tahun.
    """
    data = clear_data()

    participant  = data.groupby(["Year"])["region"].nunique().to_frame().reset_index().sort_values(by="Year")
    participant.columns = ["Year" , "number country"]
    return participant

def city_data():
    """
    Menghitung jumlah permainan Olimpiade yang diadakan di setiap kota setiap tahun.

    Returns:
    DataFrame: DataFrame yang menampilkan jumlah permainan Olimpiade untuk setiap kota setiap tahun.
    """
    data = clear_data()
    
    city = data.groupby("Year")["City"].unique()
    uniq_city = city.to_frame().reset_index()

    city_dict = {}
    all_city = []

    for i , val in uniq_city.iterrows():
        
        for k in val["City"]:

            all_city.append(k)
            
            if ( k in city_dict.keys()):
                city_dict[k] = city_dict[k] + 1
            else:
                city_dict[k] = 1
    city_pd = pd.DataFrame({"city" : [i for i in city_dict.keys()] , "num" : [city_dict[i] for i in city_dict.keys()]})

    return city_pd

        
def season_data():
    """
    Menghitung jumlah permainan Olimpiade yang diadakan dalam setiap musim setiap tahun.

    Returns:
    DataFrame: DataFrame yang menampilkan jumlah permainan Olimpiade untuk setiap musim setiap tahun.
    """
    data = clear_data()

    season = data.groupby("Year")["Season"].unique().to_frame().reset_index()
    season_dict = {}
    all_season = []

    for i , val in season.iterrows():
        
        for k in val["Season"]:

            all_season.append(k)
            
            if ( k in season_dict.keys()):
                season_dict[k] = season_dict[k] + 1
            else:
                season_dict[k] = 1

    season_pd = pd.DataFrame({"season" : [i for i in season_dict.keys()] , "num" : [season_dict[i] for i in season_dict.keys()]})

    return season_pd

def sport_data_count():
    """
    Menghitung jumlah cabang olahraga yang berpartisipasi setiap tahun.

    Returns:
    tuple: Tuple berisi DataFrame yang menampilkan jumlah cabang olahraga yang berpartisipasi setiap tahun, dan DataFrame yang menampilkan daftar cabang olahraga yang berpartisipasi setiap tahun.
    """
    data = clear_data()
    sport_data = data.groupby(["Year"])['Sport'].nunique().to_frame().reset_index()
    sport_data_value = data.groupby(["Year"])['Sport'].unique().to_frame().reset_index()

    return sport_data, sport_data_value

def athlete_per_country_data(sort = "Region" , ascending_pram = True):

    data = clear_data()
    athlete_country = data.groupby("region")["Name"].nunique().to_frame().reset_index()
    athlete_country.columns = ["Region" , "Total Athlete"]
    final = athlete_country.sort_values(ascending=ascending_pram , by=sort).reset_index().drop("index" , axis=1)

    return final

def total_athlete(fromm, too, country, sport):
    """
    Memfilter data atlet berdasarkan rentang tahun, negara, dan cabang olahraga.

    Args:
    fromm (int): Tahun awal rentang.
    too (int): Tahun akhir rentang.
    country (str): Negara yang ingin difilter.
    sport (str): Cabang olahraga yang ingin difilter.

    Returns:
    DataFrame: DataFrame yang berisi atlet yang sesuai dengan kriteria filtrasi.
    """
    data = clear_data()

    subset_year = data[np.logical_and(data["Year"] >= fromm, data["Year"] <= too)]

    if country == "All":
        after_country = subset_year.copy()
    else:
        after_country = subset_year[subset_year["region"] == country]

    if sport == "All":
        after_sport = after_country.copy()
    else:
        after_sport = after_country[after_country["Sport"] == sport]

    return after_sport

def top_medal():
    """
    Menghitung 20 atlet teratas berdasarkan jumlah total medali yang dimenangkan.

    Returns:
    DataFrame: DataFrame yang berisi 20 atlet teratas berdasarkan jumlah total medali yang dimenangkan.
    """
    athlete = clear_data()

    athlete = pd.get_dummies(athlete, prefix="medal", columns=["Medal"])
    athlete["Total Medal"] = athlete["medal_Bronze"] + athlete["medal_Gold"] + athlete["medal_Silver"]
    total_medal_athlete = athlete.groupby(["Name", "Sport"])[["medal_Gold", "medal_Silver", "medal_Bronze","Total Medal"]].sum().sort_values(ascending=False, by="Total Medal").reset_index()

    return total_medal_athlete.head(20)

def data_sport_top(sport, too):
    """
    Memfilter data atlet berdasarkan cabang olahraga dan tahun, kemudian menghitung 30 atlet teratas berdasarkan jumlah total medali yang dimenangkan.

    Args:
    sport (str): Cabang olahraga yang ingin difilter.
    too (int): Tahun akhir rentang.

    Returns:
    DataFrame: DataFrame yang berisi 30 atlet teratas berdasarkan jumlah total medali yang dimenangkan.
    """
    data = clear_data()
    medall_ttly = pd.get_dummies(data, prefix="medal", columns=["Medal"])
    medall_ttly["Total Medal"] = medall_ttly["medal_Bronze"] + medall_ttly["medal_Gold"] + medall_ttly["medal_Silver"]
    selecet_sport = medall_ttly[np.logical_and(medall_ttly["Sport"] == sport, medall_ttly["Year"] <= too)]
    group_select = selecet_sport.groupby(["Name", "Sport"])[["medal_Gold", "medal_Silver", "medal_Bronze","Total Medal"]].sum().sort_values(ascending=False, by="Total Medal").reset_index()

    return group_select.head(30)

def sex_data():
    """
    Menghitung jumlah peserta Olimpiade berdasarkan jenis kelamin setiap tahun.

    Returns:
    DataFrame: DataFrame yang menampilkan jumlah peserta Olimpiade berdasarkan jenis kelamin setiap tahun.
    """
    data = clear_data()
    dummies_s = pd.get_dummies(data, columns=["Sex"], prefix="Type")
    sex_compotation = dummies_s.groupby("Year")[["Type_M", "Type_F"]].sum().reset_index()
    sex_compotation.columns = ["Year", "Male", "Female"]
    sex_compotation["Total"] = sex_compotation["Male"] + sex_compotation["Female"]
    return sex_compotation

def sex_data_sport(sport):
    """
    Menghitung jumlah peserta Olimpiade berdasarkan jenis kelamin setiap tahun untuk cabang olahraga tertentu.

    Args:
    sport (str): Cabang olahraga yang ingin difilter.

    Returns:
    DataFrame: DataFrame yang menampilkan jumlah peserta Olimpiade berdasarkan jenis kelamin setiap tahun untuk cabang olahraga tertentu.
    """
    data = clear_data()
    data = data[data["Sport"] == sport]
    dummies_s = pd.get_dummies(data, columns=["Sex"], prefix="Type")
    sex_compotation = dummies_s.groupby("Year")[["Type_M", "Type_F"]].sum().reset_index()
    sex_compotation.columns = ["Year", "Male", "Female"]
    sex_compotation["Total"] = sex_compotation["Male"] + sex_compotation["Female"]
    return sex_compotation

def data_height_vs_weight(sport, region):
    """
    Memfilter data atlet berdasarkan cabang olahraga dan wilayah.

    Args:
    sport (str): Cabang olahraga yang ingin difilter.
    region (str): Wilayah yang ingin difilter.

    Returns:
    DataFrame: DataFrame yang berisi data atlet sesuai dengan kriteria filtrasi.
    """
    data = clear_data()

    if region == "All":
        data = data.copy()
    else:
        data = data[data["region"] == region]

    sport_subset = data[data["Sport"] == sport]

    return sport_subset

def data_games_count():
    """
    Menghitung jumlah atlet yang berpartisipasi dalam setiap edisi Olimpiade.

    Returns:
    DataFrame: DataFrame yang menampilkan jumlah atlet yang berpartisipasi dalam setiap edisi Olimpiade.
    """
    data = clear_data()
    games_count = data.groupby("Games")["Name"].count()
    games_count_df = games_count.to_frame().reset_index()
    games_count_df.columns = ["Games", "Participant Count"]

    return games_count_df
