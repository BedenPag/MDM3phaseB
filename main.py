# PROJECT AIM: Forcast bed occupancy based on distribution data and patient parameters
# e.g Age, Area, Illness, Time of year (flu season etc.)

# !CAUTION! Colorama used to format output, may cause errors in other IDE's
import math
import random as rn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from colorama import Fore, Style
from numpy.random import choice
from scipy.stats import bernoulli


# Simulation parameters
PATIENT_INIT = 0         # Number of patients already in hospital at the beginning of simulation
AD_RATE = 55                # Patient admission rate (number per day)
BASE = 15                   # Time to allow initialisation errors to dissipate
SIM_TIME = BASE + 90        # Simulation run time (days)
SIM_NUMS = 10
SEED = 2
ILLNESSES = {
    'Myocardial Infarction': [0, [0.666, 0.334], [7.3, 6.5]],
    'Stroke': [1, [0.526, 0.474], [27.2, 29.2]],
    'COVID 19': [2, [0.533, 0.467], [15.7, 16.2]],
    'Fracture of Femur': [3, [0.327, 0.673], [32.3, 28.8]],                         # Dictionary of illnesses and their aLOS (male/female)
    'Atrial Fibrillation': [4, [0.541, 0.459], [4.4, 4.1]],
    'Pneumonia': [5, [0.506, 0.494], [13.8, 16.0]],
    'Endocrine, Nutritional and Metabolic Diseases': [6, [0.497, 0.503], [4.0, 3.0]],
    'COPD': [7, [0.450, 0.550], [6.8, 7.3]]
}
AGE_PROB = [
    [0.000048, 0.000036, 0.001236, 0.012881, 0.061737, 0.178239, 0.232617, 0.261483, 0.198051, 0.053672],
    [0.000800, 0.000850, 0.004079, 0.012443, 0.036318, 0.100152, 0.164398, 0.273102, 0.301036, 0.106822],
    [0.032112, 0.015531, 0.051875, 0.093188, 0.110624, 0.141331, 0.148221, 0.184304, 0.164978, 0.057836],
    [0.010456, 0.008126, 0.007341, 0.008092, 0.011909, 0.033538, 0.078518, 0.224270, 0.403928, 0.213822], 
    [0.000093, 0.000822, 0.004908, 0.013876, 0.035552, 0.120503, 0.208803, 0.313501, 0.237352, 0.064590],
    [0.018408, 0.004256, 0.010121, 0.019732, 0.032541, 0.071616, 0.132417, 0.257947, 0.311395, 0.141567],
    [0.039002, 0.043393, 0.054660, 0.074321, 0.096695, 0.158375, 0.174663, 0.185326, 0.137744, 0.035821],
    [0.000608, 0.000227, 0.000567, 0.003987, 0.025790, 0.102994, 0.232143, 0.367922, 0.225822, 0.039940]
]
plt.rcParams.update({"text.usetex": True, 'font.size': 14})


# Hospital object that treats Patient objects
class Hospital:

    def __init__(self):
        self.beds = 300                                                 # Number of beds available
        self.patients_list = []                                         # List of all active patients
        self.occupancy = (len(self.patients_list) / self.beds)*100      # Percentage occupancy of beds
        self.occupancy_timeline = np.zeros(SIM_TIME)
        self.discharge_timeline = np.zeros(SIM_TIME)

    def treat_patients(self, day):
        temp_patients = []
        for patients in self.patients_list:
            patients.update_probability()
            if bernoulli.rvs(patients.discharge_prob) == 0:
                patients.los += 1
                temp_patients.append(patients)
        num_discharged = len(self.patients_list) - len(temp_patients)
        # print(f"Number of patients discharged: {num_discharged}")
        self.patients_list = temp_patients
        self.occupancy = len(self.patients_list) / self.beds * 100
        self.occupancy_timeline[day] = self.occupancy
        self.discharge_timeline[day] = num_discharged


    def show_results(self):
        patient_data = []
        for patient in self.patients_list:
            patient_data.append(patient.__dict__)
        df = pd.DataFrame(patient_data).drop('discharge_prob', axis=1)
        print(df)
        plt.plot(np.linspace(1, SIM_TIME, SIM_TIME), self.occupancy_timeline)
        plt.xlabel(f"Day")
        plt.ylabel(f"Bed Occupancy (%)")
        plt.title(f"Hospital Bed Occupancy Forecast 3 Months in the Future")
        plt.show()

    def illness_breakdown(self):
        patient_data = []
        counts = []
        for patient in self.patients_list:
            patient_data.append(patient.__dict__)
        df = pd.DataFrame(patient_data).drop('discharge_prob', axis=1)
        illnesses = [*ILLNESSES]
        for illness in illnesses:
            counts.append(df['illness'].value_counts()[illness])
        explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
        plt.pie(counts, explode=explode, labels=illnesses, autopct='%1.1f%%', shadow=True)
        plt.axis('equal')
        plt.title('Percentage of Different Illnesses Present in Final Count')
        plt.show()


