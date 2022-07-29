#libraries
import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt 
import seaborn as sns
import os
import io
import pandasql as ps
import streamlit as st

st.set_page_config(layout="wide")
os.system("python -m pip install -r requirements.txt")
df=pd.read_csv('dataStori.csv',encoding='utf-8')

st.title("Stori Data Challenge 2021")
st.write("For this challenge we will use a fake credit card dataset that is attached as df.csv, which includes information from a public Kaggle dataset with three added fields: activated_date,last_payment_date and fraud.")
df=df.drop(columns='Unnamed: 0')
st.write(df)
with st.container():
    col_x, col_y ,col_z = st.columns(3)
    with col_x:
        st.write("Information")
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
    with col_y:
        st.write("Describe")
        st.write(df.describe())
        
    with col_z:
        st.write("Nulls")
        st.text(df.isnull().sum())

question=st.selectbox("Question",["Question 1","Question 2","Question 3"])
if question=="Question 1":
    st.write("1.1 Plot an histogram of the balance amount for all the customers.")
    st.write("1.2 Report any structure you find and any hypotheses you have about that structure.")
    st.write("1.3 Report mean and median balance, grouped by year and month of activated_date.")
    plt.title('Clients per balance')
    plt.xlabel('Balance')
    plt.ylabel('AMOUNT OF CLIENTS')
    plt.hist(df.balance,bins=25, range=[0,20000])
    st.write("Histogram of the balance amount for all the customers")
    col_x, col_y ,col_z = st.columns(3)
    with col_x:
        st.pyplot(plt)
    st.write("Insights")
    st.write("More than 70% of users have a balance below the average of 1565")
    st.write("Another piece of information that immediately attracts attention is having so many nulls, especially in the minimum_payments column.")
    st.write("Another data that caught my attention is activated_date since I see 13 null data but it may be because the activation has not yet been done")
    st.write("Something that worries me is seeing only 15% of full payment but we should see the monthly targets to be able to compare it and think about how good or bad it is\n")
    st.write("mean and median balance, grouped by year and month of activated_date")
    mean = df.groupby([pd.DatetimeIndex(df['activated_date']).year,pd.DatetimeIndex(df['activated_date']).month])['balance'].mean()
    median = df.groupby([pd.DatetimeIndex(df['activated_date']).year,pd.DatetimeIndex(df['activated_date']).month])['balance'].median()
    st.write("################## Mean ##################")
    st.write(mean)
    st.write("################## Median ##################")
    st.write(median)
if question == "Question 2":
    st.write("2.1 Report in a table the following information for customers who activated their account and made their last payment during 2020: cust_id (excluding letters), activated_date (in format YYYY-MM), last_payment_date (in format YYYY-MM-DD), cash_advance, credit_limit, and a calculated field of cash_advance as a percentage of credit_limit.")
    df2=df
    df2['activated_date'] = df2['activated_date'].astype('datetime64[ns]')
    df2['activated_date']=df2['activated_date'].dt.to_period('M')
    df2['cust_id']=df2['cust_id'].str.replace('C', '')
    df2['activated_date'] = df2['activated_date'].apply(str)
    request="""select cust_id,activated_date,last_payment_date,cash_advance,credit_limit,cash_advance/credit_limit*100
from df2
"""

    st.write(ps.sqldf(request))
if question == "Question 3":
    df3=df
    df3.dropna(subset=['credit_limit'], inplace=True)
    df3.dropna(subset=['last_payment_date'], inplace=True)
    df3.loc[(df3['minimum_payments'].isnull()==True),'minimum_payments']=df3['minimum_payments'].mean()
    df3.loc[(df3['balance'].isnull()==True),'balance']=df3['balance'].mean()
    df3.loc[(df3['cash_advance'].isnull()==True),'cash_advance']=df3['cash_advance'].mean()
    df3.isnull().sum()

    corr_df = df3.corr(method='pearson')

    plt.figure(figsize=(20, 20))
    sns.heatmap(corr_df, annot=True)
    st.write(ptl)
