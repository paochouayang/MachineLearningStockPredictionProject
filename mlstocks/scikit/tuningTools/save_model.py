from stockPredictTuning import Stocks
import pickle

symbol_lst = ['PSTV', 'TWTR', 'SOFI', 'ROIV', 'TSLA', 'COMS', 'RITM', 'SWN', 'PBLA', 'APGN', 'LVLU']

# 1 day Random Forest model save
stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='randomforest', forecast_time_span='1d', max_depth=20, n_estimators=500,
               seg_ratio=3, max_features='log2')
model = stock_obj.get_model()
filename = 'randomforest_1day_model.sav'
pickle.dump(model, open('saved_models/' + filename, 'wb'))

# 5 day Random Forest model save
stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='randomforest', forecast_time_span='5d', max_depth=40, n_estimators=500,
               seg_ratio=2, max_features=None)
model = stock_obj.get_model()
filename = 'randomforest_5day_model.sav'
pickle.dump(model, open('saved_models/' + filename, 'wb'))

# 1 month Random Forest model save
stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='randomforest', forecast_time_span='1mo', max_depth=10, n_estimators=50,
               seg_ratio=3, max_features=None)
model = stock_obj.get_model()
filename = 'randomforest_1month_model.sav'
pickle.dump(model, open('saved_models/' + filename, 'wb'))

# 1 day LSTM model save
stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='lstm', forecast_time_span='1d',
                                           unit_a=200, unit_b=50, unit_c=50, epochs=100, batch_size=1000,
                                           seg_ratio=4)
model = stock_obj.get_model()
folder = "saved_models/lstm_1day_model/"
model.save(folder)

# 5 day LSTM model save
stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='lstm', forecast_time_span='5d',
                                           unit_a=200, unit_b=50, unit_c=100, epochs=200, batch_size=200,
                                           seg_ratio=4)
model = stock_obj.get_model()
folder = "saved_models/lstm_5day_model/"
model.save(folder)

# 1 month LSTM model save
stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='lstm', forecast_time_span='1mo',
                                           unit_a=50, unit_b=200, unit_c=100, epochs=100, batch_size=2000,
                                           seg_ratio=4)
model = stock_obj.get_model()
folder = "saved_models/lstm_1month_model/"
model.save(folder)
