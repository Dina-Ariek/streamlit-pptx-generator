import pandas as pd
# import streamlit as st
import pandas as pd
from pptx import Presentation
from io import BytesIO
from pptx.util import Pt
import calendar

def load_csv(file_path):
    """
    Load data fact_instagram_post dari file CSV.
    :param file_path: path ke file fact_instagram_post.csv
    :return: DataFrame
    """
    df = pd.read_csv(file_path)
    return df
def ig_monthly(df):
# Tambah kolom 'month' untuk agregasi bulanan
    df['month'] = pd.to_datetime(df['post_date']).dt.to_period('M').astype(str)

    # Hitung metrik agregasi bulanan
    monthly_agg = df.groupby('month').agg({
        'profile_reach': 'sum',
        'profile_visit': 'sum',
        'new_followers': 'sum',
        'view_count': 'sum',
        'like_count': 'sum',
        'comment_count': 'sum',
        'share_count': 'sum',
        'saved_count': 'sum',
        'followers': 'mean'  # rata-rata follower dalam sebulan
    }).reset_index()

    # Tambah metrik turunan
    monthly_agg['growth'] = monthly_agg['new_followers']
    monthly_agg['reach'] = monthly_agg['profile_reach']
    monthly_agg['engagement'] = monthly_agg['like_count'] + monthly_agg['comment_count'] + monthly_agg['share_count'] + monthly_agg['saved_count']

    monthly_agg['er_reach_percent'] = (monthly_agg['engagement'] / monthly_agg['reach']) * 100
    monthly_agg['er_followers_percent'] = (monthly_agg['engagement'] / monthly_agg['followers']) * 100

    # Susun kolom sesuai format
    datamart = monthly_agg[[
        'month', 'profile_reach', 'profile_visit', 'growth', 'reach', 'engagement',
        'like_count', 'comment_count', 'share_count', 'saved_count',
        'er_reach_percent', 'er_followers_percent'
    ]]
    return datamart

# combined_datamart = pd.concat([datamart_ig, datamart_tiktok], ignore_index=True)
