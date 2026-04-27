import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

# -------------------------------
# Load datasets
# -------------------------------
train_path = "../dataset/Training.csv"
test_path  = "../dataset/Testing.csv"

train_df = pd.read_csv(train_path)
test_df  = pd.read_csv(test_path)

# Drop any unnamed columns that pandas adds automatically
train_df = train_df.loc[:, ~train_df.columns.str.contains('^Unnamed')]
test_df  = test_df.loc[:, ~test_df.columns.str.contains('^Unnamed')]

# -------------------------------
# Split features and labels
# -------------------------------
X_train = train_df.drop("prognosis", axis=1)
y_train = train_df["prognosis"]

X_test = test_df.drop("prognosis", axis=1)
y_test = test_df["prognosis"]

# Align test features with training features
X_test = X_test[X_train.columns]

# -------------------------------
# Train the model
# -------------------------------
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

# -------------------------------
# Evaluate accuracy
# -------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy}")

# -------------------------------
# Ensure model folder exists
# -------------------------------
model_folder = "../model"
os.makedirs(model_folder, exist_ok=True)

# -------------------------------
# Save the model and symptom list
# -------------------------------
model_file = os.path.join(model_folder, "model.pkl")
symptom_file = os.path.join(model_folder, "symptoms.pkl")

pickle.dump(model, open(model_file, "wb"))
pickle.dump(list(X_train.columns), open(symptom_file, "wb"))

print("✅ Model and symptom list saved successfully!")