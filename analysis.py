import pandas as pd
import numpy as np
import scraper

def get_data():
    df = pd.DataFrame.from_dict(scraper.main(100))
    return df
pd.DataFrame.to_csv(get_data(),'data.csv')
