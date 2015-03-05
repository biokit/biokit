import pandas as pd
import easydev


def load_heatmap_sample():
    """A simple data frame to play with"""
    filename = easydev.gsf("biokit", "data/viz", "heatmap_sample.csv")
    df = pd.read_csv(filename, skiprows=2, index_col=0)
    return df
