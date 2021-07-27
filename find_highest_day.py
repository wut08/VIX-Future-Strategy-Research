import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


#iterate through all these files and create dataframe
def find_highest_day(filepath):
    differences = []
    for contracts in filepath.glob('**/*'):


        contract = pd.read_excel(contracts)

        # get the final settlement price
        settlement = np.array(contract.iloc[:,5])
        settlement_num = np.delete(settlement,[0])
        settlement_num30 = settlement_num[-30:]
        #format all OHLC data
        OHLCS = np.array(contract.iloc[:,1:6])
        OHLCS_num = np.delete(OHLCS,(0),axis=0)
        OHLCS_num30 = np.delete(OHLCS_num, (-1),axis=0)

        # get all the differences between T30, T29... T and T

        diffMatrix = (OHLCS_num30[-29:] - settlement_num30[-1])*-1

        # note, here 0 = T-29, 28 = T-1

        maxlist = diffMatrix.tolist()
        maxv =max(maxlist)
        days = maxlist.index(maxv)

        days= np.array(days)

        days = 29 - days

        differences.append(days)

    count = Counter(differences)
    df_count = pd.DataFrame.from_dict(count, orient='index')
    df_count.columns = ['Highest Price Occurrence']
    df_ct = df_count.T.copy()

    df_ct.columns = [f'T-{i}' for i in df_ct.columns]
    return df_ct


