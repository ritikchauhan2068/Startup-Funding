import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide',page_title='start_up_analysis')



df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')
    #Total invested amount
    total = round(df['amount'].sum())
    #max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1)[0]
    st.metric('Total',str(total) + 'Cr')
    st.metric('Max',str(max_funding) + 'Cr')
    #average ticket size
    average_funding = df.groupby('startup')['amount'].sum().mean()
    st.metric('Average',str(round(average_funding)) + 'Cr')
    #Total funded startups
    num_startups = df['startup'].nunique()
    st.metric('Funded Startups',num_startups)
    st.header('Month On Month Graph')
    temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig3)


def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investments of the investor
    last_5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_5_df)
    col1,col2 = st.columns(2)
    with col1:

        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().head()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on Year Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)
    st.pyplot(fig2)






#st.dataframe(df)
st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
    btn0 = st.sidebar.button('Show Overall Analysis')
    if btn0:
        load_overall_analysis()
elif option == 'StartUp':
    selected_investor = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Start up Details')
    if btn1:
        load_investor_details(selected_investor)

else:
    selected_investor = st.sidebar.selectbox('Select StartUp',set(sorted(df['investors'].str.split(',').sum())))
    set(sorted(df['investors'].str.split(',').sum()))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2 :
        load_investor_details(selected_investor)

