from biokit.viz import Heatmap
from biokit import biokit_data

def test_heatmap():
    filename = biokit_data("test_heatmap.csv")
    import pandas as pd
    data = pd.read_csv(filename, skiprows=2, index_col=0)

    h = Heatmap(data)
    h.plot(cmap='hot')
    h.row_method= 'single'
    h.col_method= 'single'
    #    category_cols=[0,0,1,1], 
    #    category_rows=[0,1,2,0,0,1,2,2,2,1])


