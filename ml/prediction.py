import numpy as np
from sklearn.linear_model import LinearRegression


def predict_stock(data):

    close = data["Close"].values

    # ensure correct shape
    close = close.reshape(-1)

    X = np.arange(len(close)).reshape(-1,1)
    y = close

    model = LinearRegression()

    model.fit(X,y)

    next_day = model.predict([[len(close)]])

    # FIX
    prediction = float(next_day.squeeze())

    return round(prediction,2)