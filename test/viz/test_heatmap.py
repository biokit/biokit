from biokit.viz import Heatmap
from biokit.data.viz.heatmap_sample import load_heatmap_sample



def test_heatmap():
    data = load_heatmap_sample()
    h = Heatmap(data)
    h.plot(cmap='hot')
    h.row_method= 'single'
    h.col_method= 'single'
    #    category_cols=[0,0,1,1], 
    #    category_rows=[0,1,2,0,0,1,2,2,2,1])


