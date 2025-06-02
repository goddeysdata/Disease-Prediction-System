from sklearn.tree import DecisionTreeClassifier
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load your dataset
df = pd.read_csv('models/dataset.csv')  # Ensure the correct path

# Encode categorical variables (convert text to numbers)
encoder = LabelEncoder()
for col in df.select_dtypes(include=['object']).columns:
    df[col] = encoder.fit_transform(df[col])

# Prepare features (X) and target variable (y)
X_train = df.drop(columns=['Disease'])  # Ensure this is the actual target column
y_train = df['Disease']  # Ensure correct target column is used

# Train Decision Tree model
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Save the trained model
joblib.dump(clf, 'models/model.pkl')


print("Model training completed and saved as 'model.pkl'.")
