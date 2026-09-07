import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load dataset
df = pd.read_csv("ml/wait_time_dataset.csv")

# Features and target
X = df.drop("waiting_time", axis=1)
y = df["waiting_time"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Models
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    ),
}


best_model = None
best_model_name = None
best_r2 = float("-inf")


# Train and evaluate
for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print(f"\n{name}")
    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")

    # Select best model using R²
    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_model_name = name


# Save best model
model_path = "ml/wait_time_model.pkl"

joblib.dump(best_model, model_path)

print("\n----------------------------")
print(f"Best Model : {best_model_name}")
print(f"R²         : {best_r2:.4f}")
print(f"Saved to   : {model_path}")
print("----------------------------")