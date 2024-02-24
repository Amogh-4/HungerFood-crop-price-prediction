## Features
  - 5 commodities crop value forecasting
  - Crop detailed forecast upto next 12 months
  - Crop price prediction with 93-95% accuracy
  - Model trained on authenticated datasets provided by [data.gov.in](https://data.gov.in)
  - Prediction done by using Decision Tree Regression techniques.
  - Annual Rainfall, WPI(Wholesale Price Index) datasets are used for training the model
  - Reference model used - https://github.com/rahuldkjain/Crop_Prediction which was retrained with datasets
 
### Tech
* [Python(3.0 or above)](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)-pip install flask
* [Scikit-Learn](https://scikit-learn.org/)-pip install scikit-learn
* [pandas](https://pandas.pydata.org/) -pip install pandas
* [numpy](https://numpy.org/) - pip install numpy

## Installation Guide
To install and run this webapp, you will need [Python(3.0 or above)](https://www.python.org/), and [pip](https://pypi.org/project/pip/) installed on your system
```sh
After installing, clone the repo and fetch it on to your local device.
Run app.py file to run the prediction model
The model would be running on your localhost

The predicted data will be obtained as a json object at following addresses:
Paddy - http://127.0.0.1:5000/paddy
Wheat - http://127.0.0.1:5000/wheat
Jowar - http://127.0.0.1:5000/jowar
Groundnut - http://127.0.0.1:5000/groundnut
Sugarcane - http://127.0.0.1:5000/sugarcane
Data of above 5 crops(cumulative) - http://127.0.0.1:5000/commodities