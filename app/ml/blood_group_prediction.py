# import random

# def predict_next_donor(blood_counts):
#     """
#     Takes blood group counts and predicts next donor counts
#     """
#     predictions = {}
#     for group, count in blood_counts.items():
#         predictions[group] = count + random.randint(0, 3)
#     return predictions

# import pandas as pd
# from app.models import Donor  # your model

# def predict_next_donor():
#     # Fetch donor data
#     donors = Donor.objects.all().values("blood_group")
#     df = pd.DataFrame(donors)

#     if df.empty:
#         return pd.DataFrame(columns=["blood_group", "probability"])

#     # Count donors per blood group
#     counts = df["blood_group"].value_counts().reset_index()
#     counts.columns = ["blood_group", "count"]

#     # Convert counts to probabilities (between 0 and 1)
#     total = counts["count"].sum()
#     counts["probability"] = counts["count"] / total

#     # Sort from highest to lowest probability
#     counts = counts.sort_values(by="probability", ascending=False).reset_index(drop=True)

#     return counts[["blood_group", "probability"]]
import pandas as pd
from app.models import Donor  # your donor model

def predict_next_donor():
    """
    Returns a DataFrame with blood groups and their probabilities
    based on number of donors.
    """
    # Fetch all donors
    donors = Donor.objects.all().values("blood_group")
    df = pd.DataFrame(donors)

    if df.empty:
        return pd.DataFrame(columns=["blood_group", "probability"])

    # Count donors per blood group
    counts = df["blood_group"].value_counts().reset_index()
    counts.columns = ["blood_group", "count"]

    # Convert counts to probability
    total = counts["count"].sum()
    counts["probability"] = counts["count"] / total

    # Sort from highest to lowest probability
    counts = counts.sort_values(by="probability", ascending=False).reset_index(drop=True)

    return counts[["blood_group", "probability"]]



