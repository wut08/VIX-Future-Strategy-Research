import bql
bq = bql.Service()

ma_5 = bq.data.smavg(period='5',dates=bq.func.range('2004-06-01','2021-05-20'), fill='prev')
ma_15 = bq.data.smavg(period='15',dates=bq.func.range('2004-06-01','2021-05-20'), fill='prev')
ma_20 = bq.data.smavg(period='20',dates=bq.func.range('2004-06-01','2021-05-20'), fill='prev')
ma_30 = bq.data.smavg(period='30',dates=bq.func.range('2004-06-01','2021-05-20'), fill='prev')
ma_50 = bq.data.smavg(period='50',dates=bq.func.range('2004-06-01','2021-05-20'), fill='prev')
ma_100 = bq.data.smavg(period='100',dates=bq.func.range('2004-06-01','2021-05-20'), fill='prev')
ma_200 =  bq.data.smavg(period='200',dates=bq.func.range('2004-06-01','2021-05-20'), fill='prev')
ticker = ['SPX Index','VIX Index']

fields = {'MA_5':ma_5,'MA_15':ma_15,'MA_20':ma_20,'MA_30':ma_30,'MA_50':ma_50,'MA_100':ma_100,'MA_200':ma_200}

req = bql.Request(ticker,fields,preferences=bql.Preferences(dropcols=['CURRENCY']))
resp = bq.execute(req)
df= bql.combined_df(resp).reset_index().pivot(index='DATE',columns='ID')
df.to_csv('ma.csv')