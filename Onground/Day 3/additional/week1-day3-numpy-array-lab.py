import numpy as np

scores = np.array([72, 88, 91, 65, 79, 95]) 
monthly_sales = np.array([ 
[1200, 1350, 1280], 
[1500, 1420, 1600], 
[980, 1100, 1050], 
[1750, 1680, 1800] 
])  

print("Score propeties:")
print("Shape:", scores.shape, "\nData Type:", scores.dtype, "\nDimensions", scores.ndim, "\nSize:", scores.size) 

print("\nMonthly Sales Properties:")
print("Shape:", monthly_sales.shape, "\nData Type:", monthly_sales.dtype, "\nDimensions", monthly_sales.ndim, "\nSize:", monthly_sales.size) 


#Indexing
print("\nIndexing")
print("First score:", scores[0])
print("Last score:", scores[-1])
print("First three:", scores[:3])
print("Scores >= 80:", scores[scores >= 80])

print("\nMonthly Sales array")
print("First row:", monthly_sales[0])
print("Second Column:", monthly_sales[-1])
print("Row 2, column 3:", "\n" , monthly_sales[:3])
print("First two rows and all columns:", monthly_sales[monthly_sales >= 80])

# Vectorized Operations 
curved_scores = np.minimum(scores + 5, 100)
print("\nCurved scores:", curved_scores)

passed = curved_scores >= 75
print("Passed mask:", passed)

print("Average original:", np.mean(scores))
print("Average curved:", np.mean(curved_scores))
print("Max curved:", np.max(curved_scores))
print("Passing count:", np.sum(passed))

# Aggregate Across Axes 
sales_by_person = monthly_sales.sum(axis=1)
sales_by_month = monthly_sales.sum(axis=0)
overall_sales = monthly_sales.sum()

print("\nSales by person:", sales_by_person)
print("Sales by month:", sales_by_month)
print("Overall sales:", overall_sales)

# Broadcasting
monthly_bonus = np.array([100, 150, 200])
adjusted_sales = monthly_sales + monthly_bonus

print("\nAdjusted sales:\n", adjusted_sales)

# Why did NumPy allow a 1D array with 3 values to be added to a 4 by 3 array?
# --> NumPy can add a 1D array to a 2D array using broadcasting.
# Which dimension did the bonus values align with? 
# --> The 3 bonus values correspond to the 3 columns. They are added to each column.
