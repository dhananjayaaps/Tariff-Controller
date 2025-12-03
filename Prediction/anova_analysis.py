import pandas as pd
import numpy as np
from scipy import stats

# Dataset
# data = {
#     'student': ['Gabby', 'Gabby', 'Bella', 'Bella', 'Gabby', 'Aiden', 'Will', 'Gabby', 'Will', 'Aiden', 
#                 'Aiden', 'Eli', 'Aiden', 'Gabby', 'Will', 'Gabby', 'Eli', 'Gabby', 'Louis', 'Aiden', 
#                 'Bella', 'Louis', 'Aiden', 'Eli', 'Eli', 'Eli', 'Bella', 'Louis', 'Gabby', 'Eli', 
#                 'Will', 'Louis', 'Aiden', 'Aiden', 'Bella', 'Gabby', 'Eli', 'Gabby', 'Aiden', 'Eli', 
#                 'Eli', 'Louis', 'Aiden', 'Gabby'],
#     'date': ['29_07', '23_07', '02_08', '25_07', '28_07', '27_07', '28_07', '02_08', '30_07', '25_07', 
#              '03_08', '25_07', '28_07', '25_07', '31_07', '25_07', '23_07', '27_07', '30_07', '31_07', 
#              '31_07', '23_07', '24_07', '27_07', '25_07', '31_07', '29_07', '27_07', '26_07', '02_08', 
#              '30_07', '31_07', '01_08', '30_07', '01_08', '01_08', '01_08', '30_07', '25_07', '03_08', 
#              '27_07', '26_07', '29_07', '03_08'],
#     'day': ['t', 'w', 'sa', 'f', 'm', 'su', 'm', 'sa', 'w', 'f', 'su', 'f', 'm', 'f', 'th', 'f', 'w', 
#             'su', 'w', 'th', 'th', 'w', 'th', 'su', 'f', 'th', 't', 'su', 'sa', 'sa', 'w', 'th', 'f', 
#             'w', 'f', 'f', 'f', 'w', 'f', 'su', 'su', 'sa', 't', 'su'],
#     'place': ['syd', 'bris', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'syd', 'bris', 'syd', 'bris', 
#               'bris', 'bris', 'syd', 'syd', 'bris', 'syd', 'syd', 'bris', 'bris', 'bris', 'bris', 'bris', 
#               'syd', 'bris', 'syd', 'bris', 'syd', 'bris', 'bris', 'syd', 'syd', 'syd', 'bris', 'bris', 
#               'syd', 'bris', 'syd', 'syd', 'syd', 'syd', 'bris', 'bris'],
#     'source': ['web', 'web', 'app', 'app', 'web', 'app', 'TV news', 'web', 'TV news', 'app', 'app', 'web', 
#                'app', 'web', 'TV news', 'web', 'web', 'web', 'TV news', 'app', 'app', 'TV news', 'app', 
#                'web', 'web', 'web', 'app', 'TV news', 'web', 'web', 'TV news', 'TV news', 'app', 'app', 
#                'app', 'web', 'web', 'web', 'app', 'web', 'web', 'TV news', 'app', 'web'],
#     'maxf': [18, 22, 16, 17, 18, 17, 18, 20, 15, 21, 16, 22, 19, 22, 16, 18, 22, 19, 15, 19, 19, 
#              22, 19, 22, 18, 21, 19, 17, 19, 19, 24, 16, 13, 13, 18, 19, 15, 22, 17, 18, 19, 19, 20, 21]
# }

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

df = pd.DataFrame(data)

# Grand mean
mu = df['maxf'].mean()

# Group means
source_means = df.groupby('source')['maxf'].mean()
place_means = df.groupby('place')['maxf'].mean()
source_place_means = df.groupby(['source', 'place'])['maxf'].mean()
source_counts = df.groupby('source').size()
place_counts = df.groupby('place').size()
source_place_counts = df.groupby(['source', 'place']).size()

# Total Sum of Squares (SST)
sst = sum((df['maxf'] - mu) ** 2)

# --- Preliminary ANOVA ---
# Source Sum of Squares
ss_source = sum(source_counts[i] * (source_means[i] - mu) ** 2 for i in source_means.index)

# Place Sum of Squares
ss_place = sum(place_counts[j] * (place_means[j] - mu) ** 2 for j in place_means.index)

