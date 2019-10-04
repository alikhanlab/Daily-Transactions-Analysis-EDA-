#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 17:30:44 2019

@author: alikhannurlanuly
"""
import pandas as pd
import numpy as np

df = pd.read_csv('BreadBasket_DMS_output.csv')

'''
Q1

what is the busiest (in terms of number of transactions)? 
'''

# (a)
print('The busiest hour: ',df['Hour'].value_counts().index[0])
# (b)
print('The busiest day of the week: ', df['Weekday'].value_counts().index[0])
# (c)
print('The busiest period: ', df['Period'].value_counts().index[0])

'''
Observations:
    - The busiest hour:  11am
    - The busiest day of the week:  Saturday
    - The busiest period:  afternoon

By finding the busiest times, 
we can offer better service. 
For example, observe that busiest time, and 
look does the bakery have optimal number of cashiers, 
parking places, number of items in storage. 
As a result, we can adjust these services to demand, 
and get more profit.
'''


'''
# Q2

what is the most profitable time (in terms of revenue)?
'''

# The most profitable hour
hours_rev = dict(df.groupby('Hour')['Item_Price'].sum())
maximum_rev = max(hours_rev, key=hours_rev.get)
print('\nThe most profitable time: ')  
print('\nHour: ', maximum_rev, '\nRevenue: $',round(hours_rev[maximum_rev], 2))


# The most profitable day of the week
days_rev = dict(df.groupby('Weekday')['Item_Price'].sum())
maximum_rev = max(days_rev, key=days_rev.get)  
print('\nDay of the week: ', maximum_rev, '\nRevenue: $',round(days_rev[maximum_rev], 2))


# The most profitable period
period_rev = dict(df.groupby('Period')['Item_Price'].sum())
maximum_rev = max(period_rev, key=period_rev.get)  
print('\nPeriod: ', maximum_rev, '\nRevenue: $',round(period_rev[maximum_rev], 2))

'''
Observations:
    - The most profitable hour: 11 am
    - The most profitable day of the week: Saturday
    - The most profitable period of time: afternoon

By knowing the most profitable times, 
we can test the new items, how customers reacts to it. 
For example, if the mean profit increase after introducing 
that new product means customers like it.  
'''


'''
Q3

what is the most and least popular item?
'''

print('\nThe most popular item: ', df['Item'].value_counts().index[0])

s_dict = df['Item'].value_counts().to_dict()
result_dict = {k:v for (k,v) in s_dict.items() if v == df['Item'].value_counts().min()}

print('The least popular: ', [*result_dict.keys()])

'''
Observations:
The most popular item: Coffee
The least popular: ['Adjustment', 'The BART', 'Gift voucher', 'Chicken sand', 'Raw bars', 'Olum & polenta', 'Bacon', 'Polenta']
By finding most popular and least popular item, 
we can better deal with production. 
We know the damand for items, and produce accordingly to it. 
For most popular 20% ones we can introduce new types, special prices, to further increase popularity. 
On the other hand, for the least popular ones, we can think about their necessity, or investigate its unpopularity. 
Overall, these type of analysis, helps to build customer preference and target the popular items, reconsider unpopular ones.
'''

'''
Q4

assume one barrista can handle 50 transactions per day. 
How many barristas do you need for each day of the week?
'''

result = df.groupby(['Weekday'])['Transaction', 'Day'].nunique()

transaction_per_day = result['Transaction'] / result['Day'] 
barista_per_day = round(transaction_per_day / 50)

print('\nBarista per day:\n')
print(barista_per_day)

'''
Observations: 
    
Barista per day: 
Weekday 
Friday 2.0 
Monday 1.0 
Saturday 2.0 
Sunday 1.0 
Thursday 1.0 
Tuesday 1.0 
Wednesday 1.0
As a pre analysis assumption, one barrista can handle 50 transactions per day.
By finding the number of staff(barrista,baker, waiters). 
We can optimize operations cost. 
There is no economical reason to have in bakery 2 baristas, where one barista is enough to handle transactions or it can be other extreme.
As a result of this analysis, we adjusting operational stuff according to client stream.
'''


'''
Q5

divide all items in 3 groups (drinks, food, unknown). 
What is the average price of a drink and a food item?
'''

drinks = ['Coffee', 'Hot chocolate', 'Mineral water'
         'Juice', 'Smoothies', 'Focaccia', 'Gingerbread syrup'
         'Coke', 'Tea']
unknown = ['Gift voucher', 'Afternoon with the baker', 
          'NONE']

def categorize_item(row):
    if row['Item'] in drinks:
        category = "Drinks"
    elif row['Item'] in unknown:
        category = "Unknown"
    else:
        category = 'Food'
    return category

df['Category'] = df.apply(categorize_item, axis = 1)

food_mean_price = df[df['Category'] == 'Food']['Item_Price'].mean()

drinks_mean_price = df[df['Category'] == 'Drinks']['Item_Price'].mean()

print('\nFood mean price: $', round(food_mean_price, 2))
print('Drinks mean price: $', round(drinks_mean_price, 2))

'''
Observations:
Food mean price: $ 5.74
Drinks mean price: $4.95

By finding mean price, gives us general summary of our price policy. 
We can write how many dollar signs to Yelp, Google maps. 
We can adjust prices, as a general assumption we do not expect drinks prices to be higher than for foods prices. 
Also, we can experement on prices, lower food price, upper drinks, and see how market reacts to it.
'''



'''
Q6
does this coffee shop make more money from selling drinks or from selling food?
'''

food_revenue = round(df[df['Category'] == 'Food'].Item_Price.sum(), 2)
drinks_revenue = round(df[df['Category'] == 'Drinks'].Item_Price.sum(), 2)

print('\nFood total revenue: $', food_revenue)
print('Drinks total revenue: $', drinks_revenue)

print('Ratio food/drinks revenue: ',round(food_revenue/drinks_revenue, 2), '\n')

'''
Observations:

Food total revenue: $ 74350.66
Drinks total revenue: $ 37768.74 
Ratio food/drinks revenue: 1.97

By analysing food, drinks transactions, helps us better understand cash flow.
'''


'''
Q7
what are the top 5 most popular items for each day of the week? does this list stays the same from day to day?
'''

def top_5_items_weights(df):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
           'Saturday', 'Sunday']
    
    # intialise data of lists. 
    data = {'Weekdays': weekdays} 
  
    # Create DataFrame 
    df_result = pd.DataFrame(data) 
    
    top_5_all = []
    top_5_all_weights = []
    
    df.replace('NONE', np.nan, inplace=True)
    for day in weekdays:
        top_5 = list(df[df['Weekday'] == day].Item.value_counts(dropna = True)[:5].index)
        top_5_weights = list(df[df['Weekday'] == day].Item.value_counts(dropna = True, normalize = True)[:5].values)
        top_5_weights =  [round(x,2) for x in top_5_weights] 
        top_5_all.append(top_5)
        top_5_all_weights.append(top_5_weights)
    df_result['Top 5 items'] = top_5_all
    df_result['Weights top 5 items'] = top_5_all_weights
    
    return df_result

df_new1 = top_5_items_weights(df)
print(df_new1)
print()

'''
Observations:
Top 3 items (Coffee, Bread, Tea) do not change over week days, there are approximately 50% of all item sells.
All top 5 items have similar distribution.

By finding top sellers in each days, may help in marketing campaigns. 
As its shown, people have a pattern to eat sandwich on Mondays, 
than on other days, and we can do special prices or offer new kinds of sandwiches, thus attract more customers.
'''


'''
Q8

what are the bottom 5 least popular items for each day of the week? does this list stays the same from day to day? 
'''
def bottom_5_items_weights(df):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
           'Saturday', 'Sunday']
    
    # intialise data of lists. 
    data = {'Weekdays': weekdays} 
  
    # Create DataFrame 
    df_result = pd.DataFrame(data) 
    
    bottom_5_all = []
    bottom_5_all_weights = []
    
    df.replace('NONE', np.nan, inplace=True)
    for day in weekdays:
        bottom_5 = list(df[df['Weekday'] == day].Item.value_counts(dropna = True, ascending = True)[:5].index)
        bottom_5_weights = list(df[df['Weekday'] == day].Item.value_counts(dropna = True, normalize = True, ascending = True)[:5].values)
        bottom_5_weights =  [round(x,2) for x in bottom_5_weights] 
        bottom_5_all.append(bottom_5)
        bottom_5_all_weights.append(bottom_5_weights)
    df_result['Bottom 5 items'] = bottom_5_all
    df_result['Weights bottom 5 items'] = bottom_5_all_weights
    
    return df_result

df_new2 = bottom_5_items_weights(df)
print(df_new2)


'''
Observations:
The bottom 5 least popular items difer from day to day. But, 'Chocolates' in bottom 5 for three days of the week. 'Duck egg' in bottom 5 for two days of the week.
The distribution of least popular 5 items close to zero (we rounded 2 decimal points).
There is no clear patterns, on item preferences on each day. 
This analysis might be helpful in adjusting menu. 
For example, top seller on the top of menu, least sellers on th bottom of menu.
'''


'''
Q9
how many drinks are there per transaction?
'''
# Total number of unique transactions
transactions_unique = len(df['Transaction'].unique())
# Total number drinks  
number_drinks = len(df[df['Category'] == 'Drinks']['Transaction'])

# Drinks per transaction:

drinks_per_transaction = round(number_drinks/transactions_unique, 2)

print('\nDrinks per transaction: ', drinks_per_transaction)

'''
Observations:
There is 80% chance that the transaction will consist drink.
By finding drink/transaction ratio might be helpful. 
Even the business is bakery, drinks aslo should be consuder as main revenue source.
'''






