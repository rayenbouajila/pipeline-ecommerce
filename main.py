from scripts.explore import load_raw_data
from scripts.transform import (
    transform_order,
    transform_order_items,
    transform_order_reviews,
    transform_items,
    transform_order_reviews,
    construct_table
)
from scripts.load import get_engine, load_dataframe, test_connection
from scripts.analyze import run_analysis
if __name__ == "__main__":
    print("Test de connexion...")
    engine = get_engine()
    test_connection(engine)

    print("\nExtraction des données...")
    orders,customers,items,payments,order_items,reviews,products= load_raw_data()

    print("\nTransformation...")
    orders=transform_order(orders)
    order_items=transform_order_items(order_items)
    reviews=transform_order_reviews(reviews)
    items=transform_items(items)
    ordercustomerreview=construct_table(orders, customers, reviews);

    print("\ntableau final ")
    print(ordercustomerreview[ordercustomerreview["has_repurchased"]==1].head(20))
    print(run_analysis(ordercustomerreview))
    print("\nChargement des tables staging...")
    load_dataframe(orders,      "fact_order_delivery",   engine)  # grain commande — pour drill-down PowerBI
    load_dataframe(order_items, "stg_order_items",        engine)
    load_dataframe(customers,   "dim_customers",          engine)
    load_dataframe(products,    "dim_products",           engine)
    load_dataframe(payments,    "stg_payments",           engine)
    load_dataframe(reviews,     "stg_reviews",             engine)

    print("\nConstruction de la table analytique...")
    customer_repurchase = construct_table(orders, customers, reviews)
    load_dataframe(customer_repurchase, "fact_customer_repurchase", engine)

    print("\nPipeline ETL terminé !")
    print("\nExport en csv...")
    import os
    os.makedirs("exports", exist_ok=True)

    orders.to_csv("exports/fact_order_delivery.csv", index=False, encoding="utf-8-sig")
    order_items.to_csv("exports/stg_order_items.csv", index=False, encoding="utf-8-sig")
    customers.to_csv("exports/dim_customers.csv", index=False, encoding="utf-8-sig")
    products.to_csv("exports/dim_products.csv", index=False, encoding="utf-8-sig")
    payments.to_csv("exports/stg_payments.csv", index=False, encoding="utf-8-sig")
    reviews.to_csv("exports/stg_reviews.csv", index=False, encoding="utf-8-sig")
    customer_repurchase.to_csv("exports/fact_customer_repurchase.csv", index=False, encoding="utf-8-sig")

    print("Export terminé dans /exports")