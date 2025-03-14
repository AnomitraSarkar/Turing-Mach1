import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_filter(image, kernel):
    """Applies a given filter to an image using convolution."""
    return cv2.filter2D(image, -1, kernel)

# Load the image in grayscale
image = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)

# Define custom filters (kernels)
gaussian_filter = (1/16) * np.array([[1, 2, 1],
                                     [2, 4, 2],
                                     [1, 2, 1]])

laplacian_filter = np.array([[ 0,  1,  0],
                              [ 1, -4,  1],
                              [ 0,  1,  0]])

box_filter = (1/9) * np.ones((3, 3))  # 3x3 Box Filter (Mean filter)

# Apply filters
filtered_gaussian = apply_filter(image, gaussian_filter)
filtered_laplacian = apply_filter(image, laplacian_filter)
filtered_box = apply_filter(image, box_filter)

# Plot results
fig, axes = plt.subplots(1, 4, figsize=(12, 5))
axes[0].imshow(image, cmap='gray')
axes[0].set_title("Original Image")

axes[1].imshow(filtered_gaussian, cmap='gray')
axes[1].set_title("Custom Filter")

axes[2].imshow(filtered_laplacian, cmap='gray')
# axes[2].set_title("Laplacian Filter")

# axes[3].imshow(filtered_box, cmap='gray')
# axes[3].set_title("Box Filter")

for ax in axes:
    ax.axis("off")

plt.show()
