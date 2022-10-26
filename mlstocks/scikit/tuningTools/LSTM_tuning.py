# Random Forest tuning

from stockPredictTuning import Stocks
from bestSettings import write_best_settings

forecast_time_span_lst = ['1d', '5d', '1mo']
algorithm = 'lstm'
unit_a_lst = [10, 50, 100]
unit_b_lst = [10, 50, 100]
seg_ratio = [1, 2, 4, 6]
epochs_lst = [100, 200, 400]
batch_size_lst = [200, 500, 1000]
# Selected stocks from different price ranges.
stocks_lst = ['PSTV', 'TWTR', 'SOFI', 'ROIV', 'TSLA', 'COMS', 'RITM', 'SWN', 'PBLA', 'APGN', 'LVLU']

mse_list = []
size = len(forecast_time_span_lst) * len(unit_a_lst) * len(unit_b_lst) * len(seg_ratio) * len(epochs_lst) * len(batch_size_lst)
count = 1

for forecast_time_span in forecast_time_span_lst:
    for unit_a in unit_a_lst:
        for unit_b in unit_b_lst:
            for ratio in seg_ratio:
                for epochs in epochs_lst:
                    for batch_size in batch_size_lst:
                        mse_list = []
                        for symbol in stocks_lst:
                            print(f'Tuning status: {round((count / size) * 100, 2)}%')
                            model = Stocks(symbol=symbol, algorithm=algorithm, forecast_time_span=forecast_time_span,
                                           unit_a=unit_a, unit_b=unit_b, epochs=epochs, batch_size=batch_size,
                                           seg_ratio=ratio)
                            mse_list.append(model.get_mse())
                            count += 1

                        average_mse = sum(mse_list) / len(mse_list)
                        with open('LSTM_TuningResults.txt', 'a') as file:
                            file.write(forecast_time_span + ',' + algorithm + ',' + str(average_mse) + ',' + str(unit_a) + ',' + str(
                                unit_b) + ',' + str(epochs) + ',' + str(batch_size) + ',' + str(ratio) + '\n')

# format: forcast_time_span, algorithm, average_mse, max_depth, n_estimators, max_features, segment_ratio
write_best_settings('LSTM_TuningResults.txt')
