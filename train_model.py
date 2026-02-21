import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

# Load data
data = pd.read_csv('hand_data.csv', header=None)
X = data.iloc[:, :-1].values.astype('float32')
y = data.iloc[:, -1].values

# Encode labels (e.g., "Chrome" becomes 0, "Volume" becomes 1)
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Simple Model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(42,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(len(np.unique(y_encoded)), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y_encoded, epochs=20)
model.save('gesture_model.h5')
print("Model Updated!")