from biokit.viz import heatmap
from biokit.data.viz.heatmap_sample import load_heatmap_sample



def test_heatmap():
    data = load_heatmap_sample()
    h = heatmap.HiearchicalHeatmap(); 
    h.frame = data;
    h.plot(cmap='hot', category_cols=[0,0,1,1], category_rows=[0,1,2,0,0,1,2,2,2,1])



