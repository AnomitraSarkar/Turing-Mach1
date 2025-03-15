import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Grid size
size = 120  # 100x100 grid
c = 3.0  # Wave speed
dt = 0.1  # Time step
dx = 1.0  # Grid spacing
damping = 0.995  # Damping factor to simulate viscosity

# Smoothing factor for direction stability
smooth_factor = 0.9
previous_direction = None

# Initialize wave state
def ripple_wave():
    return np.zeros((size, size))

current = ripple_wave()
previous = np.copy(current)

agent_x, agent_y = size // 2, size // 2  # Default ripple origin
observer_x, observer_y = 50, 50  # Observer at origin
agent_length = 5  # Horizontal length of agent

detection_time = None  # Track first detection time
angles = []  # Store detected wave directions
frames = []  # Store frame numbers

def on_key(event):
    global observer_x, observer_y, agent_x, agent_y, current
    if event.key == 'up' and observer_y > 0:
        observer_y -= 1
    elif event.key == 'down' and observer_y < size - 1:
        observer_y += 1
    elif event.key == 'left' and observer_x > 0:
        observer_x -= 1
    elif event.key == 'right' and observer_x < size - 1:
        observer_x += 1
    elif event.key in ['w', 'x', 'a', 'd', 'space']:
        if event.key == 'w' and agent_y > 0:
            agent_y -= 1
        elif event.key == 'x' and agent_y < size - 1:
            agent_y += 1
        elif event.key == 'a' and agent_x > 0:
            agent_x -= 1
        elif event.key == 'd' and agent_x < size - 1:
            agent_x += 1
        
        # Generate a wave across the agent's length
        for i in range(-agent_length // 2, agent_length // 2 + 1):
            if 0 <= agent_x + i < size:
                current[agent_y, agent_x + i] = 1
    elif event.key == 's':
        return  # Prevent save dialog by doing nothing on 's' key
    print(f"Observer at ({observer_x}, {observer_y}), Agent at ({agent_x}, {agent_y})")

fig, ax = plt.subplots(figsize=(6, 6))
cmap = ax.imshow(current, cmap='coolwarm', vmin=-1, vmax=1)
observer_dot, = ax.plot(observer_x, observer_y, 'ro', markersize=5)  # Red dot for observer
direction_line, = ax.plot([], [], 'g-', linewidth=2)  # Green line for direction
fig.canvas.mpl_connect('key_press_event', on_key)

def update(frame):
    global current, previous, detection_time, previous_direction
    next_grid = np.copy(current)
    
    # Apply the 2D wave equation (finite difference method) with damping
    laplacian = (
        np.roll(current, 1, axis=0) + np.roll(current, -1, axis=0) +
        np.roll(current, 1, axis=1) + np.roll(current, -1, axis=1) - 4 * current
    )
    next_grid = damping * (2 * current - previous + (c**2 * dt**2 / dx**2) * laplacian)
    
    # Check if any disturbance is detected by the observer
    if abs(current[observer_y, observer_x]) > 0.001:  # Threshold to ignore small disturbances
        if detection_time is None:
            detection_time = frame  # Set the time of first detection
        
        # Compute tangential direction to the wavefront using gradients
        grad_x = -(np.roll(current, -1, axis=1) - np.roll(current, 1, axis=1)) / 2.0
        grad_y = -(np.roll(current, -1, axis=0) - np.roll(current, 1, axis=0)) / 2.0
        best_dx, best_dy = grad_x[observer_y, observer_x], grad_y[observer_y, observer_x]
        
        direction = np.arctan2(best_dy, best_dx)  # Direction in radians
        
        # Apply smoothing to stabilize direction
        if previous_direction is not None:
            direction = smooth_factor * previous_direction + (1 - smooth_factor) * direction
        previous_direction = direction
        
        print(f"Disturbance detected at observer ({observer_x}, {observer_y}) at frame {frame}, wave coming from {np.degrees(direction):.2f} degrees")
        
        # Draw direction line from observer
        end_x = observer_x - 5 * np.cos(direction)
        end_y = observer_y - 5 * np.sin(direction)
        direction_line.set_data([observer_x, end_x], [observer_y, end_y])
    
    previous = np.copy(current)
    current = np.copy(next_grid)
    cmap.set_array(current)
    observer_dot.set_data(observer_x, observer_y)
    
    return [cmap, observer_dot, direction_line]

ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)
plt.show()
