from train_model import Trainer
import time

#with open('nasdaq_stocks_list.txt', 'r') as f:
#    stocks_lst = f.read().splitlines()
stocks_lst = ['TSLA', 'GOOGL']
forecast_time_span_lst = ['1d', '5d', '1mo']
size = len(stocks_lst) * len(forecast_time_span_lst)
count = 1
for symbol in stocks_lst:
    for forecast_time_span in forecast_time_span_lst:
        try:
            trainer = Trainer(symbol, 'randomforest', forecast_time_span)
            trainer.train()
            print(f'Progress: {round((count / size) * 100, 2)} %')
        except Exception as e:
            print(e)
        count += 1
        # yfinance has a rate limit of 2000 requests per hour. Wait 2 seconds between each request.
        time.sleep(2)
