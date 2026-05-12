import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Book Sales Dashboard",
    layout="wide"
)

st.title("📚 Book Sales Analytics Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("Cleaned_book_sales_data.csv")

df = load_data()

st.sidebar.header("🔍 Filters")

selected_genre = st.sidebar.multiselect(
    "Select Genre",
    options=sorted(df['genre'].unique()),
    default=sorted(df['genre'].unique())
)

selected_year = st.sidebar.slider(
    "Publishing Year Range",
    int(df['Publishing Year'].min()),
    int(df['Publishing Year'].max()),
    (
        int(df['Publishing Year'].min()),
        int(df['Publishing Year'].max())
    )
)

filtered_df = df[
    (df['genre'].isin(selected_genre)) &
    (df['Publishing Year'] >= selected_year[0]) &
    (df['Publishing Year'] <= selected_year[1])
]

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Books",
        filtered_df.shape[0]
    )

with col2:
    st.metric(
        "Total Units Sold",
        f"{filtered_df['units sold'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Total Revenue",
        f"${filtered_df['gross sales'].sum():,.0f}"
    )

with col4:
    st.metric(
        "Average Rating",
        round(filtered_df['Book_average_rating'].mean(), 2)
    )

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📚 Books by Genre")
    genre_counts = filtered_df['genre'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        genre_counts.index,
        genre_counts.values
    )

    plt.xticks(rotation=90)
    plt.xlabel("Genre")
    plt.ylabel("Count")

    st.pyplot(fig)

with right_col:
    st.subheader("📅 Publishing Year Distribution")

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        filtered_df['Publishing Year'],
        bins=10
    )

    plt.xlabel("Publishing Year")
    plt.ylabel("Frequency")

    st.pyplot(fig)

st.subheader('Average price of book by year')

grouped_year=filtered_df.groupby('Publishing Year')['sale price'].mean().reset_index()
fig, ax= plt.subplots(figsize=(12,5))
sns.lineplot(x="Publishing Year", y="sale price", data=grouped_year, color="skyblue", ax=ax)
plt.xlabel("Publishing Year")
plt.ylabel("Sale Price")
st.pyplot(fig)

left_2, right_2 = st.columns(2)

with left_2:
    st.subheader("🏢 Top Publishers by Units Sold")
    unit_sold_per_publisher=filtered_df.groupby('Publisher')['units sold'].sum().sort_values(ascending=False)
    units_in_m=round(unit_sold_per_publisher/1000000, 2)

    fig, ax=plt.subplots(figsize=(8,4))
    ax.bar(units_in_m.index, units_in_m)
    plt.xticks(rotation=90)
    plt.xlabel('Publishers')
    plt.ylabel('Units sold in millions')
    
    st.pyplot(fig)

with right_2:
    st.subheader("🔥 Correlation Heatmap")

    corr_cols = [
        'units sold',
        'gross sales',
        'publisher revenue',
        'sale price',
        'Book_average_rating'
    ]

    corr_matrix = filtered_df[corr_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap='coolwarm',
        ax=ax
    )

    st.pyplot(fig)

left_3, right_3=st.columns(2)

with left_3:
    st.subheader("💰 Sale Price vs Units Sold")

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(
        filtered_df['sale price'],
        filtered_df['units sold'],
        alpha=0.5
    )

    plt.xlabel("Sale Price")
    plt.ylabel("Units Sold")

    st.pyplot(fig)

with right_3:
    st.subheader("✍️ Top Authors by Average Rating")

    author_rating = (
        filtered_df
        .groupby('Author')['Book_average_rating']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.barh(
        author_rating.index,
        author_rating.values
    )

    plt.xlabel("Average Rating")

    st.pyplot(fig)

st.subheader("📈 Revenue Trend Over Years")

revenue_trend = (
    filtered_df
    .groupby('Publishing Year')['gross sales']
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    revenue_trend['Publishing Year'],
    revenue_trend['gross sales']
)

plt.xlabel("Publishing Year")
plt.ylabel("Gross Sales")

st.pyplot(fig)


st.subheader("🏆 Top Selling Books")

best_books = (
    filtered_df[[
        'Book Name',
        'Author',
        'genre',
        'units sold',
        'gross sales'
    ]]
    .sort_values(
        by='units sold',
        ascending=False
    )
    .head(10)
)

st.dataframe(best_books)

with st.expander("📄 View Dataset"):
    st.dataframe(filtered_df)
