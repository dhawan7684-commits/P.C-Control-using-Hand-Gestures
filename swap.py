import pandas as pd

# Load your data
df = pd.read_csv('hand_data.csv', header=None)

# Swap 5 and 6
# We use a temporary placeholder (-1) so we don't overwrite everything at once
df[0] = df[0].replace({5: -1, 6: 5})
df[0] = df[0].replace({-1: 6})

# Save it back
df.to_csv('hand_data.csv', index=False, header=None)
print("Labels 5 and 6 swapped successfully!")