import pandas as pd

def data_wrangling(neighbourhood, bedrooms):
    df = pd.read_csv('data/tsne_final.csv')

    # filter the dataframe to show only SoHo data.
    df = df[(df.neighbourhood_cleansed == neighbourhood) & (df.minimum_nights <= 3) & (df.bedrooms == bedrooms)]

    # get only required cols
    cols = ['TSNE1', 'TSNE2', 'TSNE3', 'name', 'price_category', 'price', 'minimum_nights', 'id', 'bedrooms']

    df = df[cols]

    return df
