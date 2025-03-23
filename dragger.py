import numpy as np
import matplotlib.pyplot as plt

# Define parameters
H0 = 2.2e-18  # Hubble constant in s^-1 (approximate)
beta_values = [1e-18, 5e-19, 1e-19, 5e-20]  # Different beta values to test
t = np.linspace(0, 1.4e10 * 3.154e7, 1000)  # Time from 0 to 14 billion years in seconds

# Compute redshift evolution for each beta
plt.figure(figsize=(8,6))
for beta in beta_values:
    z_drag = np.exp(beta * t) - 1  # Redshift from photon drag model
    plt.plot(t / (1e9 * 3.154e7), z_drag, label=f'β = {beta:.1e} s⁻¹')

# Standard ΛCDM redshift evolution
z_lcdm = np.exp(H0 * t) - 1
plt.plot(t / (1e9 * 3.154e7), z_lcdm, 'k--', label='ΛCDM (H0 = 2.2e-18 s⁻¹)')

# Labels and legend
plt.xlabel('Time (Billion Years)')
plt.ylabel('Redshift (z)')
plt.title('Redshift Evolution in Photon Drag Model vs ΛCDM')
plt.legend()
plt.grid(True)
plt.yscale('log')  # Log scale to show differences better

# Show plot
plt.show()
