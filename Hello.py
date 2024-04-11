import streamlit as st
import pandas as pd
import plotly.express as px

def wide_space_default():
    st.set_page_config(layout='wide')

wide_space_default()

from map import map_continent

st.write("hello")

# Read CSV files into DataFrames
lifeexp_df = pd.read_csv('/workspaces/gapminder-data/files/lex.csv')
pop_df = pd.read_csv('/workspaces/gapminder-data/files/pop.csv')
gdp_df = pd.read_csv('/workspaces/gapminder-data/files/gdp_pcap.csv')

# Melt each DataFrame to reshape
lifeexp_df_melted = lifeexp_df.melt(id_vars=['country'], var_name='year', value_name='lifeExp')
pop_df_melted = pop_df.melt(id_vars=['country'], var_name='year', value_name='pop')
gdp_df_melted = gdp_df.melt(id_vars=['country'], var_name='year', value_name='gdpPercap')

# Merge DataFrames
merged_df = pd.merge(lifeexp_df_melted, pop_df_melted, on=['country', 'year'])
merged_df = pd.merge(merged_df, gdp_df_melted, on=['country', 'year'])

# st.dataframe(merged_df)

merged_df['pop'] = merged_df['pop'].astype('string')
merged_df['gdpPercap'] = merged_df['gdpPercap'].astype('string')
# merged_df.dtypes

def convert_population(pop_str):
    if pop_str[-1]=='k':
        return int(float(pop_str[:-1]) * 1000)  # Convert 'k' to thousands
    elif pop_str[-1]=='M':
        return int(float(pop_str[:-1]) * 1000000)  # Convert 'M' to millions
    elif pop_str[-1]=='B':
        return int(float(pop_str[:-1]) * 1000000000)  # Convert 'B' to billions
    else:
        return int(pop_str)  # For values without 'k' or 'M', convert directly to integer

# Apply the conversion function to the 'population' column
merged_df['pop'] = merged_df['pop'].apply(convert_population)
merged_df['gdpPercap'] = merged_df['gdpPercap'].apply(convert_population)

#convert year to integer
merged_df['year'] = merged_df['year'].astype(str).astype(int)


# Create a new column 'continent' based on the 'country' column
merged_df['continent'] = merged_df['country'].apply(map_continent)

merged_df.dropna()
merged_df.drop(merged_df[merged_df['year'] > 2023].index, inplace = True)

fig = px.scatter(
    data_frame = merged_df,
    x = "gdpPercap",
    y = "lifeExp",
    size = "pop",
    color = "continent",
    title = "test",
    labels = { "gdpPercap" : "Wealth",
               "lifeExp" : "Life Span"},
    log_x = True,
    hover_name = "country",
    animation_frame = "year",
    size_max = 100
)

fig.update_yaxes(range=[10,120])
fig.update_xaxes(range=[2.5,5.5])
st.plotly_chart(fig, theme="streamlit", use_container_width=True)
fig.show()