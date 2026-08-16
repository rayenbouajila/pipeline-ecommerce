# Ecommerce ETL Pipeline & Power BI Dashboards

Pipeline ETL en Python transformant des données e-commerce brutes (100k+ commandes) en modèle analytique en étoile, chargé dans PostgreSQL et exporté vers Power BI pour l'analyse du réachat client, des délais de livraison et de la satisfaction.

## Aperçu

Ce projet extrait, nettoie et transforme des données issues de plusieurs sources (commandes, clients, produits, paiements, avis, items de commande), calcule des indicateurs métier clés, puis charge le résultat dans une base PostgreSQL. Les données sont ensuite exportées en CSV pour construire des dashboards Power BI orientés fidélisation client et performance logistique.

## Fonctionnalités

- **Extraction** de 7 tables sources brutes
- **Transformation** avec Pandas :
  - Typage et nettoyage des colonnes de dates
  - Calcul du délai de livraison (`delivery_delay_days`), du temps de livraison total (`delivery_time_days`) et du temps de traitement (`processing_time_days`)
  - Détection du réachat client (`has_repurchased`) via une logique de fenêtre glissante de 365 jours par client
  - Catégorisation des retards de livraison en buckets (`delay_bucket`)
- **Chargement** dans PostgreSQL via SQLAlchemy, selon un modèle en étoile (tables de faits et de dimensions)
- **Export** vers CSV pour alimenter Power BI
- **Analyse** exploratoire intégrée (module `analyze.py`)

## Architecture du pipeline

```
scripts/
├── explore.py      # Extraction des données brutes
├── transform.py     # Nettoyage et calcul des indicateurs
├── load.py           # Connexion et chargement PostgreSQL
├── analyze.py       # Analyses exploratoires
main.py               # Orchestration du pipeline
exports/               # Fichiers CSV pour Power BI
```

## Modèle de données

| Table | Type | Description |
|---|---|---|
| `fact_order_delivery` | Fait | Grain commande — délais, statuts, dates |
| `fact_customer_repurchase` | Fait | Grain client — indicateur de réachat, retard, note |
| `dim_customers` | Dimension | Informations clients |
| `dim_products` | Dimension | Informations produits |
| `stg_order_items` | Staging | Détail des articles par commande |
| `stg_payments` | Staging | Détail des paiements |
| `stg_reviews` | Staging | Avis clients |

## Stack technique

- **Python** : Pandas, SQLAlchemy
- **Base de données** : PostgreSQL
- **Visualisation** : Power BI (mesures DAX, table de dates, modèle en étoile)
- **Gestion de config** : python-dotenv

## Installation

```bash
git clone https://github.com/<ton-user>/<ton-repo>.git
cd <ton-repo>
pip install -r requirements.txt
```

Crée un fichier `.env` à la racine avec tes identifiants PostgreSQL :

```
DB_USER=xxx
DB_PASSWORD=xxx
DB_HOST=xxx
DB_PORT=xxx
DB_NAME=xxx
```

## Utilisation

```bash
python main.py
```

Le pipeline va :
1. Tester la connexion à PostgreSQL
2. Extraire les données brutes
3. Transformer et calculer les indicateurs
4. Charger les tables dans PostgreSQL
5. Exporter les fichiers CSV dans `/exports` pour Power BI

## Dashboards Power BI

Les fichiers exportés alimentent 5 dashboards :

1. **Vue d'ensemble** — CA, panier moyen, taux de réachat, note moyenne
2. **Livraison / Logistique** — délais, retards, drill-down par commande
3. **Clients / Réachat** — taux de réachat, corrélation retard/satisfaction
4. **Produits** — top produits, CA par catégorie
5. **Paiements** — répartition des moyens de paiement

## Indicateurs clés calculés

- `delivery_delay_days` : écart entre livraison réelle et estimée
- `delivery_time_days` : durée totale entre achat et livraison
- `processing_time_days` : délai entre achat et approbation
- `has_repurchased` : le client a-t-il recommandé dans les 365 jours suivant sa 1ère commande
- `delay_bucket` : catégorisation du retard (en avance, à temps, 1-5j, 6-15j, >15j)

## Auteur

Rayen Bouajila — [rayenbouajila.me](https://rayenbouajila.me) — [LinkedIn](https://linkedin.com/in/rayenbouajilaa)