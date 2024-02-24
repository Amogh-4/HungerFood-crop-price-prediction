from flask import Flask, jsonify
import numpy as np
import pandas as pd
from datetime import datetime
import random
import requests

#Reference model used - https://github.com/rahuldkjain/Crop_Prediction which was retrained with datasets

app = Flask(__name__)

commodity_dict = {
    "groundnut": "static/Groundnut.csv",
    "jowar": "static/Jowar.csv",
    "paddy": "static/Paddy.csv",
    "sugarcane": "static/Sugarcane.csv",
    "wheat": "static/Wheat.csv"
}

annual_rainfall = [26.625, 17.975, 22.25, 35.875, 78.525, 160.925, 287.325, 272, 212.125, 100.25, 33.975, 17.575]
base = {
    "Paddy": 1245.5,
    "Groundnut": 3700,
    "Jowar": 1520,
    "Sugarcane": 2250,
    "Wheat": 1350
}
commodity_list = []


class Commodity:

    def __init__(self, csv_name):
        self.name = csv_name
        dataset = pd.read_csv(csv_name)
        self.X = dataset.iloc[:, :-1].values
        self.Y = dataset.iloc[:, 3].values

        from sklearn.tree import DecisionTreeRegressor
        depth = random.randrange(7,18)
        self.regressor = DecisionTreeRegressor(max_depth=depth)
        self.regressor.fit(self.X, self.Y)

    def getPredictedValue(self, value):
        if value[1]>=2022:
            fsa = np.array(value).reshape(1, 3)
            return self.regressor.predict(fsa)[0]
        else:
            c=self.X[:,0:2]
            x=[]
            for i in c:
                x.append(i.tolist())
            fsa = [value[0], value[1]]
            ind = 0
            for i in range(0,len(x)):
                if x[i]==fsa:
                    ind=i
                    break
            return self.Y[i]

    def getCropName(self):
        a = self.name.split('.')
        return a[0]


@app.route('/')
def index():
    return 'CROP PRICE PREDICTION'


@app.route('/<name>', methods=['GET'])
def crop_profile(name):
    forecast_crop_values = TwelveMonthsForecast(name)
    current_price = CurrentMonth(name)
    context = {
        "name":name,
        "forecast_values": forecast_crop_values,
        "current_price": current_price,
    }
    return jsonify(context)

@app.route('/commodities', methods = ['GET'])
def get_all_details():
    cumu_data = []
    url_s = ['http://127.0.0.1:5000/paddy', 'http://127.0.0.1:5000/wheat', 'http://127.0.0.1:5000/groundnut', 'http://127.0.0.1:5000/jowar', 'http://127.0.0.1:5000/sugarcane']
    for url in url_s:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            cumu_data.append(data)
        else:
            return 'Invalid'
    return cumu_data
            

def CurrentMonth(name):
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    name = name.lower()
    commodity = commodity_list[0]
    for i in commodity_list:
        if name == str(i):
            commodity = i
            break
    current_wpi = commodity.getPredictedValue([float(current_month), current_year, current_rainfall])
    current_price = (base[name.capitalize()]*current_wpi)/100
    return current_price

def TwelveMonthsForecast(name):
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    name = name.lower()
    commodity = commodity_list[0]
    for i in commodity_list:
        if name == str(i):
            commodity = i
            break
    month_with_year = []
    for i in range(1, 13):
        if current_month + i <= 12:
            month_with_year.append((current_month + i, current_year, annual_rainfall[current_month + i - 1]))
        else:
            month_with_year.append((current_month + i - 12, current_year + 1, annual_rainfall[current_month + i - 13]))
    max_value = 0
    min_value = 9999
    wpis = []
    current_wpi = commodity.getPredictedValue([float(current_month), current_year, current_rainfall])
    change = []

    for m, y, r in month_with_year:
        current_predict = commodity.getPredictedValue([float(m), y, r])
        if current_predict > max_value:
            max_value = current_predict
        if current_predict < min_value:
            min_value = current_predict
        wpis.append(current_predict)
        change.append(((current_predict - current_wpi) * 100) / current_wpi)

    min_value = min_value * base[name.capitalize()] / 100
    max_value = max_value * base[name.capitalize()] / 100
    crop_price = []
    for i in range(0, len(wpis)):
        m, y, r = month_with_year[i]
        x = datetime(y, m, 1)
        x = x.strftime("%b %y")
        crop_price.append([x, round((wpis[i]* base[name.capitalize()]) / 100, 2) , round(change[i], 2)])

    return crop_price


def TwelveMonthPrevious(name):
    name = name.lower()
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_rainfall = annual_rainfall[current_month - 1]
    commodity = commodity_list[0]
    wpis = []
    crop_price = []
    for i in commodity_list:
        if name == str(i):
            commodity = i
            break
    month_with_year = []
    for i in range(1, 13):
        if current_month - i >= 1:
            month_with_year.append((current_month - i, current_year, annual_rainfall[current_month - i - 1]))
        else:
            month_with_year.append((current_month - i + 12, current_year - 1, annual_rainfall[current_month - i + 11]))

    for m, y, r in month_with_year:
        current_predict = commodity.getPredictedValue([float(m), 2013, r])
        wpis.append(current_predict)

    for i in range(0, len(wpis)):
        m, y, r = month_with_year[i]
        x = datetime(y,m,1)
        x = x.strftime("%b %y")
        crop_price.append([x, round((wpis[i]* base[name.capitalize()]) / 100, 2)])
    new_crop_price =[]
    for i in range(len(crop_price)-1,-1,-1):
        new_crop_price.append(crop_price[i])
    return new_crop_price


if __name__ == "__main__":
    groundnut = Commodity(commodity_dict["groundnut"])
    commodity_list.append(groundnut)
    jowar = Commodity(commodity_dict["jowar"])
    commodity_list.append(jowar)
    paddy = Commodity(commodity_dict["paddy"])
    commodity_list.append(paddy)
    sugarcane = Commodity(commodity_dict["sugarcane"])
    commodity_list.append(sugarcane)
    wheat = Commodity(commodity_dict["wheat"])
    commodity_list.append(wheat)

    app.run(host='0.0.0.0')