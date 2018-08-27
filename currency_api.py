import time
import numpy as np
import networkx as nx
from forex_python.converter import CurrencyRates


currency_codes = ['EUR', 'USD', 'GBP', 'JPY', 'CNY', 'INR', 'AUD']


def currency_nxgraph(list_codes, sleeping=0, adjmatrix=False):
    print('Lazy-search for real time rates')
    c = CurrencyRates()
    d = {}
    for currency in list_codes:
        print(f'Checking for {currency}')
        d[currency] = {}
        remaining_codes = [i for i in list_codes if i not in list(d.keys())]
        for other_currency in remaining_codes:
            log_rate = np.log(c.get_rate(currency, other_currency))
            d[currency][other_currency] = {}
            d[currency][other_currency]['weights'] = log_rate
        time.sleep(0.5)
    G = nx.from_dict_of_dicts(d)
    return G


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pdb
    G = currency_nxgraph(currency_codes)
    plt.plot()
    nx.draw_networkx(G, pos=nx.spring_layout(G))
    plt.savefig('currency_graph.png')
    plt.close()
    pdb.set_trace()
