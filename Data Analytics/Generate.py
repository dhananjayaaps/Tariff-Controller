# Import required libraries
import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
num_employees = 300
employee_ids = np.arange(1, num_employees + 1)
ages = np.random.randint(22, 30, size=num_employees)
departments = np.random.choice(['Sales', 'Marketing', 'IT', 'HR', 'Finance', 'Production'], size=num_employees)
monthly_sales = np.random.uniform(1000, 20000, size=num_employees)
performance_scores = np.random.uniform(1, 10, size=num_employees)

# Create a DataFrame
data = {
    'EmployeeID': employee_ids,
    'Age': ages,
    'Department': departments,
    'MonthlySales': monthly_sales,
    'PerformanceScore': performance_scores
}
df = pd.DataFrame(data)

# Save the dataset to a CSV file
df.to_csv('synthetic_dataset.csv', index=False)
print("Synthetic dataset has been saved as 'synthetic_dataset.csv'.")