import gzip
import json
import os
import re
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


def extract_listings(user_input, count):

    url = f"https://data.insideairbnb.com/united-states/ny/new-york-city/{user_input}/data/listings.csv.gz"
    data_folder = "data"
    local_gz_path = os.path.join(data_folder, "listings.csv.gz")
    output_csv_path = os.path.join(data_folder, f"listings_{count}.csv")

    os.makedirs(data_folder, exist_ok=True)

    print("Downloading ", user_input)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_gz_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded: {local_gz_path}")
    else:
        print("Failed to download the file.")
        response.raise_for_status()

    with gzip.open(local_gz_path, "rb") as gz_file:
        with open(output_csv_path, "wb") as csv_file:
            shutil.copyfileobj(gz_file, csv_file)

    print(f"File extracted and saved as: {output_csv_path}")
    os.remove(local_gz_path)


def extract_reviews(user_input, count):

    url = f"https://data.insideairbnb.com/united-states/ny/new-york-city/{user_input}/data/reviews.csv.gz"
    data_folder = "data"
    local_gz_path = os.path.join(data_folder, "reviews.csv.gz")
    output_csv_path = os.path.join(data_folder, f"reviews_{count}.csv")

    os.makedirs(data_folder, exist_ok=True)

    print("Downloading ", user_input)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_gz_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded: {local_gz_path}")
    else:
        print("Failed to download the file.")
        response.raise_for_status()

    with gzip.open(local_gz_path, "rb") as gz_file:
        with open(output_csv_path, "wb") as csv_file:
            shutil.copyfileobj(gz_file, csv_file)

    print(f"File extracted and saved as: {output_csv_path}")
    os.remove(local_gz_path)


ip_dates = ['2024-01-05', '2024-02-06', '2024-03-07', '2024-04-06', '2024-05-03',
            '2024-06-04', '2024-07-05', '2024-08-05', '2024-09-04', '2024-10-04', '2024-11-04']
count = 0

for user_input in ip_dates:
    count += 1
    extract_listings(user_input, count)
    extract_reviews(user_input, count)

data_folder = "data"
all_files = os.listdir(data_folder)

listings_files = sorted([f for f in all_files if f.startswith("listings_") and f.endswith(".csv")],
                        key=lambda x: int(x.split('_')[1].split('.')[0]))
reviews_files = sorted([f for f in all_files if f.startswith("reviews_") and f.endswith(".csv")],
                       key=lambda x: int(x.split('_')[1].split('.')[0]))


def merge_csv_files(file_list, output_filename):
    merged_df = pd.DataFrame()
    for file in file_list:
        file_path = os.path.join(data_folder, file)
        df = pd.read_csv(file_path)
        merged_df = pd.concat([merged_df, df], ignore_index=True)
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    merged_df.to_csv(os.path.join(data_folder, output_filename), index=False)
    print(f"Merged file saved as: {output_filename}")


print("Merging listings files...")
merge_csv_files(listings_files, "airbnblistings_2024.csv")

print("Merging reviews files...")
merge_csv_files(reviews_files, "airbnbreviews_2024.csv")

print("All files merged and individual files deleted.")
