import pandas as pd
import matplotlib.pyplot as plt



def import_data (path):
    return pd.read_csv(path)

def drop_unnecessary (df):
    '''
    information on the dataset can be found here https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243/about_data
    First we delete unnecessary columns
    - X_COORD_CD/Y_COORD_CD/HADEVELOPT/BORO_NM/ADDR_PCT_CD/STATION_NAME/TRANSIT_DISTRICT unnecessary as we use coordinates for location data
    - LOC_OF_OCCUR_DESC not relevant for us if crime happened on the outside/inside
    - JURIS_DESC/JURISDICTION_CODE not relevant for us which police department handles it
    - CMPLNT_NUM no id is needed for our purposes
    - PREM_TYP_DESC not relevant what type of premise
    - PARKS_NM park name not relevant since coordinates are used for locations
    - CMPLNT_FR_TM/CMPLNT_TO_TM date is enough for our purposes
    - HOUSING_PSA/PATROL_BORO/SUSP_AGE_GROUP/SUSP_SEX/SUSP_RACE/VIC_AGE_GROUP/VIC_RACE/VIC_SEX are not relevant
    - RPT_DT/CMPLNT_TO_DT as we are only interested on when the crime was taken place not when it was reported/finished
    (((- KY_CD not usable as no description provided and no decent mapping was found)))
    '''
    df = df.drop(columns=
                                 ['X_COORD_CD', 'Y_COORD_CD', 'LOC_OF_OCCUR_DESC', 'JURIS_DESC', 'HADEVELOPT',
                                  'CMPLNT_NUM', 'PREM_TYP_DESC', 'BORO_NM', 'PARKS_NM', 'CMPLNT_TO_TM', 'CMPLNT_FR_TM',
                                  'ADDR_PCT_CD', 'HOUSING_PSA','JURISDICTION_CODE', 'PATROL_BORO', 'STATION_NAME',
                                  'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX', 'TRANSIT_DISTRICT', 'VIC_AGE_GROUP', 'VIC_RACE',
                                  'VIC_SEX', 'RPT_DT', 'CMPLNT_TO_DT'])
    return df

def drop_unnecessary_shootings(df):
    '''
    - INCIDENT_KEY/OCCUR_TIME not relevant
    - BORO/LOC_OF_OCCUR_DESC/PRECINCT/JURISDICTION_CODE/LOC_CLASSFCTN_DESC/LOCATION_DESC location only via coordinates
    - PERP_AGE_GROUP/PERP_SEX/PERP_RACE/VIC_AGE_GROUP/VIC_SEX/VIC_RACE not relevant as we will be aggregating the number of shootings later
    '''
    df = df.drop(columns=
                 ['OCCUR_TIME', 'INCIDENT_KEY', 'LOC_OF_OCCUR_DESC', 'BORO', 'LOCATION_DESC', 'LOC_CLASSFCTN_DESC',
                  'JURISDICTION_CODE', 'PRECINCT', 'PERP_AGE_GROUP', 'PERP_SEX', 'PERP_RACE', 'VIC_AGE_GROUP', 'VIC_RACE','VIC_SEX'])
    return df

def type_date_columns (df):
    column_names = list(df.columns)
    for column in column_names:
        if column.endswith('DT') or column.endswith('DATE'):
            df[column] = pd.to_datetime(df[column], errors='coerce', format='%m/%d/%Y')
    return df

def drop_na_location (df, column_names):
    for col in column_names:
        df = df.dropna(subset=[col])
    return df

