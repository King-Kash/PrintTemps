import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV log file
data = pd.read_csv('./log.csv')

# Plot each layer separately
plt.figure(figsize=(10, 6))

for layer, layer_data in data.groupby('Layer'):
    plt.plot(
        layer_data['ElapsedTime(s)'],
        layer_data['Temperature(C)'],
        label=f'Layer {layer}'
    )

plt.title("Cooling Profiles by Layer")
plt.xlabel("Elapsed Time (s)")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()