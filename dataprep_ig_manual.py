import pandas as pd

# Load file Excel
df = pd.read_excel("data/data crawling manual.xlsx", sheet_name="ig", header=0)
df = df[df['username'] == 'vinfast.indonesia']
# Mapping bulan Indonesia ke Inggris
bulan_mapping = {
    "Januari": "January",
    "Februari": "February",
    "Maret": "March",
    "April": "April",
    "Mei": "May",
    "Juni": "June",
    "Juli": "July",
    "Agustus": "August",
    "September": "September",
    "Oktober": "October",
    "November": "November",
    "Desember": "December"
}

# Pastikan kolom post_date dalam format string
df['post_date'] = df['post_date'].astype(str)

# Replace bulan Indonesia ke Inggris
for indo, eng in bulan_mapping.items():
    df['post_date'] = df['post_date'].str.replace(indo, eng, regex=False)

# Convert ke datetime dengan format yang tepat
df['post_date'] = pd.to_datetime(df['post_date'], format="%d %B %Y")

# Tambahan: kolom bulan (optional)
df['month'] = df['post_date'].dt.to_period('M').astype(str)

# Cek hasil
print(df[['post_date', 'month']].head())

# Convert tanggal
df['post_date'] = pd.to_datetime(df['post_date'])
df['month'] = df['post_date'].dt.to_period('M').astype(str)

# Hitung engagement
df['like_count'] = df['like_count'].fillna(0)
df['comment_count'] = df['comment_count'].fillna(0)
df['share_count'] = df['share_count'].fillna(0)
df['saved_count'] = df['saved_count'].fillna(0)
df['engagement'] = df['like_count'] + df['comment_count'] + df['share_count'] + df['saved_count']
df.to_csv("data/fact_instagram_post.csv", index=False, encoding="utf-8-sig")
# Group by bulan
df_monthly = df.groupby('month').agg({
    'post_id': 'count',
    'total follower': 'last',
    'view_count': 'sum',
    'engagement': 'sum',
    'like_count': 'sum',
    'comment_count': 'sum',
    'share_count': 'sum',
    'saved_count': 'sum'
}).reset_index()

# Rename
df_monthly = df_monthly.rename(columns={
    'post_id': 'total_post',
    'total follower': 'followers',
    'view_count': 'reach'
})

# Tambah growth
df_monthly['growth'] = df_monthly['followers'].diff().fillna(0)

# Tambah kolom kosong & channel
df_monthly['profile_visit'] = 0
df_monthly['profile_reach'] = 0
df_monthly['channel'] = 'Instagram'
pd.set_option('display.max_columns', None)
print(df_monthly)
# Simpan DataFrame ke file CSV
df_monthly.to_csv("data/datamart_ig.csv", index=False, encoding="utf-8-sig")
