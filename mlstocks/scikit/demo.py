from stockPredict import Stocks


symbol = 'BBBY'
algorithm = 'randomforest'

# So far, this predicts better in 5-day forecasts.
# May need to create and tune different models for different lengths of forecast.
forecast = '5d'    # ('1d', '5d', '1mo', '6mo', '1y')
stock_obj = Stocks(symbol=symbol, algorithm=algorithm, forcast_time_span=forecast)
stock_obj.forcast_test()
