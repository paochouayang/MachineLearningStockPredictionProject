# Random Forest tuning
from stockPredictTuning import Stocks
from bestSettings import write_best_settings
import pickle


algorithm = 'randomforest'
# Random Forest tuning
max_depth_param = [10, 20, 30, 40, 50]
n_estimators_param = [50, 100, 500]
max_features_param = [None, 'sqrt', 'log2']
seg_ratio = [1, 2, 3]

# Selected stocks from different price ranges.
symbol_lst = ['PSTV', 'TWTR', 'SOFI', 'ROIV', 'TSLA', 'COMS', 'RITM', 'SWN', 'PBLA', 'APGN', 'LVLU']
size = len(max_depth_param) * len(n_estimators_param) * len(max_features_param) * len(seg_ratio) * 3
count = 1

for max_depth in max_depth_param:
    for n_estimators in n_estimators_param:
        for max_features in max_features_param:
            for ratio in seg_ratio:
                try:
                    print(f'Tuning status: {round((count / size) * 100, 2)}%')
                    stock_obj = Stocks(symbol_lst=symbol_lst, algorithm=algorithm, forecast_time_span='1d',
                                       max_depth=max_depth, n_estimators=n_estimators, max_features=max_features,
                                       seg_ratio=ratio)
                    mse = stock_obj.get_mse()
                    count += 1

                    with open('RF_TuningResults.txt', 'a') as file:
                        file.write('1d' + ',' + algorithm + ',' + str(mse) + ',' + str(
                            max_depth) + ',' + str(n_estimators) + ',' + str(max_features) + ',' + str(ratio) + '\n')

                except Exception as e:
                    print(e)
                    count += 1


for max_depth in max_depth_param:
    for n_estimators in n_estimators_param:
        for max_features in max_features_param:
            for ratio in seg_ratio:
                try:
                    print(f'Tuning status: {round((count / size) * 100, 2)}%')
                    stock_obj = Stocks(symbol_lst=symbol_lst, algorithm=algorithm, forecast_time_span='5d',
                                       max_depth=max_depth, n_estimators=n_estimators, max_features=max_features,
                                       seg_ratio=ratio)
                    mse = stock_obj.get_mse()

                    count += 1

                    with open('RF_TuningResults.txt', 'a') as file:
                        file.write('5d' + ',' + algorithm + ',' + str(mse) + ',' + str(
                            max_depth) + ',' + str(n_estimators) + ',' + str(max_features) + ',' + str(ratio) + '\n')

                except Exception as e:
                    print(e)
                    count += 1

for max_depth in max_depth_param:
    for n_estimators in n_estimators_param:
        for max_features in max_features_param:
            for ratio in seg_ratio:
                try:
                    print(f'Tuning status: {round((count / size) * 100, 2)}%')
                    stock_obj = Stocks(symbol_lst=symbol_lst, algorithm=algorithm, forecast_time_span='1mo',
                                       max_depth=max_depth, n_estimators=n_estimators, max_features=max_features,
                                       seg_ratio=ratio)
                    mse = stock_obj.get_mse()
                    count += 1

                    with open('RF_TuningResults.txt', 'a') as file:
                        file.write('1mo' + ',' + algorithm + ',' + str(mse) + ',' + str(
                            max_depth) + ',' + str(n_estimators) + ',' + str(max_features) + ',' + str(ratio) + '\n')

                except Exception as e:
                    print(e)
                    count += 1

# format: forecast_time_span, algorithm, mse, max_depth, n_estimators, max_features, seg_ratio
write_best_settings('RF_TuningResults.txt')
