import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def plot_proportions(counts, labels):
    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    plt.pie(counts, explode=explode, autopct='%1.1f%%', shadow=True)
    plt.legend(labels, loc=0, fontsize="small")
    plt.axis('equal')
    plt.title('Proportions of Patients with each Condition')
    plt.show()
    

def exp_func(x, a, b, c):
    return a * np.exp(-b * x) + c


def plot_data(data):
    days = np.array(data[data.columns[0]])
    count = np.array(data[data.columns[1]])
    popt, pcov = curve_fit(exp_func, days, count)
    a1, b1 = np.polyfit(days, count, 1)
    a2, b2, c2 = np.polyfit(days, count, 2)
    trend_exp = exp_func(days, *popt)
    trend_lin = a1*days + b1
    trend_poly = a2*days**2 + b2*days + c2
    error_exp = np.sum((count - trend_exp)**2)/len(days)
    error_lin = np.sum((count - trend_lin)**2)/len(days)
    error_poly = np.sum((count - trend_poly) ** 2)/len(days)
    plt.plot(days, count, 'k', label="Count")
    plt.plot(days, trend_lin, 'r', label=F"Linear Approximation. MSE {error_lin:.2f}")
    plt.plot(days, trend_poly, 'b', label=f"Polynomial Approximation. MSE: {error_poly:.2f}")
    plt.plot(days, trend_exp, 'g', label=f"Exponential Approximation. MSE: {error_exp:.2f}")
    plt.title("LOS Patient Count for University Hospital Ayr (28/06/2022)")
    plt.xlabel("Length of Stay (Days)")
    plt.ylabel("Patient Count")
    plt.legend()
    plt.grid(visible=True, which="both")
    plt.show()


plt.rcParams.update({"text.usetex": True, 'font.size': 14})
illnesses = ["Pneumonia, Organism Unspecified", "Acute Myocardial Infarction", "Cerebral Infarction (Stroke)",					
            "Covid-19",	"Atrial Fibrillation", "Femur Fracture", "Endocrine, Nutritional and Metabolic Diseases",					
            "Other Chronic Obstructive Pulmonary Disease"	
]				
proportions = np.array([0.2001, 0.0867, 0.0826, 0.1505, 0.0833, 0.0617, 0.2346, 0.1005])
df = pd.read_csv('nhsinitialdata.csv')
plot_proportions(proportions, illnesses)
# plot_data(df)