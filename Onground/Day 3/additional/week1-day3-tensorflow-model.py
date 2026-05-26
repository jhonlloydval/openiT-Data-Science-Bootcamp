# Week 1 Day 3 - TensorFlow Model Lab

import numpy as np 
import pandas as pd 
import tensorflow as tf 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler 

#Load and clean data
training_df = pd.read_csv("week1-day3-cleaned-training-data.csv") 
print(training_df.head()) 

print(training_df.columns)


#Split Features and Target
X = training_df.drop(columns=["churned"]) 
y = training_df["churned"] 
X_values = X.to_numpy().astype("float32") 
y_values = y.to_numpy().astype("float32") 

#Train and Test
X_train, X_test, y_train, y_test = train_test_split( 
    X_values, 
    y_values, 
    test_size=0.25, 
    random_state=42, 
    stratify=y_values if len(np.unique(y_values)) > 1 else None 
    )

print("\nShape of x_train:", X_train.shape) 
print("\nShape of x_test:", X_test.shape) 
print("\nShape of y_train:",y_train.shape) 
print("\nShape of x_test:",y_test.shape) 


#Scale
scaler = StandardScaler() 
X_train_scaled = scaler.fit_transform(X_train) 
X_test_scaled = scaler.transform(X_test) 

# Answer in comments or printed output: 
# • Why should the scaler be fit on the training data only? 
# --> To prevent data leakage and keep data unseend during training
# • What problem might happen if the test data is used during scaling setup?
# --> The test data may cause a leakage or train test contamination


model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Train
history = model.fit(
    X_train_scaled, 
    y_train,
    validation_split=0.2,
    epochs=25,
    batch_size=4,
    verbose=1
)

history.history.keys()  

# Evaluate
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print("\nTest loss:", loss)
print("Test accuracy:", acc)

preds = model.predict(X_test)
classes = (preds >= 0.5).astype(int)

print("\nPredictions:", preds[:5])
print("Classes:", classes[:5])

# Optional chart
plt.plot(history.history["loss"], label="Training Loss") 
plt.plot(history.history["val_loss"], label="Validation Loss") 
plt.xlabel("Epoch") 
plt.ylabel("Loss") 
plt.legend() 
plt.title("Training and Validation Loss") 
plt.tight_layout() 
plt.savefig("week1-day3-training-loss.png") 
print("Saved chart: week1-day3-training-loss.png")


# In comments or printed output, answer: 
# What does a prediction close to 1 mean? 
# --> Prediction near 1 means it has a high chance of churn
# What does a prediction close to 0 mean? 
# --> Prediction near 0 it means it has a low chance of churn
# Is accuracy enough to judge the model? Why or why not? 
# --> Accuracy alone may be misleading if data is imbalanced.

# Save model
model.save("week1-day3-basic-tensorflow-model.keras")
loaded_model = tf.keras.models.load_model("week1-day3-basic-tensorflow-model.keras")
loaded_model.summary() 
print("\nModel saved successfully.")