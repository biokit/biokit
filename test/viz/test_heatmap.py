from biokit.viz import heatmap
from biokit.data.viz.heatmap_sample import load_heatmap_sample



def _test_heatmap():
    data = load_heatmap_sample()
    h = heatmap.HiearchicalHeatmap(data)
    h.plot(
        cmap='hot', 
        category_cols=[0,0,1,1], 
        category_rows=[0,1,2,0,0,1,2,2,2,1])


