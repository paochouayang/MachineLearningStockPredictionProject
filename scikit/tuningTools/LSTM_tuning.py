# Random Forest tuning

from stockPredictTuning import Stocks
from bestSettings import write_best_settings

algorithm = 'lstm'
unit_a_lst = [50, 100, 200]
unit_b_lst = [50, 100, 200]
unit_c_lst = [50, 100, 200]
seg_ratio = [1, 2, 4]
epochs_lst = [100, 200, 400]
batch_size_lst = [200, 500, 1000]
# Selected stocks from different price ranges.
symbol_lst = ['PSTV', 'TWTR', 'SOFI', 'ROIV', 'TSLA', 'COMS', 'RITM', 'SWN', 'PBLA', 'APGN', 'LVLU']

size = len(unit_a_lst) * len(unit_b_lst) * len(unit_c_lst) * len(seg_ratio) * len(epochs_lst) * len(batch_size_lst) * 3
count = 1

for unit_a in unit_a_lst:
    for unit_b in unit_b_lst:
        for unit_c in unit_c_lst:
            for ratio in seg_ratio:
                for epochs in epochs_lst:
                    for batch_size in batch_size_lst:
                        try:
                            print(f'Tuning status: {round((count / size) * 100, 2)}%')
                            model = Stocks(symbol_lst=symbol_lst, algorithm=algorithm, forecast_time_span='1d',
                                           unit_a=unit_a, unit_b=unit_b, unit_c=unit_c, epochs=epochs, batch_size=batch_size,
                                           seg_ratio=ratio)
                            mse = model.get_mse()
                            count += 1

                            with open('LSTM_TuningResults.txt', 'a') as file:
                                file.write('1d' + ',' + algorithm + ',' + str(mse) + ',' + str(unit_a) + ',' + str(
                                    unit_b) + ',' + str(unit_c) + ',' + str(epochs) + ',' + str(batch_size) + ',' + str(ratio) + '\n')

                        except Exception as e:
                            print(e)
                            count += 1

for unit_a in unit_a_lst:
    for unit_b in unit_b_lst:
        for unit_c in unit_c_lst:
            for ratio in seg_ratio:
                for epochs in epochs_lst:
                    for batch_size in batch_size_lst:
                        try:
                            print(f'Tuning status: {round((count / size) * 100, 2)}%')
                            model = Stocks(symbol_lst=symbol_lst, algorithm=algorithm, forecast_time_span='5d',
                                           unit_a=unit_a, unit_b=unit_b, unit_c=unit_c, epochs=epochs, batch_size=batch_size,
                                           seg_ratio=ratio)
                            mse = model.get_mse()
                            count += 1

                            with open('LSTM_TuningResults.txt', 'a') as file:
                                file.write('5d' + ',' + algorithm + ',' + str(mse) + ',' + str(unit_a) + ',' + str(
                                    unit_b) + ',' + str(unit_c) + ',' + str(epochs) + ',' + str(batch_size) + ',' + str(ratio) + '\n')

                        except Exception as e:
                            print(e)
                            count += 1

for unit_a in unit_a_lst:
    for unit_b in unit_b_lst:
        for unit_c in unit_c_lst:
            for ratio in seg_ratio:
                for epochs in epochs_lst:
                    for batch_size in batch_size_lst:
                        try:
                            print(f'Tuning status: {round((count / size) * 100, 2)}%')
                            model = Stocks(symbol_lst=symbol_lst, algorithm=algorithm, forecast_time_span='1mo',
                                           unit_a=unit_a, unit_b=unit_b, unit_c=unit_c, epochs=epochs, batch_size=batch_size,
                                           seg_ratio=ratio)
                            mse = model.get_mse()
                            count += 1

                            with open('LSTM_TuningResults.txt', 'a') as file:
                                file.write('1mo' + ',' + algorithm + ',' + str(mse) + ',' + str(unit_a) + ',' + str(
                                    unit_b) + ',' + str(unit_c) + ',' + str(epochs) + ',' + str(batch_size) + ',' + str(ratio) + '\n')

                        except Exception as e:
                            print(e)
                            count += 1

# format: forcast_time_span, algorithm, average_mse, unit_a, unit_b, unit_c, epochs, batch size, seg ratio
write_best_settings('LSTM_TuningResults.txt')
