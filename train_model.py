import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras import layers, models

# 1. Load the data
df = pd.read_csv('hand_data.csv', header=None)
X = df.iloc[:, 1:].values  # The 42 coordinates
y = df.iloc[:, 0].values   # The Label (0-8)

# 2. Split into Training (80%) and Testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Build the CNN/Dense Model
model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(42,)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(10, activation='softmax') # 9 output classes for your 9 gestures
])

model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

# 4. Train
print("Starting training...")
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# 5. Save the brain!
model.save('gesture_model.h5')
print("Model saved as gesture_model.h5")