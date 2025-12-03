import pandas as pd
import numpy as np

# Data as a dictionary
data = {
    'student': ['Aiden', 'Aiden', 'Bella', 'Bella', 'Bella', 'Will', 'Louis', 'Will', 'Louis', 'Will', 'Gabby', 'Gabby', 'Gabby', 'Gabby', 'Eli', 'Aiden', 'Bella', 'Bella', 'Aiden', 'Bella', 'Will', 'Will', 'Louis', 'Will', 'Will', 'Gabby', 'Gabby', 'Gabby', 'Eli', 'Eli'],
    'date': ['27_07', '24_07', '27_07', '23_07', '02_08', '24_07', '26_07', '29_07', '01_08', '23_07', '26_07', '03_08', '01_08', '23_07', '24_07', '29_07', '29_07', '03_08', '24_07', '28_07', '23_07', '30_07', '25_07', '27_07', '02_08', '02_08', '23_07', '25_07', '30_07', '02_08'],
    'day': ['su', 'th', 'su', 'w', 'sa', 'th', 'sa', 't', 'f', 'w', 'sa', 'su', 'f', 'w', 'th', 't', 't', 'su', 'th', 'm', 'w', 'w', 'f', 'su', 'sa', 'sa', 'w', 'f', 'w', 'sa'],
    'place': ['bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'bris', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd'],
    'source': ['app', 'app', 'app', 'app', 'app', 'TV news', 'TV news', 'TV news', 'TV news', 'TV news', 'web', 'web', 'web', 'web', 'web', 'app', 'app', 'app', 'app', 'app', 'TV news', 'TV news', 'TV news', 'TV news', 'TV news', 'web', 'web', 'web', 'web', 'web'],
    'minf': [12, 9, 9, 9, 7, 10, 12, 7, 11, 13, 8, 10, 10, 9, 10, 9, 9, 13, 8, 9, 12, 9, 6, 11, 11, 10, 7, 12, 10, 11],
    'maxf': [20, 19, 20, 22, 18, 21, 23, 22, 20, 22, 20, 21, 19, 22, 21, 17, 18, 16, 16, 18, 19, 15, 18, 19, 17, 20, 21, 18, 15, 18],
    'rainf': ['yes', 'no', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes'],
    'rain': ['no', 'no', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes']
}

# Create DataFrame
df = pd.DataFrame(data)

# Group by source and place, calculate statistics for maxf
table = df.groupby(['source', 'place'])['maxf'].agg(
    Mean='mean',
    Max='max',
    SD='std',
    Count='count'
).reset_index()

# Round Mean and SD to 2 decimal places
table['Mean'] = table['Mean'].round(2)
table['SD'] = table['SD'].round(2)

# Print the table
print("\nTable: Mean, Max, SD, and Count of maxf (°C) by Source and Place\n")
print(table.to_string(index=False))