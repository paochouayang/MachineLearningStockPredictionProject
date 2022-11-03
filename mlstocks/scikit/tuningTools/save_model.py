from stockPredictTuning import Stocks
import pickle

symbol_lst = ['PSTV', 'TWTR', 'SOFI', 'ROIV', 'TSLA', 'COMS', 'RITM', 'SWN', 'PBLA', 'APGN', 'LVLU']

stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='randomforest', forecast_time_span='1d', max_depth=20, n_estimators=500,
               seg_ratio=3, max_features='log2')
model = stock_obj.get_model()
filename = 'randomforest_1day_model.sav'
pickle.dump(model, open('saved_models/' + filename, 'wb'))

stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='randomforest', forecast_time_span='5d', max_depth=40, n_estimators=500,
               seg_ratio=2, max_features=None)
model = stock_obj.get_model()
filename = 'randomforest_5day_model.sav'
pickle.dump(model, open('saved_models/' + filename, 'wb'))

stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='randomforest', forecast_time_span='1mo', max_depth=10, n_estimators=50,
               seg_ratio=3, max_features=None)
model = stock_obj.get_model()
filename = 'randomforest_1month_model.sav'
pickle.dump(model, open('saved_models/' + filename, 'wb'))

# Save LSTM model
stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='lstm', forecast_time_span='1d',
                                           unit_a=200, unit_b=50, unit_c=50, epochs=100, batch_size=1000,
                                           seg_ratio=4)
model = stock_obj.get_model()
folder = "saved_models/lstm_1day_model/"
model.save(folder)

stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='lstm', forecast_time_span='5d',
                                           unit_a=50, unit_b=100, unit_c=100, epochs=400, batch_size=1000,
                                           seg_ratio=2)
model = stock_obj.get_model()
folder = "saved_models/lstm_5day_model/"
model.save(folder)

stock_obj = Stocks(symbol_lst=symbol_lst, algorithm='lstm', forecast_time_span='1mo',
                                           unit_a=100, unit_b=100, unit_c=100, epochs=400, batch_size=1000,
                                           seg_ratio=2)
model = stock_obj.get_model()
folder = "saved_models/lstm_1month_model/"
model.save(folder)
