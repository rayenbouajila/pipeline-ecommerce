import pandas as pd

orders=pd.read_csv('../data/olist_orders_dataset.csv')
customers=pd.read_csv('../data/olist_customers_dataset.csv')
items=pd.read_csv('../data/olist_order_items_dataset.csv')
payments=pd.read_csv('../data/olist_order_payments_dataset.csv')
print("Orders\nShapes:",orders.shape,"\nData types:\n",orders.dtypes,orders.isnull().sum())
print("\n",orders.head())
print("\n",orders["order_status"].values.unique())
print("\ncustomers\nShapes:",customers.shape,"\nData types:\n",customers.dtypes,customers.isnull().sum())
print(customers.head())
print("\nitems\nShapes:",items.shape,"\nData types:\n",items.dtypes,items.isnull().sum())
print(items.head())
# print("\npayments\nShapes:",payments.shape,"\nData types:\n",payments.dtypes,payments.isnull().sum())
