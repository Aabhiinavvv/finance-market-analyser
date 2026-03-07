import pandas as pd

def run_screener():

    data = {
        "Stock":["Reliance","TCS","HDFC","Infosys"],
        "PE":[18,25,16,22],
        "ROE":[19,21,17,23]
    }

    df = pd.DataFrame(data)

    return df[df["ROE"]>18]