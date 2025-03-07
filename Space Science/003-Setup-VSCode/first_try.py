# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Generate a random integer between 0 and 9
test_var = np.random.randint(10)
print(f"Random Integer: {test_var}")

# Set dark mode style for better visuals
plt.style.use('dark_background')

# Create a plot with labeled axes
plt.figure(figsize=(10, 8))
plt.plot([1.0, 10.0], [2.0, 5.0], color='cyan', label='Line Plot')
plt.xlabel("An X-Axis with a meaning")
plt.ylabel("The corresponding Y values")
plt.title("Random Line Plot")
plt.legend()

# Show the plot
plt.show()