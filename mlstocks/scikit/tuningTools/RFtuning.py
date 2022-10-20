# Random Forest tuning

from stockPredictTuning import Stocks
from bestSettings import write_best_settings

forecast_time_span_lst = ['1d', '5d', '1mo']
algorithm = 'randomforest'
# Random Forest tuning
max_depth_param = [10, 20, 30, 40, 50]
n_estimators_param = [50, 100, 500]
max_features_param = [None, 'sqrt', 'log2']
seg_ratio = [1, 2, 3]

# Selected stocks from different price ranges.
stocks_lst = ['PSTV', 'TWTR', 'SOFI', 'ROIV', 'TSLA', 'COMS', 'RITM', 'SWN', 'PBLA', 'APGN', 'LVLU']

mse_list = []
size = len(forecast_time_span_lst) * len(max_depth_param) * len(n_estimators_param) * len(max_features_param) * len(stocks_lst) * len(seg_ratio)
count = 1

for forecast_time_span in forecast_time_span_lst:
    for max_depth in max_depth_param:
        for n_estimators in n_estimators_param:
            for max_features in max_features_param:
                for ratio in seg_ratio:
                    mse_list = []
                    for symbol in stocks_lst:
                        print(f'Tuning status: {round((count / size) * 100, 2)}%')
                        model = Stocks(symbol=symbol, algorithm=algorithm, forecast_time_span=forecast_time_span,
                                       max_depth=max_depth, n_estimators=n_estimators, max_features=max_features,
                                       seg_ratio=ratio)
                        mse_list.append(model.get_mse())
                        count += 1

                    average_mse = sum(mse_list) / len(mse_list)
                    with open('RF_TuningResults.txt', 'a') as file:
                        file.write(forecast_time_span + ',' + algorithm + ',' + str(average_mse) + ',' + str(
                            max_depth) + ',' + str(n_estimators) + ',' + str(max_features) + ',' + str(ratio) + '\n')

# format: forcast_time_span, algorithm, average_mse, max_depth, n_estimators, max_features, segment_ratio
write_best_settings()
