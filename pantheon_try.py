import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad

# Constants
H0 = 70  # Hubble constant in km/s/Mpc
c = 3e5  # Speed of light in km/s
Omega_m = 0.3  # Matter density parameter
Omega_L = 0.7  # Dark energy density parameter

# Function for E(z) in ΛCDM model
def E(z):
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_L)

# Proper luminosity distance in ΛCDM model
def luminosity_distance_lcdm(z):
    integral, _ = quad(lambda z_: 1/E(z_), 0, z)
    return (c / H0) * (1 + z) * integral

# Modified Photon Drag Model with only alpha
# d_L = (c/H0) * (1+z) * exp(-alpha * ln(1+z))
def luminosity_distance_drag(z, alpha):
    return (c / H0) * (1 + z) * np.exp(-alpha * np.log(1 + z))

# Load latest Pantheon+ Supernova Data from File
file_path = "/mnt/data/lcparam_full_long.txt"
df = pd.read_csv(file_path, delim_whitespace=True, comment='#')

# Ensure correct column names and check dataset structure
expected_columns = ["zcmb", "mb"]
for col in expected_columns:
    if col not in df.columns:
        raise ValueError(f"Missing expected column: {col}")

# Extract relevant columns
z_obs = df["zcmb"].values  # CMB-frame redshift
mb_obs = df["mb"].values    # Apparent magnitudes of supernovae

# Convert apparent magnitude to luminosity distance
# Standard relation: d_L (Mpc) = 10^((mb - M_ref + 5) / 5)
M_ref = -19.3  # Approximate absolute magnitude for Type Ia supernovae
d_obs = 10 ** ((mb_obs - M_ref + 5) / 5)  # Convert to distance in Mpc

# Fit the modified photon drag model to observational data
popt, _ = curve_fit(luminosity_distance_drag, z_obs, d_obs, p0=[0.1])
alpha_fit = popt[0]

# Generate redshift values for plotting
z_values = np.linspace(0.01, max(z_obs), 100)
d_lcdm = np.array([luminosity_distance_lcdm(z) for z in z_values])
d_drag = luminosity_distance_drag(z_values, alpha_fit)

# Plot comparison
plt.figure(figsize=(8, 5))
plt.plot(z_values, d_lcdm, label="ΛCDM (Dark Energy)", linestyle='dashed', color='blue')
plt.plot(z_values, d_drag, label=f"Photon Drag Model (α={alpha_fit:.3f})", color='red')
plt.scatter(z_obs, d_obs, label="Pantheon+ Supernova Data", color='black', marker='o')

plt.xlabel("Redshift (z)")
plt.ylabel("Luminosity Distance (Mpc)")
plt.legend()
plt.title("Comparison of Redshift-Distance Predictions")
plt.grid()
plt.show()

# Print fitted alpha value
print(f"Fitted Photon Drag Coefficient: α = {alpha_fit:.3f}")