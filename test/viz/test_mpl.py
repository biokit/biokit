from biokit.viz import imshow



def test_viz_imshow():
    from pandas import DataFrame
    df = DataFrame({'a':[1,2], 'b':[3,4]})
    imshow(df)
