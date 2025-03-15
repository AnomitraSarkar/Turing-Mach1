import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Constants
H0 = 70  # Hubble constant in km/s/Mpc
c = 3e5  # Speed of light in km/s

# Standard ΛCDM redshift-distance relation
def luminosity_distance_lcdm(z):
    return (c / H0) * (1 + z) * np.log(1 + z)

# Modified Photon Drag Model with a quadratic correction
# d_L = (c/H0) * (1+z) * exp(-alpha * ln(1+z) - beta * ln(1+z)^2)
def luminosity_distance_drag(z, alpha, beta):
    return (c / H0) * (1 + z) * np.exp(-alpha * np.log(1 + z) - beta * (np.log(1 + z))**2)

# Load latest Pantheon+ Supernova Data from File
file_path = "lcparam_full_long.txt"
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
popt, _ = curve_fit(luminosity_distance_drag, z_obs, d_obs, p0=[0.1, 0.01])
alpha_fit, beta_fit = popt

# Generate redshift values for plotting
z_values = np.linspace(0.01, max(z_obs), 100)
d_lcdm = luminosity_distance_lcdm(z_values)
d_drag = luminosity_distance_drag(z_values, alpha_fit, beta_fit)

# Plot comparison
plt.figure(figsize=(8, 5))
plt.plot(z_values, d_lcdm, label="ΛCDM (Dark Energy)", linestyle='dashed', color='blue')
plt.plot(z_values, d_drag, label=f"Photon Drag Model (α={alpha_fit:.3f}, β={beta_fit:.3f})", color='red')
plt.scatter(z_obs, d_obs, label="Pantheon+ Supernova Data", color='black', marker='o')

plt.xlabel("Redshift (z)")
plt.ylabel("Luminosity Distance (Mpc)")
plt.legend()
plt.title("Comparison of Redshift-Distance Predictions")
plt.grid()
plt.show()

# Print fitted alpha and beta values
print(f"Fitted Photon Drag Coefficients: α = {alpha_fit:.3f}, β = {beta_fit:.3f}")