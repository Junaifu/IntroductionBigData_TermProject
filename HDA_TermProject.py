import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style
style.use("ggplot")

data = pd.read_csv('../input/heart-disease-health-indicators-dataset/heart_disease_health_indicators_BRFSS2015.csv')

data.drop_duplicates(inplace=True)
HDA = "HeartDiseaseorAttack"
Education = "Education"
unwantedColumns = ["CholCheck", "Stroke", "HvyAlcoholConsump", "AnyHealthcare", "GenHlth", "MentHlth", "PhysHlth", "BMI"]
filteredColumns = [e for e in data.columns if e not in unwantedColumns]

filteredColumnsLen = len(filteredColumns)

fig, axes = plt.subplots(nrows=filteredColumnsLen, ncols=1, figsize=(20,13*filteredColumnsLen))


for i in range(len(filteredColumns)):
    col = filteredColumns[i]
    sns.countplot(x=col, data=data, hue=HDA, palette="seismic", ax=axes[i])
    axes[i].legend([f"No_HDA: {data[data[HDA]==0.0][col].mean():.2f}", f"HDA: {data[data[HDA]==1.0][col].mean():.2f}"],
                   fontsize=15,
                   title=f"{col} average",
                   title_fontsize=20)
axes[0].legend([])
plt.show()

if (HDA not in filteredColumns):
    filteredColumns.insert(0, HDA)
if (Education in filteredColumns):
    filteredColumns.remove(Education)

for i in range(len(filteredColumns)):
    col = filteredColumns[i]
    prop_df = (data[col]
               .groupby(data[Education])
               .value_counts(normalize=True)
               .mul(100)
               .rename(y)
               .reset_index()).sort_values(by=[Education, col])
    fg = sns.catplot(x=col, y=y,
                hue=Education,
                data=prop_df, kind="bar",
                height=8, aspect=2);
    fg.fig.subplots_adjust(top=0.95)
    fg.fig.suptitle(col + " per category of " + Education + " in " + y)
    for ax in fg.axes.ravel():
        counter = 0
        for c in ax.containers:
            labels = []
            for v in c:
                labels.append(f'{prop_df[y][prop_df.index[counter]]:.2f}%')
                if (counter < len(prop_df[col]) - 1):
                    counter += 1
            ax.bar_label(c, labels=labels, label_type='edge')
plt.show()

onlyHaveHDAData = data[data[HDA] == 1.0]
if (Education in filteredColumns):
    filteredColumns.remove(Education)

for i in range(len(filteredColumns)):
    col = filteredColumns[i]
    prop_df = (onlyHaveHDAData[col]
               .groupby(data[Education])
               .value_counts(normalize=True, dropna=False)
               .reindex(fill_value=0)
               .mul(100)
               .rename(y)
               .reset_index()).sort_values(by=[Education, col])
    fg = sns.catplot(x=col, y=y,
                hue=Education,
                data=prop_df, kind="bar",
                height=8, aspect=2);
    fg.fig.subplots_adjust(top=0.95)
    fg.fig.suptitle(col + " per category of " + Education + " in " + y + " among people who had Heart Disease or Attack")
    if (col != "Age" and col != "Income"):
        for ax in fg.axes.ravel():
            counter = 0
            for c in ax.containers:
                labels = []
                for v in c:
                    labels.append(f'{prop_df[y][prop_df.index[counter]]:.2f}%')
                    if (counter < len(prop_df[col]) - 1):
                        counter += 1
                ax.bar_label(c, labels=labels, label_type='edge')
plt.show()