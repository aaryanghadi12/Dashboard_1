import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('startup_cleaned.csv')
st.set_page_config(layout='wide',page_title='StartUP Analysis')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
#st.dataframe(df)

st.sidebar.title('Startup Funding Analysis')

opt=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

def load_investor_details(investor):

    st.title(investor)
    last5_df=df[df['investors'].str.contains(investor,na=False)].head()[['date','Startup','Vertical','City  Location','round','amount']]

    st.title('Most recent invenstment')
    st.dataframe(last5_df)


    col1,col2,col3=st.columns(3)
    with col1:
        big_series=df[df['investors'].str.contains(investor,na=False)].groupby('Startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor,na=False)].groupby('Vertical')['amount'].sum().sort_values()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels= vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)


    with col3:
        st.subheader('According to the City')
        city_invest = df[df['investors'].str.contains(investor, na=False)].groupby('City  Location')['amount'].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(city_invest, labels=city_invest.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Rounds')
        round = df[df['investors'].str.contains(investor,na=False)].groupby('round')['amount'].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(round, labels=round.index, autopct="%0.01f%%")
        st.pyplot(fig2)


    with col2:



        df['year'] = pd.to_datetime(df['date']).dt.year
        yearly = df[df['investors'].str.contains('IDG Ventures', na=False)].groupby('year')['amount'].sum()
        st.subheader('Yearly Investment')
        fig2, ax2 = plt.subplots()
        ax2.plot(yearly.index, yearly.values)
        st.pyplot(fig2)



def overall_analysis():
    st.title('Overall Analysis')

    # Total invested amount
    total = round(df['amount'].sum())
    # Max amount infused in a startup
    max_funding = df.groupby('Startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # Avg ticket size
    avg_funding = df.groupby('Startup')['amount'].sum().mean()
    # Total funded startups
    num_startups = df['Startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max',str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('MoM Graph')
    select_opt = st.selectbox('Select Type', ['Total', 'Count'])

    if select_opt == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x-axis'], temp_df['amount'])

    st.pyplot(fig3)

    st.header('Sector Analysis')
    st.subheader("Top 3 Industries")
    top_verticals = df['Vertical'].value_counts().head(3)
    fig, ax = plt.subplots()
    top_verticals.plot(kind='pie', ax=ax)
    st.pyplot(fig)

    st.header('City Wise funding')
    total_investment_by_city = df.groupby('City  Location')['amount'].sum().fillna(0)
    total_investment_by_city = total_investment_by_city.sort_values(ascending=False)
    total_investment_by_city = total_investment_by_city.reset_index()

    st.subheader('Total Investment by City')
    # Plotting a pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(total_investment_by_city['amount'], labels=total_investment_by_city['City  Location'],autopct='%1.1f%%')
    ax.set_title('Total Investment by City')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Displaying the plot
    st.pyplot(fig)
    # Group by investors and find the maximum investment amount for each investor

    df['date'] = pd.to_datetime(df['date'])

    # Extract year from the date column
    df['year'] = df['date'].dt.year

    # Group by year and startup, summing the investment amounts, and finding the top startup each year
    top_startups_yearly = df.groupby(['year'])['Startup'].agg(lambda x: x.value_counts().idxmax()).reset_index()

    # bar graph
    st.title('Top Startup Year-Wise Overall')
    # Plotting a bar graph
    fig, ax = plt.subplots()
    ax.bar(top_startups_yearly['year'], top_startups_yearly['Startup'], color='skyblue')
    ax.set_xlabel('Year')
    ax.set_ylabel('Top Startup')
    ax.set_title('Top Startup Each Year Overall')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    # Displaying the plot
    st.pyplot(fig)


    st.title("Top Investors")
    # Aggregate investment amounts for each investor
    investor_totals = df.groupby('investors')['amount'].sum().reset_index()
    # Rank investors based on total investment amount
    investor_totals = investor_totals.sort_values(by='amount', ascending=False)
    # Select top investors (e.g., top 10)
    top_investors = investor_totals.head(10)
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(top_investors['amount'], labels=top_investors['investors'], autopct='%1.1f%%')
    ax.set_title('Top Investors')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart using Streamlit
    st.pyplot(fig)

    st.subheader('Funding Heatmap')
    heatmap_data = df.pivot_table(values='amount', index='year', columns='month', aggfunc='sum')
    fig10, ax10 = plt.subplots()
    cax = ax10.matshow(heatmap_data, cmap='viridis')
    fig10.colorbar(cax)
    ax10.set_xticks(range(len(heatmap_data.columns)))
    ax10.set_xticklabels(heatmap_data.columns, rotation=45)
    ax10.set_yticks(range(len(heatmap_data.index)))
    ax10.set_yticklabels(heatmap_data.index)
    st.pyplot(fig10)



def Startup_details(startup_name):
    st.header('Founders:')
    # Filter the DataFrame to select rows where the 'startup' column
    old_df = df[df['Startup'] == startup_name]
    # Print the names of investors in the startup
    int1 = old_df['investors']
    # Create a DataFrame from the 'investors' column
    investors_df = pd.DataFrame(int1, columns=['investors']).reset_index()
    # Display the DataFrame
    st.write(investors_df)

    col1, col2 = st.columns(2)

    with col1:
        st.title('Industry')
        industry_data = df[df['Startup'].str.contains(startup_name, na=False)]['Vertical'].str.lower().value_counts().head()

        # Create a pie chart for 'Industry'
        fig_industry, ax_industry = plt.subplots()
        ax_industry.pie(industry_data, labels=industry_data.index, autopct='%1.1f%%', startangle=90)
        ax_industry.set_title('Industry Distribution')

        # Display the pie chart using Streamlit
        st.pyplot(fig_industry)

    with col2:
        st.title('Sub-Industry')
        sub_industry_data = df[df['Startup'].str.contains(startup_name, na=False)]['subvertical'].str.lower().value_counts().head()

        # Create a pie chart for 'Sub-Industry'
        fig_subindustry, ax_subindustry = plt.subplots()
        ax_subindustry.pie(sub_industry_data, labels=sub_industry_data.index, autopct='%1.1f%%', startangle=90)
        ax_subindustry.set_title('Sub-Industry Distribution')

        # Display the pie chart using Streamlit
        st.pyplot(fig_subindustry)

    # 'City' section as pie chart
    st.title('City')
    city_data = df[df['Startup'].str.contains(startup_name, na=False)].groupby('Startup')['City  Location'].value_counts().head()

    # Create a pie chart for 'City'
    fig_city, ax_city = plt.subplots()
    ax_city.pie(city_data, labels=city_data.index, autopct='%1.1f%%', startangle=90)
    ax_city.set_title('City Distribution')

    # Display the pie chart using Streamlit
    st.pyplot(fig_city)

    st.header('Funding Rounds')
    funding_rounds_info = df[['round', 'investors', 'date']].sort_values('date', ascending=False)
    st.dataframe(funding_rounds_info)



if opt == 'Overall Analysis':
    st.title('Overall Analysis')
    st.header('Aaryan Ghadi')
    overall_analysis()



elif opt == 'Startup':
    st.title("Startup Analysis")
    select_start = selected_investor = st.sidebar.selectbox('Select One',sorted(set(df['Startup'].astype(str).str.split(',').sum())))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        st.title(select_start)
        Startup_details(select_start)

else:
    st.title('Investor')
    select=st.sidebar.selectbox('Select One',sorted(set(df['investors'].astype(str).str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(select)