# Patient object to be treated by hospital
class Patient:

    def __init__(self, admission, los_factor):
        self.illness = choice(list(ILLNESSES.keys()), p=[0.10, 0.08, 0.15, 0.06, 0.08, 0.20, 0.23, 0.10])
        # original probabilities p=[0.10, 0.08, 0.15, 0.06, 0.08, 0.20, 0.23, 0.10]
        # pandemic probabilities p=[0.04, 0.03, 0.75, 0.04, 0.03, 0.04, 0.03, 0.04]
        self.gender = choice((0, 1), p=ILLNESSES[self.illness][1])
        self.age = choice(choice([range(0, 9), range(10, 19), range(20, 29), range(30, 39),
                                       range(40, 49), range(50, 59), range(60, 69), 
                                       range(70, 79), range(80, 89), range(90, 100)],
                                      p=AGE_PROB[ILLNESSES[self.illness][0]]))
        self.age_factor = self.age_factor()
        self.av_los = self.assign_a_los() * los_factor
        self.ad_day = admission
        self.los = self.los_calculate()
        self.discharge_prob = 0

    def age_factor(self):
        idx = int(self.age/10)
        age_factors = np.array([0.772, 0.9219, 0.9493, 0.9676, 0.9927, 1.0155, 1.0818, 1.0840, 1.1229, 1.9322])
        return age_factors[idx]

    # Returns average length of stay for each illness
    def assign_a_los(self):
        los = ILLNESSES[self.illness][2][self.gender] * self.age_factor
        return los

    def los_calculate(self):
        if self.ad_day < 0:
            return abs(self.ad_day)
        else:
            return 0

    def update_probability(self):
        self.discharge_prob = 1 - math.e**(-((1/self.av_los)*self.los))


# Runs the simulation using simulation parameters
def run(days, ad_rate, los_factor):
    hospital = Hospital()
    for num in range(PATIENT_INIT):
        hospital.patients_list.append(Patient(rn.randint(-2, 0), 1))  # Initialise hospital with existing patients
    for i in range(days):
        # print(f"Day {i+1}")
        for j in range(ad_rate + 1):
            if len(hospital.patients_list) < hospital.beds:         # Checks bed occupancy hasn't been reached
                hospital.patients_list.append(Patient(i, los_factor))  # Patients get admitted if there is an available bed
            else:
                break
        # print(f"Number of patients admitted: {j}")
        hospital.treat_patients(i)
        # print(Fore.BLUE + f"Occupancy: {hospital.occupancy:.1f}%" + Style.RESET_ALL)
    # hospital.show_results()
    # hospital.illness_breakdown()
    avg_discharge = np.mean(hospital.discharge_timeline)
    print(f"Average Discharge Rate: {avg_discharge:.2f}")
    return hospital.occupancy_timeline, avg_discharge


def plot_results(result):
    iterations = []
    colours = ['red', 'blue', 'orange', 'green']
    for i in range(1):
        iterations.append(f"Iteration {i + 1}")
        iterations.append(f"Average {i + 1}")
        idx = i % len(colours)
        plt.plot(np.linspace(1, SIM_TIME - BASE, SIM_TIME - BASE), result[i][BASE:SIM_TIME], color=colours[idx])
        plt.axhline(y=np.mean(result[i][BASE:SIM_TIME]), linestyle='--', color=colours[idx])
    avg = np.sum(result, axis=0)/len(result)
    iterations.append(f"{SIM_NUMS} Iteration Average")
    plt.plot(np.linspace(1, SIM_TIME - BASE, SIM_TIME - BASE), avg[BASE:SIM_TIME], 
             color='black', linewidth=2)
    plt.xlabel(f"Day")
    plt.ylabel(f"Bed Occupancy (\%)")
    plt.title(f"Hospital Bed Occupancy Forecast (3 Month Prediction)")
    plt.grid()
    plt.legend(iterations, loc='upper right')
    plt.show()
    
    
def plot_discharge(los_factor, rates):
    plt.plot(los_factor, rates, linestyle='dashdot', color='black')
    plt.xlabel(f"LOS factor")
    plt.ylabel(f"Discharge Rate (patients per day)")
    plt.title(f"Average discharge rate as a function of LOS")
    plt.grid()
    plt.show()

    

if __name__ == '__main__':
    print(f"Start Simulation")
    # Allows repeat results i.e same random values generated per seed
    np.random.seed(SEED)
    rn.seed(SEED)
    results = np.zeros((SIM_NUMS, SIM_TIME))
    discharge_rate = np.zeros(SIM_NUMS)
    los_factor = np.linspace(0.5, 1.5, SIM_NUMS)
    for i in range(SIM_NUMS):
        (results[i], discharge_rate[i]) = run(SIM_TIME, AD_RATE, los_factor[i])  # Runs simulation
    # plot_results(results)
    plot_discharge(los_factor, discharge_rate)
		
