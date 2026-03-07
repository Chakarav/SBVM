import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

data = [27550, 30283, 33886, 33968, 40179, 34447, 38286, 41252, 41906, 44809, 44525, 47050, 42748, 43934, 48003, 48737, 58024, 50367, 50932]

index = pd.date_range(start='2021-06-30', periods=len(data), freq='QE')
ts_data = pd.Series(data, index=index)

model = SARIMAX(ts_data, order=(1, 0, 1), seasonal_order=(1, 1, 1, 4))
model_fit = model.fit(disp=False)
forecast = model_fit.forecast(steps=4)

for date, value in forecast.items():
    print(f"{date.date()}: {value:.2f}")