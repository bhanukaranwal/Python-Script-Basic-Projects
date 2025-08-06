import numpy as np
import matplotlib.pyplot as plt
import pywt

# Parameters
np.random.seed(42)
TIME_STEPS = 300
WAVELET = 'db4'
THRESH = 2.5  # Z-score threshold for anomaly

# Generate a synthetic time series (with a couple of anomalies)
x = np.arange(TIME_STEPS)
y = np.sin(0.04 * np.pi * x) + 0.3*np.random.randn(TIME_STEPS)
y[80] += 6  # Insert a positive spike
y[200] -= 4  # Insert a negative drop

# Wavelet decomposition
coeffs = pywt.wavedec(y, WAVELET, level=3)
detail_coeffs = coeffs[1]  # Use level-1 details for local anomaly

# Reconstruct signal from level-1 details for anomaly detection
rec_detail = pywt.upcoef('d', detail_coeffs, WAVELET, level=1, take=len(y))

# Detect anomalies using Z-score of detail coefficients
zscore = (rec_detail - np.mean(rec_detail)) / np.std(rec_detail)
anomalies = np.where(np.abs(zscore) > THRESH)[0]

# Output summary
print(f"Detected {len(anomalies)} anomalies at indices: {anomalies.tolist()}")

# Plot
plt.figure(figsize=(12,6))
plt.subplot(211)
plt.plot(y, label='Original Signal')
plt.scatter(anomalies, y[anomalies], c='r', label='Anomaly', zorder=5)
plt.title('Time Series with Anomalies')
plt.legend()

plt.subplot(212)
plt.plot(rec_detail, label='Wavelet Detail (level 1)')
plt.axhline(THRESH*np.std(rec_detail)+np.mean(rec_detail), color='red', linestyle='--', label='Threshold')
plt.axhline(-THRESH*np.std(rec_detail)+np.mean(rec_detail), color='red', linestyle='--')
plt.title('Wavelet Detail Coefficients')
plt.legend()
plt.tight_layout()
plt.show()
