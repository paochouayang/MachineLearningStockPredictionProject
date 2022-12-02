import models

def add_data():
    i = 1
    for line in open('nasdaq_stocks.csv', 'r'):
        line = line.split(',')
        ticker = models.Tickers(i, line[0],line[1])
        ticker.save()
        i=i+1