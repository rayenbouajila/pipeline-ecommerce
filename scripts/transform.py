import pandas as pd
def transform_order(orders):
    date_cols=['order_purchase_timestamp', 'order_approved_at','order_delivered_customer_date','order_delivered_carrier_date','order_estimated_delivery_date']
    for col in date_cols:
        orders[col]=pd.to_datetime(orders[col],errors='coerce')
        
    orders=orders[orders["order_status"]=="delivered"].copy()
    orders['delivery_delay_days']=(orders['order_delivered_customer_date']-orders["order_estimated_delivery_date"]).dt.days
    orders=orders.dropna(subset=["order_delivered_customer_date"])
    orders["processing_time"]=orders["order_approved_at"]-orders["order_purchase_timestamp"]
    return orders;
def transform_items(items):
    items.drop_duplicates()
def construct_table(orders,customers):
    ordercustomer=pd.merge(orders,customers,on="customer_id")
    ordercustomer["repeated"] = (ordercustomer["nb_orders"] > 1).astype(int)
