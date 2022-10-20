def write_best_settings():
    with open('RF_TuningResults.txt', 'r') as file:
        settings_lst = file.read().splitlines()
    forecast_time_span_lst = ['1d', '5d', '1mo']
    for forecast_time_span in forecast_time_span_lst:
        min_mse = 99999.9
        best_settings = []
        for setting in settings_lst:
            setting_vals = setting.split(',')
            mse = float(setting_vals[2])
            if setting_vals[0] == forecast_time_span and mse < min_mse:
                best_settings = setting_vals
                min_mse = mse
        with open('bestSettings.txt', 'a') as file:
            file.write(str(best_settings) + '\n')

write_best_settings()


