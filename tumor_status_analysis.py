import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# Create plots directory if it doesn't exist
plots_dir = 'tumor_status_plots'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

# Load data from the JSON file
with open('processed_patients.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create a DataFrame
df = pd.DataFrame(data)

def clean_tumor_status(status):
    # Remove 'R0' and similar residual markers
    status = re.sub(r'R\d+', '', status)
    # Replace multiple spaces with single space
    return ' '.join(status.split())

def extract_T(tumor_status):
    # Handle both comma-separated and space-separated formats
    parts = [p.strip() for p in tumor_status.replace(',', ' ').split()]
    for part in parts:
        match = re.search(r'(?i)(?:[cp])?T\d+[a-z]?', part)
        if match:
            return match.group(0).upper()
    return None

def extract_N(tumor_status):
    parts = [p.strip() for p in tumor_status.replace(',', ' ').split()]
    for part in parts:
        match = re.search(r'(?i)(?:[cp])?N(?:\d+|x)', part)
        if match:
            return match.group(0).upper()
    return None

def extract_M(tumor_status):
    parts = [p.strip() for p in tumor_status.replace(',', ' ').split()]
    for part in parts:
        match = re.search(r'(?i)(?:[cp])?M(?:\d+[a-z]?|X)', part)
        if match:
            return match.group(0).upper()
    return None

# Clean and extract components
if 'tumor_status' in df.columns:
    df['tumor_status_clean'] = df['tumor_status'].apply(lambda x: clean_tumor_status(x) if isinstance(x, str) else x)
    df['T_stage'] = df['tumor_status'].apply(lambda x: extract_T(x) if isinstance(x, str) else None)
    df['N_stage'] = df['tumor_status'].apply(lambda x: extract_N(x) if isinstance(x, str) else None)
    df['M_stage'] = df['tumor_status'].apply(lambda x: extract_M(x) if isinstance(x, str) else None)

# 1. Raw distribution of complete tumor status
plt.figure(figsize=(12, 6))
sns.countplot(y='tumor_status_clean', data=df, order=df['tumor_status_clean'].value_counts().index)
plt.title('Complete Tumor Status Distribution')
plt.xlabel('Count')
plt.ylabel('Tumor Status')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, '1_complete_distribution.png'))
plt.close()

# 2. Individual stage distributions
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
sns.countplot(x='T_stage', data=df, order=df['T_stage'].value_counts().index, ax=ax1)
ax1.set_title('T Stage Distribution')
ax1.tick_params(axis='x', rotation=45)

sns.countplot(x='N_stage', data=df, order=df['N_stage'].value_counts().index, ax=ax2)
ax2.set_title('N Stage Distribution')
ax2.tick_params(axis='x', rotation=45)

sns.countplot(x='M_stage', data=df, order=df['M_stage'].value_counts().index, ax=ax3)
ax3.set_title('M Stage Distribution')
ax3.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, '2_individual_distributions.png'))
plt.close()

# 3. T vs N Stage Heatmap
plt.figure(figsize=(10, 8))
crosstab_tn = pd.crosstab(df['T_stage'], df['N_stage'])
sns.heatmap(crosstab_tn, annot=True, fmt='d', cmap='YlOrRd')
plt.title('T Stage vs N Stage Distribution')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, '3_t_vs_n_heatmap.png'))
plt.close()

# 4. T vs M Stage Heatmap
plt.figure(figsize=(10, 8))
crosstab_tm = pd.crosstab(df['T_stage'], df['M_stage'])
sns.heatmap(crosstab_tm, annot=True, fmt='d', cmap='YlOrRd')
plt.title('T Stage vs M Stage Distribution')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, '4_t_vs_m_heatmap.png'))
plt.close()

# 5. Stage Prefix Distribution (c/p)
def get_prefix(stage):
    if not isinstance(stage, str):
        return 'Unknown'
    match = re.match(r'^([cp])?', stage)
    return match.group(1).upper() if match and match.group(1) else 'None'

df['T_prefix'] = df['T_stage'].apply(get_prefix)
df['N_prefix'] = df['N_stage'].apply(get_prefix)
df['M_prefix'] = df['M_stage'].apply(get_prefix)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
sns.countplot(x='T_prefix', data=df, ax=ax1)
ax1.set_title('T Stage Prefix Distribution')
sns.countplot(x='N_prefix', data=df, ax=ax2)
ax2.set_title('N Stage Prefix Distribution')
sns.countplot(x='M_prefix', data=df, ax=ax3)
ax3.set_title('M Stage Prefix Distribution')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, '5_prefix_distributions.png'))
plt.close()

# 6. Stage Combinations Network
import networkx as nx
plt.figure(figsize=(12, 8))
G = nx.Graph()

# Create edges between stages that appear together
for _, row in df.iterrows():
    if row['T_stage'] and row['N_stage']:
        G.add_edge(row['T_stage'], row['N_stage'])
    if row['T_stage'] and row['M_stage']:
        G.add_edge(row['T_stage'], row['M_stage'])
    if row['N_stage'] and row['M_stage']:
        G.add_edge(row['N_stage'], row['M_stage'])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', 
        node_size=2000, font_size=10, font_weight='bold')
plt.title('Stage Combinations Network')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, '6_stage_network.png'))
plt.close()

# 7. Stacked Bar Chart of M Stage by T Stage
plt.figure(figsize=(12, 6))
crosstab_normalized = pd.crosstab(df['T_stage'], df['M_stage'], normalize='index') * 100
crosstab_normalized.plot(kind='bar', stacked=True)
plt.title('M Stage Distribution by T Stage')
plt.xlabel('T Stage')
plt.ylabel('Percentage')
plt.legend(title='M Stage')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, '7_m_stage_by_t_stage.png'))
plt.close()

# Print summary statistics
print("\nSummary Statistics:")
print("\nTotal number of patients:", len(df))
print("\nDistribution of T stages:")
print(df['T_stage'].value_counts())
print("\nDistribution of N stages:")
print(df['N_stage'].value_counts())
print("\nDistribution of M stages:")
print(df['M_stage'].value_counts()) 