def occurences_per_date_column (df, column_name):
    temp = df.copy()
    temp['year_month'] = temp[column_name].dt.to_period('M')  # Convert to 'YYYY-MM' format
    monthly_counts = temp['year_month'].value_counts().sort_index()  # Count and sort by time

    plt.figure(figsize=(12, 6))
    monthly_counts.plot(kind='bar', color='skyblue')
    plt.title(f'Occurrences per Month Over the Years for {column_name}', fontsize=16)
    plt.xlabel('Month-Year', fontsize=12)
    plt.ylabel('Number of Occurrences', fontsize=12)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def count_unique_values (df, column_name):
    # Count the occurrences of each unique value
    counts = df[column_name].value_counts()

    # Plot the top N most frequent values for better visualization
    top_n = 20  # Adjust N as needed
    counts.head(top_n).plot(kind='bar', figsize=(12, 6), color='skyblue', edgecolor='black')

    plt.title(f'Count unique values for {column_name}'.format(top_n), fontsize=16)
    plt.xlabel(f'{column_name}', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def id_off (df, column_name_one, column_name_two):
    # Check the unique combinations of KY_CD and OFNS_DESC
    unique_combinations = df[[column_name_one, column_name_two]].drop_duplicates()

    # Count how many unique combinations there are
    num_unique_combinations = unique_combinations.shape[0]
    print(f'Number of unique combinations of {column_name_one} and {column_name_two}: {num_unique_combinations}')

    # Check if the number of unique KY_CD values matches the number of unique OFNS_DESC values
    num_unique_kcd = df['KY_CD'].nunique()
    num_unique_ofns_desc = df['OFNS_DESC'].nunique()
    print(f'Number of unique {column_name_one} values: {num_unique_kcd}')
    print(f'Number of unique {column_name_two} values: {num_unique_ofns_desc}')

def limit_date_range (df, column_name, year):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')

    df_filtered = df[df[column_name].dt.year >= year]

    return df_filtered

# file_path: path to csv
# beginning_year: year that should start being taken to account for analysis
def handle_police_data (file_path, beginning_year):
    (pd.set_option('display.max_columns', None))

    df = import_data(file_path)
    df = drop_unnecessary(df)
    df = type_date_columns(df)

    #occurences_per_date_column(df, 'CMPLNT_FR_DT')

    #count_unique_values(df, 'OFNS_DESC')
    # looking at this graph this seems to be the most relevant predictor (later it would be wise to analyze if KY_CD and LAW_CAT_CD are needed)
    #count_unique_values(df, 'KY_CD')
    # I suspect that KY_CD is the id of OFNS_DESC and therefore we would only need one; we check it:
    #id_off(df, 'KY_CD', 'OFNS_DESC')
    # As we can see by the results this is not the case
    # As I do not find a good description for KY_CD I will drop it as it does not convey information in this state
    df = df.drop('KY_CD', axis = 1)

    #count_unique_values(df, 'PD_CD')
    #count_unique_values(df, 'PD_DESC')
    # PD_CD and PD_DESC should be kept for now and will be looked at later for the machine learning model

    df = limit_date_range(df, "CMPLNT_FR_DT", beginning_year)
    #occurences_per_date_column(df, 'CMPLNT_FR_DT')

    #now lets take a look at NaN values
    nan_count_per_column = df.isna().sum()
    print(nan_count_per_column)
    # first we drop all columns without GPS Data as they are useless for us:
    df = drop_na_location(df, ['Latitude', 'Longitude', 'Lat_Lon', 'New Georeferenced Column'])
    # As PD_CD has a lot of NaN values we drop it
    df = df.drop('PD_CD', axis = 1)
    #nan_count_per_column = df.isna().sum()
    #print(nan_count_per_column)

    print(df.head())
    print(df.info())
    return df

def handle_shooting_data (path, beginning_year):
    (pd.set_option('display.max_columns', None))
    df = import_data(path)
    df = type_date_columns(df)
    df = drop_unnecessary_shootings(df)
    df = drop_na_location(df, ['X_COORD_CD', 'Y_COORD_CD', 'Latitude', 'Longitude', 'New Georeferenced Column'])

    #nan_count_per_column = df.isna().sum()
    #print(nan_count_per_column)

    print(df.head())
    print(df.info())
    return df

# For police data
#file_path = 'police_data/NYPD_Complaint_Data_Current__Year_To_Date__20241223.csv'
#df = handle_police_data(file_path, 2022)

#For shootings data:
#file_path = 'shootings/NYPD_Shooting_Incident_Data__Year_To_Date__20241227.csv'
#df = handle_shooting_data(file_path, 2022)