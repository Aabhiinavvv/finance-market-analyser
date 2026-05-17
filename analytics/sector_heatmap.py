import pandas as pd

def sector_data():

    data = {
        "Sector":["IT","Banking","Energy","FMCG","Pharma"],
        "Change":[1.2,-0.5,0.8,-0.2,1.5]
    }

    return pd.DataFrame(data)