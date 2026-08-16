import pandas as pd
def transform_order(orders):
    date_cols=['order_purchase_timestamp', 'order_approved_at','order_delivered_customer_date','order_delivered_carrier_date','order_estimated_delivery_date']
    for col in date_cols:
        orders[col]=pd.to_datetime(orders[col],errors='coerce')
        
    orders=orders[orders["order_status"]=="delivered"].copy()
    orders['delivery_delay_days']=(orders['order_delivered_customer_date']-orders["order_estimated_delivery_date"]).dt.days
    orders["delivery_time_days"] = (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    orders["processing_time_days"] = (
        orders["order_approved_at"]
        - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    orders=orders.dropna(subset=["order_delivered_customer_date"])
    orders["processing_time"]=(orders["order_approved_at"]-orders["order_purchase_timestamp"]).dt.days
    return orders;

def transform_order_items(order_items):
    order_items["shipping_limit_date"]=pd.to_datetime(order_items["shipping_limit_date"],errors="coerce")
    order_items["total_item_value"] = order_items["price"] + order_items["freight_value"]
    return order_items;

def transform_items(items):
    items=items.drop_duplicates()
    return items;

def transform_order_reviews(order_reviews):
    date_cols=['review_answer_timestamp','review_creation_date']
    for col in date_cols:
        order_reviews[col]=pd.to_datetime(order_reviews[col],errors='coerce')
    return order_reviews;

def transform_products(products):

    products = products.drop_duplicates()

    return products
def construct_table(orders, customers, reviews):
    ordercustomer = pd.merge(orders, customers, on="customer_id")

    # Reviews : garder la première review par commande, en LEFT join
    # (un inner join droppe les commandes sans review et biaise l'échantillon)
    reviews_dedup = reviews.sort_values("review_creation_date").drop_duplicates(
        subset="order_id", keep="first"
    )
    ordercustomer = pd.merge(
        ordercustomer, reviews_dedup, on="order_id", how="left"
    )

    # --- Identifier la 1ère commande de chaque client ---
    ordercustomer = ordercustomer.sort_values(
        ["customer_unique_id", "order_purchase_timestamp"]
    )
    ordercustomer["order_rank"] = ordercustomer.groupby(
        "customer_unique_id"
    ).cumcount() + 1

    first_orders = ordercustomer[ordercustomer["order_rank"] == 1].copy()
    first_orders["lateornot"] = (first_orders["delivery_delay_days"] > 0).astype(int)

    # --- Réachat : a-t-il commandé APRÈS sa 1ère commande, dans les 365j ---
    all_orders_dates = ordercustomer[
        ["customer_unique_id", "order_purchase_timestamp"]
    ].rename(columns={"order_purchase_timestamp": "later_purchase_date"})

    merged = pd.merge(first_orders, all_orders_dates, on="customer_unique_id")
    merged["is_repurchase_window"] = (
        (merged["later_purchase_date"] > merged["order_purchase_timestamp"])
        & (
            merged["later_purchase_date"]
            <= merged["order_purchase_timestamp"] + pd.Timedelta(days=365)
        )
    )
    repurchased = (
        merged.groupby("customer_unique_id")["is_repurchase_window"]
        .any()
        .rename("has_repurchased")
        .astype(int)
    )

    result = first_orders.merge(repurchased, on="customer_unique_id")

    result["delay_bucket"] = pd.cut(
        result["delivery_delay_days"],
        bins=[-999, -3, 0, 5, 15, 999],
        labels=["En avance", "À temps", "1-5j retard", "6-15j retard", ">15j retard"],
    )

    return result[
        [
            "customer_unique_id",
            "order_id",
            "delivery_delay_days",
            "delay_bucket",
            "lateornot",
            "review_score",
            "has_repurchased",
        ]
    ]