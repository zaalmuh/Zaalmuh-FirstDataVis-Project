import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency   
sns.set(style='dark')

# membuat create_bycity_df
def create_bycity_df(df):
    bycity_df = df.groupby('customer_city').agg({
    'customer_id': 'count'
}).sort_values(by='customer_id')

    return bycity_df

def create_bypayment_df(df):
    bypayment_df = {'payment_type': df['payment_type'].value_counts().values, 
    'index': df['payment_type'].value_counts().index}
    return bypayment_df

def create_byproduct_df(df):
    byproduct_df = df.groupby('product_category_name_english').agg({
    'order_id': 'count'
}).sort_values(by='order_id', ascending=False)

    return byproduct_df

def create_byreview_df(df):
    byreview_df = df.groupby(by='product_category_name_english').agg({
    'review_score': 'mean'
}).sort_values(by='review_score', ascending=False)
    return byreview_df

# membuat create_rfm_df
def create_rfm_df(df):
    rfm_df = df.groupby('customer_id', as_index=False).agg({
        'order_purchase_date': 'max',
        'order_id': 'nunique',
        'price': 'sum'
    })
    rfm_df.columns = ['customer_id', 'max_order_timestamp', 'frequency', 'monetary']

    rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date
    recent_date = df['order_purchase_date'].dt.date.max()
    rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date - x).days)
    rfm_df.drop('max_order_timestamp',axis=1, inplace=True)

    return rfm_df

# Read data
all_df = pd.read_csv('./Data/all_df.csv')
# # Mengurutkan dataframe berdasarkan order'order_purchase_date'
all_df.sort_values(by='order_purchase_date', inplace=True)
all_df.reset_index(inplace=True)
all_df['order_purchase_date'] = pd.to_datetime(all_df['order_purchase_date'])

# Membuat komponen filter
min_date =  all_df['order_purchase_date'].min()
max_date = all_df['order_purchase_date'].max()

with st.sidebar:

    # Mengambil start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        help='Rentang waktu Yang Diinginkan'
    )

main_df = all_df[(all_df['order_purchase_date'] >= str(start_date)) & (all_df['order_purchase_date'] <= str(end_date))]
bycity_df = create_bycity_df(main_df)
bypayment_df = create_bypayment_df(main_df)
rfm_df = create_rfm_df(main_df)
byproduct_df = create_byproduct_df(main_df)
byreview_df = create_byreview_df(main_df)

st.header('Brazilian E-Commerce Dashboard :sparkles:')

st.write("""
            Welcome to Brazilian E-Commerce Dashboard, for information about dataset source:
         """)
st.page_link('https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce', label="Sumber Dataset")
st.subheader("Best & Worst Product Category Based on Sales")
 
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(35, 40))

colors = ["#0044CC", "#808080" , "#808080", "#808080", "#808080", "#808080", "#808080", "#808080", "#808080", "#808080" ]
 
sns.barplot(x="order_id", y="product_category_name_english", data=byproduct_df.head(10), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Product Category Based on Sales", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_id", y="product_category_name_english", data=byproduct_df.sort_values(by="order_id", ascending=True).head(10), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].set_title("Worst Product Category Based on Sales", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.subheader("Cities with the Most Customers")
 
fig, ax = plt.subplots(figsize=(20, 10))
 
sns.barplot(y="customer_id", 
            x="customer_city",
        data=bycity_df.sort_values(by="customer_id", ascending=False).head(5),
        palette=colors,
        ax=ax
    )
ax.set_title("Cities with the Most Customers", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.subheader("Customer Demographics by Payment Type")

fig, ax = plt.subplots(figsize=(20, 10))
pieColors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

ax.pie(bypayment_df['payment_type'], labels=bypayment_df['index'], autopct='%1.1f%%', startangle=90, colors=pieColors)
ax.set_title("Customer Demographics by Payment Type", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)



st.subheader("Best & Worst Product Based on Review Score")
 
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(35, 40))
 
colors = ["#0044CC", "#808080" , "#808080", "#808080", "#808080"]
 
sns.barplot(y='product_category_name_english', x='review_score', data=byreview_df.head(5), palette=colors, ax=ax[0])
ax[0].set_xlabel("Score (1-5)", fontsize=30)
ax[0].set_ylabel(None)
ax[0].set_title("Best Rated Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
# rotate x axis
 
sns.barplot(y='product_category_name_english', x='review_score', data=byreview_df.sort_values(by="review_score", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_xlabel("Score (1-5)", fontsize=30)
ax[1].set_ylabel(None)
ax[1].set_title("Worst Rated Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = f'R${rfm_df.monetary.mean():,.2f}'.replace('.',',')
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(35, 60))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(x="recency", y="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(x="frequency", y="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(x="monetary", y="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)
 
st.caption('Copyright (c) Aliza for Dicoding Project 2024, Dataset by Olist (Kaggle)')