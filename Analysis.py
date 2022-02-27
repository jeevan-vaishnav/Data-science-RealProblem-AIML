#!/usr/bin/env python
# coding: utf-8

# # Sales Analysis

# In[1]:


import pandas as pd
import os


# # Task1#### Merging 12 months of sales data into a single file

# In[2]:



# files = [file for file in os.listdir('./Sales_Data')]



# all_month_data = pd.DataFrame()

# for file in files:
#     df = pd.read_csv('./Sales_Data/'+file)
#     all_month_data = pd.concat([all_month_data,df])

# all_month_data.to_csv("All_data.csv",index=False,)


# # Read in update dataframe

# In[3]:


all_data = pd.read_csv('All_data.csv')
all_data.head()


# # Clean up the data

# # Drop rows of NAN

# In[4]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head
all_data = all_data.dropna(how='all')
all_data.head()


# # FInd "or" delete it 

# In[5]:


all_data = all_data[all_data['Order Date'].str[0:2] !='Or']


# # Convert columns to the correct type

# In[6]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered']) #make int 
all_data['Price Each'] =  pd.to_numeric(all_data['Price Each'])#Make float

all_data.head()


# In[ ]:





# # Augment data with additional columns

# ## Task2 : Add Month Columns

# In[7]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# # Task 3 : Add a Sales Month

# In[8]:


all_data['Sales']  = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# # Task 4: Add a city column

# In[9]:


#lets use .apply() method

def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]


all_data['City'] = all_data['Purchase Address'].apply(lambda x : f"{get_city(x)}({get_state(x)})") 

# all_data = all_data.drop(columns = 'City, State',inplace=True)

# all_data['City'] = all_data['Purchase Address'].apply(lambda x:x.split(',')[1])
# all_data['State'] = all_data['Purchase Address'].apply(lambda x:x.split(',')[2].split(' ')[1])
# all_data = all_data.drop(columns='Column',inplace=True)
all_data.head()


# # Q 1 : What was the best month for sales ? How much was earned that month?

# In[10]:


results  = all_data.groupby('Month').sum()


# In[11]:


import matplotlib.pyplot as plt

months = range(1,13)

plt.bar(months,results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in India (Rs)' )
plt.xlabel("Number in month")
plt.show()


# # Question 2 :What city had the highest number of sales 

# In[12]:


results = all_data.groupby('City').sum()
results.head()


# In[13]:


import matplotlib.pyplot as plt

cites = all_data['City'].unique()
# cites
cites = [city for city,df in all_data.groupby('City')]
# cites
plt.bar(cites,results['Sales'])
plt.xticks(cites,rotation = 'vertical',size =8)
plt.ylabel('Sales in India (Rs)' )
plt.xlabel("City Name")
plt.show()


# # Questation 3 : What time should be we display advertisement to maxmize likelihood customer's buying product?

# In[23]:


all_data.head()


# In[22]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# In[24]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data['Count'] = 1
all_data.head()


# In[ ]:





# In[ ]:





# In[17]:


hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours,all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel("Hour")
plt.ylabel("Number Or Orders")
plt.grid()
plt.show()


# # Question 4 : What producst are most often sold together?

# In[25]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

df = df[['Order ID','Grouped']].drop_duplicates()

df.head()


# In[43]:



from itertools import combinations
from collections import Counter


count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,3)))

for key,value in count.most_common(10):
    print(key,value)



# # Last Quesetion : What product sold the most ? why do you think it sold the most ?

# In[44]:


all_data.head()


# In[70]:


product_group = all_data.groupby('Product')

# quantity_order = all_data['Quantity Ordered'].sum()
# print(quantity_order)


quantity_ordered = product_group.sum()['Quantity Ordered']
# print(quantity_ordered)


products = [product for product ,df in product_group]

plt.bar(products,quantity_ordered)
plt.xticks(products,rotation='vertical',size=10)
plt.ylabel("# Quantity Ordered")
plt.xlabel("Products")
plt.show()


# In[106]:


price = all_data.groupby('Product').mean()['Price Each']


fig,ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products,quantity_ordered,color='g')
ax2.plot(products,price,'b-')
ax1.set_xlabel("Product Name")
ax1.set_ylabel("quantity_ordered",color='g')
ax2.set_ylabel("Price ($)",color='b')
ax1.set_xticklabels(products,rotation='vertical',size=8)

plt.show()


# In[ ]:




