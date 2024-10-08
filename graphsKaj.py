import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# labels = np.array(["Pneumonia", "Myocardial Infarction", "Stroke",					
#             "Covid-19",	"Atrial Fibrillation", "Femer Fracture", "Endocrine, Nutritional and Metabolic Diseases",					
#             "Other Pulmonary Disease"])
# zero = np.array([0.018408, 0.000048, 0.0008, 0.032112, 0.000093, 0.010456, 0.039002, 0.000608])
# ten = np.array([0.004256, 0.000036, 0.00085, 0.015531, 0.000822, 0.008126, 0.043393, 0.000227])
# twenty = np.array([0.010121, 0.001236, 0.004079, 0.051875, 0.004908, 0.007341, 0.05466, 0.000567])
# thirty = np.array([0.019732, 0.012881, 0.012443, 0.093188, 0.013876, 0.008092, 0.074321, 0.003987])
# fourty = np.array([0.032541, 0.061737, 0.036318, 0.110624, 0.035552, 0.011909, 0.096695, 0.02579])
# fifty = np.array([0.071616, 0.178239, 0.100152, 0.141331, 0.120503, 0.033538, 0.158375, 0.102994])
# sixty = np.array([0.132417, 0.232617, 0.164398, 0.148221, 0.208803, 0.078518, 0.174663, 0.232143])
# seventy = np.array([0.257947, 0.261483, 0.273102, 0.184304, 0.313501, 0.22427, 0.185326, 0.367922])
# eighty = np.array([0.311395, 0.198051, 0.301036, 0.164978, 0.237352, 0.403928, 0.137744, 0.225822])
# ninety = np.array([0.141568, 0.053671, 0.106823, 0.057836, 0.06459, 0.213823, 0.03582, 0.039941])

# width = 0.7       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()

# ax.bar(labels, zero, width, bottom = zero, label='0-9')
# ax.bar(labels, ten, width, bottom = zero + ten, label='10-19')
# ax.bar(labels, twenty, width, bottom = zero + ten + twenty, label='20-29')
# ax.bar(labels, thirty, width, bottom = zero + ten + twenty + thirty, label='30-39')
# ax.bar(labels, fourty, width, bottom = zero + ten + twenty + thirty + fourty, label='40-49')
# ax.bar(labels, fifty, width, bottom = zero + ten + twenty + thirty + fourty + fifty, label='50-59')
# ax.bar(labels, sixty, width, bottom = zero + ten + twenty + thirty + fourty + fifty + sixty, label='60-69')
# ax.bar(labels, seventy, width, bottom = zero + ten + twenty + thirty + fourty + fifty + sixty + seventy, label='70-79')
# ax.bar(labels, eighty, width, bottom = zero + ten + twenty + thirty + fourty + fifty + sixty + seventy + eighty, label='80-89')
# ax.bar(labels, ninety, width, bottom = zero + ten + twenty + thirty + fourty + fifty + sixty + seventy + eighty + ninety, label='90+')

# ax.set_xlabel('Condition')
# ax.set_title('Proportion of Age Groups with Each Condition')
# ax.legend()

# plt.show()

plt.rcParams.update({"text.usetex": True, 'font.size': 14})

width = 0.9

df = pd.DataFrame({'0-9': [0.018408, 0.000048, 0.0008, 0.032112, 0.000093, 0.010456, 0.039002, 0.000608],
                   '10-19': [0.004256, 0.000036, 0.00085, 0.015531, 0.000822, 0.008126, 0.043393, 0.000227],
                   '20-29': [0.010121, 0.001236, 0.004079, 0.051875, 0.004908, 0.007341, 0.05466, 0.000567],
                   '30-39': [0.019732, 0.012881, 0.012443, 0.093188, 0.013876, 0.008092, 0.074321, 0.003987],
                   '40-49': [0.032541, 0.061737, 0.036318, 0.110624, 0.035552, 0.011909, 0.096695, 0.02579],
                   '50-59': [0.071616, 0.178239, 0.100152, 0.141331, 0.120503, 0.033538, 0.158375, 0.102994],
                   '60-69': [0.132417, 0.232617, 0.164398, 0.148221, 0.208803, 0.078518, 0.174663, 0.232143],
                   '70-79': [0.257947, 0.261483, 0.273102, 0.184304, 0.313501, 0.22427, 0.185326, 0.367922],
                   '80-89': [0.311395, 0.198051, 0.301036, 0.164978, 0.237352, 0.403928, 0.137744, 0.225822],
                   '90+': [0.141568, 0.053671, 0.106823, 0.057836, 0.06459, 0.213823, 0.03582, 0.039941]},
                index = ["Pneumonia", "Myocardial Infarction", "Stroke", "Covid-19",	"Atrial Fibrillation", "Femur Fracture", "Nutritional \& Metabolic Diseases","Other Pulmonary Disease"])
ax = df.plot(kind='bar', stacked=True, width = width, figsize = (10, 7))
plt.xlabel('Condition')
plt.ylabel('Proportion')
plt.title('Proportion of Age Groups with Each Condition')
plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()

# MALE/FEMALE
df = pd.DataFrame({'Male': [0.506, 0.666, 0.526, 0.533, 0.541, 0.327, 0.497, 0.450],
                  'Female': [0.494, 0.334, 0.474, 0.467, 0.458, 0.673, 0.502, 0.550]},
                index = ["Pneumonia", "Myocardial Infarction", "Stroke", "Covid-19",	"Atrial Fibrillation", "Femur Fracture", "Nutritional \& Metabolic Diseases","Other Pulmonary Disease"])
ax = df.plot(kind='bar', stacked=True, width = width, figsize = (10, 7))
plt.xlabel('Condition')
plt.ylabel('Proportion')
plt.title('Proportion of Male and Female Patients with Each Condition')
plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()

# MALE FEMALE AV LOS
labels = ["Pneumonia", "Myocardial Infarction", "Stroke", "Covid-19",	"Atrial Fibrillation", "Femur Fracture", "Nutritional \& Metabolic Diseases","Other Pulmonary Disease"]
men_means = [16, 6.5, 29.2, 16.2, 4.1, 28.8, 3, 7.3]
women_means = [13.8, 7.3, 27.2, 15.7, 4.4, 32.3, 4, 6.8]


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, men_means, width, label='Male')
rects2 = ax.bar(x + width/2, women_means, width, label='Female')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average LOS (days)')
ax.set_xlabel('Condition')
ax.set_title('Average LOS for Male and Female Patients with each Condition')
ax.set_xticks(x, labels, rotation=30, ha='right')
ax.legend()
ax.grid()

#ax.bar_label(rects1, padding=3)
#ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()