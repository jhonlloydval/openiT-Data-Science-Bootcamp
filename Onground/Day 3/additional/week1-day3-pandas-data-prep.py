import numpy as np 
import pandas as pd


df = pd.DataFrame({ 
    "customer_id": [101, 102, 103, 104, 105, 106, 107, 108], 
    "region": ["North", "South", "North", "East", "West", "South", "East", 
               "West"], 
               "plan_type": ["Basic", "Premium", "Basic", "Premium", "Basic", "Premium", 
                             "Basic", "Premium"], 
                             "monthly_fee": [29.99, 59.99, 29.99, 59.99, 29.99, None, 29.99, 59.99], 
                             "usage_hours": [12, 45, 18, 50, 9, 38, None, 41], 
                             "support_tickets": [1, 3, 0, 4, 2, 1, 0, 2], 
                             "churned": [0, 1, 0, 1, 0, 0, 0, 1] 
                             })


print(df.head()) 
print(df.tail()) 
df.info() 
print(df.describe(include="all")) 
print(df.isna().sum())

# In comments or printed output, answer: 
# • How many rows and columns are in the dataset? 
# --> The original dataset has 8 rows and 7 columns however, after encoding categorial variables, the number of columns increases. 
# • Which columns are numeric? 
# -->  Numeric columns: customer_id, monthly_fee, usage_hours, support_tickets, churned.
# • Which columns are categorical? 
# --> Categorical columns are region, plan_type.
# • Which columns contain missing values? 
# --> Missing values are in the monthly_fee and usage_hours.
# • Which column appears to be the target variable? 
# --> The target variable is "churned" since it's what we want to predict.


clean_df = df.copy() 

numeric_cols = clean_df.select_dtypes(include=["number"]).columns 
clean_df[numeric_cols] = clean_df[numeric_cols].fillna(clean_df[numeric_cols].median())


text_cols = clean_df.select_dtypes(include=["object"]).columns 
clean_df[text_cols] = clean_df[text_cols].fillna("Unknown")


print(clean_df.isna().sum()) 

print(clean_df.dtypes)

print(clean_df["region"].value_counts()) 
print(clean_df["plan_type"].value_counts()) 

clean_df["region"] = clean_df["region"].str.strip().str.title() 
clean_df["plan_type"] = clean_df["plan_type"].str.strip().str.title() 

# Summary tables
plan_summary = clean_df.groupby("plan_type").agg(
    customers=("customer_id", "count"),
    avg_monthly_fee=("monthly_fee", "mean"),
    avg_usage_hours=("usage_hours", "mean"),
    churn_rate=("churned", "mean")
)

print("\nPlan summary:\n", plan_summary)

region_summary = clean_df.groupby("region").agg(
    customers=("customer_id", "count"),
    total_support_tickets=("support_tickets", "sum"),
    churn_rate=("churned", "mean")
)

print("\nRegion summary:\n", region_summary)

# Feature prep for Tensorflow
feature_df = clean_df[["region", "plan_type", "monthly_fee", "usage_hours", "support_tickets"]]
target = clean_df["churned"]

feature_df = pd.get_dummies(feature_df, columns=["region", "plan_type"])

print("\nFeature types:\n", feature_df.dtypes)

training_df = feature_df.copy()
training_df["churned"] = target

print(training_df.head())

# Save CSV
training_df.to_csv("week1-day3-cleaned-training-data.csv", index=False)

print("\nSaved cleaned dataset.")