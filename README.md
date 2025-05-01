# Sol_Assessment_Ind_Mod_H.Ragab_
Total  Return  Stock  Index   - Selecting q number of high capitalized stocks, Index levels  based on total retuns,  Monthly Rebalancing 


# Assessment Index Modelling 

## Overview
An implementation of Total Return Stock Index Model that calculates stock index levels based on Mkt Cap. The model Monthly rebalancing.

## Features

1- Initial Index Value = 100.
2- Index constituents =  3 stocks. 
3- Constituents selection based on Mkt Cap. (all stocks hold same outstanding shares, ie. prices identify highest cap) 
4- Rebalancing Monthly.  
2- Index Calculation – Applies geometric compounding with predefined weights (0.5, 0.25, 0.25).  
3- CSV Export – Saves computed index levels.  
4- Plotting support

## Requirements 
see 'requirments.txt'

## Usage
```python
from index_model import IndexModel
from datetime import date

model = IndexModel(price_data=mkt)
index_series = model.calc_index_level(start_date=date(2020,1,1), end_date=date(2020,12,31))
model.export_values("index_2020.csv")
model.plot_index()