# Residual Sum of Squares (Preliminary)
# Fitted values: mu + alpha_i + beta_j
source_effects = source_means - mu
place_effects = place_means - mu
df['fitted_prelim'] = df.apply(
    lambda row: mu + source_effects[row['source']] + place_effects[row['place']], axis=1
)
ss_residual_prelim = sum((df['maxf'] - df['fitted_prelim']) ** 2)

# Degrees of Freedom
n = len(df)
I = len(source_means)  # Number of sources
J = len(place_means)   # Number of places
df_source = I - 1
df_place = J - 1
df_residual_prelim = n - I - J + 1
df_total = n - 1

# Mean Squares
ms_source = ss_source / df_source
ms_place = ss_place / df_place
ms_residual_prelim = ss_residual_prelim / df_residual_prelim

# F-statistics
f_source = ms_source / ms_residual_prelim
f_place = ms_place / ms_residual_prelim

# p-values
p_source = 1 - stats.f.cdf(f_source, df_source, df_residual_prelim)
p_place = 1 - stats.f.cdf(f_place, df_place, df_residual_prelim)

# --- Factorial ANOVA ---
# Interaction Sum of Squares
ss_interaction = sum(
    source_place_counts.get((i, j), 0) * (source_place_means.get((i, j), mu) - mu - 
                                          source_effects[i] - place_effects[j]) ** 2 
    for i in source_means.index for j in place_means.index
)

# Residual Sum of Squares (Factorial)
# Fitted values: mu + alpha_i + beta_j + gamma_ij
df['fitted_factorial'] = df.apply(
    lambda row: source_place_means.get((row['source'], row['place']), mu), axis=1
)
ss_residual_factorial = sum((df['maxf'] - df['fitted_factorial']) ** 2)

# Degrees of Freedom
df_interaction = (I - 1) * (J - 1)
df_residual_factorial = n - I * J

# Mean Squares
ms_interaction = ss_interaction / df_interaction
ms_residual_factorial = ss_residual_factorial / df_residual_factorial

# F-statistics
f_source_factorial = ms_source / ms_residual_factorial
f_place_factorial = ms_place / ms_residual_factorial
f_interaction = ms_interaction / ms_residual_factorial

# p-values
p_source_factorial = 1 - stats.f.cdf(f_source_factorial, df_source, df_residual_factorial)
p_place_factorial = 1 - stats.f.cdf(f_place_factorial, df_place, df_residual_factorial)
p_interaction = 1 - stats.f.cdf(f_interaction, df_interaction, df_residual_factorial)

# Output ANOVA Tables
print("Preliminary ANOVA:")
print(f"{'Source':<15} {'df':<5} {'SS':<10} {'MS':<10} {'F':<10} {'p-value':<10}")
print(f"{'source':<15} {df_source:<5} {ss_source:.2f} {ms_source:.3f} {f_source:.3f} {p_source:.4f}")
print(f"{'place':<15} {df_place:<5} {ss_place:.2f} {ms_place:.3f} {f_place:.3f} {p_place:.4f}")
print(f"{'Error':<15} {df_residual_prelim:<5} {ss_residual_prelim:.2f} {ms_residual_prelim:.3f} {'':<10} {'':<10}")
print(f"{'Total':<15} {df_total:<5} {sst:.2f} {'':<10} {'':<10} {'':<10}\n")

print("Factorial ANOVA:")
print(f"{'Source':<15} {'df':<5} {'SS':<10} {'MS':<10} {'F':<10} {'p-value':<10}")
print(f"{'source':<15} {df_source:<5} {ss_source:.2f} {ms_source:.3f} {f_source_factorial:.3f} {p_source_factorial:.4f}")
print(f"{'place':<15} {df_place:<5} {ss_place:.2f} {ms_place:.3f} {f_place_factorial:.3f} {p_place_factorial:.4f}")
print(f"{'source:place':<15} {df_interaction:<5} {ss_interaction:.2f} {ms_interaction:.3f} {f_interaction:.3f} {p_interaction:.4f}")
print(f"{'Error':<15} {df_residual_factorial:<5} {ss_residual_factorial:.2f} {ms_residual_factorial:.3f} {'':<10} {'':<10}")
print(f"{'Total':<15} {df_total:<5} {sst:.2f} {'':<10} {'':<10} {'':<10}")