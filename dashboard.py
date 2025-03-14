import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')


def load_data():
    file_path = "./all_data.csv"  # Pastikan path ini benar
    return pd.read_csv(file_path, parse_dates=["order_purchase_timestamp"])

df = load_data()

df.sort_values(by="order_date", inplace=True)
df.reset_index(drop=True, inplace=True)

# Sidebar - Filter by Date Range
min_date = df["order_date"].min()
max_date = df["order_date"].max()

with st.sidebar:
    st.image("https://i.pinimg.com/originals/65/dd/2f/65dd2f283db26ce78dd6ab61a489b90e.jpg")
    start_date, end_date = st.date_input("Rentang Waktu", min_value=min_date, max_value=max_date, value=[min_date, max_date])

df_filtered = df[(df["order_date"] >= pd.to_datetime(start_date)) & (df["order_date"] <= pd.to_datetime(end_date))]

# Daily Orders Analysis
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_date').agg({"order_id": "nunique"}).reset_index()
    daily_orders_df.rename(columns={"order_id": "order_count"}, inplace=True)
    return daily_orders_df

daily_orders_df = create_daily_orders_df(df_filtered)

st.header('Olist E-Commerce Dashboard :sparkles:')
st.subheader('Daily Orders')

# Display Total Orders
col1, col2 = st.columns(2)
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)

# Line Chart of Daily Orders
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_orders_df["order_date"], daily_orders_df["order_count"], marker='o', linewidth=2, color="#90CAF9")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Orders")
ax.set_title("Daily Order Count")
st.pyplot(fig)


# Simulasi Data dari Sumber yang Diberikan
customers_data = {
    "customer_city": [
        "sao paulo", "rio de janeiro", "belo horizonte", "brasilia", "curitiba",
        "campinas", "porto alegre", "salvador", "guarulhos", "sao bernardo do campo"
    ],
    "customer_count": [15540, 6882, 2773, 2131, 1521, 1444, 1379, 1245, 1189, 938]
}

customer_state_data = {
    "customer_state": ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "DF", "ES", "GO"],
    "state_count": [41746, 12852, 11635, 5466, 5045, 3637, 3380, 2140, 2033, 2020]
}

payment_type_data = {
    "payment_type": ["credit_card", "boleto", "voucher", "debit_card"],
    "count": [76795, 19784, 5769, 1529]
}

# DataFrame
customers_df = pd.DataFrame(customers_data)
customer_state_df = pd.DataFrame(customer_state_data)
payment_type_df = pd.DataFrame(payment_type_data)

# Judul Dashboard
st.title("Analisis E-Commerce Dataset")

# --- Pelanggan per Kota ---
st.subheader("Top 10 Kota dengan Pelanggan Terbanyak")
st.write(customers_df)
st.bar_chart(customers_df.set_index("customer_city"))

# --- Pelanggan per State ---
st.subheader("Jumlah Pelanggan per State")
st.write(customer_state_df)
st.bar_chart(customer_state_df.set_index("customer_state"))

# --- Pembayaran ---
st.subheader("Distribusi Metode Pembayaran")
fig, ax = plt.subplots()
ax.pie(payment_type_df["count"], labels=payment_type_df["payment_type"], autopct='%1.1f%%', colors=["skyblue", "lightcoral", "lightgreen", "orange"])
ax.set_title("Metode Pembayaran")
st.pyplot(fig)

# --- Kesimpulan ---
st.subheader("Kesimpulan")
st.write("Data ini menunjukkan laporan daily orders serta distribusi pelanggan berdasarkan kota dan state dan juga metode pembayaran yang paling sering digunakan dalam e-commerce ini.")


st.caption('Data Source: Olist Brazilian E-Commerce https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce')


st.caption('Copyright (c) ')
