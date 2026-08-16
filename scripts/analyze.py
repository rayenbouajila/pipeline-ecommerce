import pandas as pd
from scipy.stats import chi2_contingency
import statsmodels.formula.api as smf

def run_analysis(df):
    df = df.dropna(subset=["delivery_delay_days", "review_score"])

    # Taux de réachat par bucket
    print(df.groupby("delay_bucket")["has_repurchased"].mean())

    # Test khi-2 : le statut de livraison est-il indépendant du réachat ?
    contingency = pd.crosstab(df["delay_bucket"], df["has_repurchased"])
    chi2, p, dof, _ = chi2_contingency(contingency)
    print(f"\nChi2 p-value: {p:.5f}")

    # Régression logistique : effet du délai en contrôlant par review_score
    model = smf.logit(
        "has_repurchased ~ delivery_delay_days + review_score", data=df
    ).fit()
    print(model.summary())

    return model