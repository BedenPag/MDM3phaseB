# PROJECT AIM: Forcast bed occupancy based on distribution data and patient parameters
# e.g Age, Area, Illness, Time of year (flu season etc.)

# CURRENT ISSUES: using pyplot to generate counts is way too slow, need a better method - see line 62

# !CAUTION! Colorama used to format output, may cause errors in other IDE's
import random as rn
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, Style
from numpy.random import choice

# Simulation parameters
AD_RATE = 55                # Patient admission rate (number per day)
SIM_TIME = 90               # Simulation run time (days)
SEED = 1
ILLNESSES = {
    'Myocardial Infarction': [7.3, 6.5],
    'Stroke': [27.2, 29.2],
    'COVID 19': [15.7, 16.2],
    'Fracture of Femur': [32.3, 28.8],                             # Dictionary of illnesses and their aLOS
    'Atrial Fibrillation': [4.4, 4.1],
    'Pneumonia': [13.8, 16.0],
    'Endocrine, Nutritional and Metabolic Diseases': [4.0, 3.0],
    'COPD': [6.8, 7.3]
}


# Hospital object that treats Patient objects
class Hospital:

    def __init__(self):
        self.beds = 300                                                 # Number of beds available
        self.patients_list = []                                         # List of all active patients
        self.occupancy = (len(self.patients_list) / self.beds)*100      # Percentage occupancy of beds

    def treat_patients(self, day):
        temp_patients = []
        for patients in self.patients_list:
            if patients.discharge_prob[day - patients.ad_day] < np.random.random():
                # Temporary list to store all patients who do not leave this day
                temp_patients.append(patients)
        print(f"Number of patients discharged: {len(self.patients_list) - len(temp_patients)}")
        self.patients_list = temp_patients
        self.occupancy = len(self.patients_list) / self.beds * 100


# Patient object to be treated by hospital
class Patient:

    def __init__(self, admission):
        self.gender = choice((0, 1), p=[0.5, 0.5])
        self.illness = rn.choice(list(ILLNESSES.keys()))
        self.los = self.assign_a_los()
        self.discharge_prob = self.probability_distribution()
        self.ad_day = admission

    # Returns average length of stay for each illness
    def assign_a_los(self):
        los = ILLNESSES[self.illness][self.gender]
        return los

    # -NEEDS UPDATING TO EXPONENTIAL- Returns distribution of probability of leaving per day for given illness
    # Commented out code is too slow
    def probability_distribution(self):
        dist = np.random.normal(self.los, 10, size=100)
        # dist = np.random.exponential(self.los, size=100)
        # counts = plt.hist(dist, density=True, cumulative=True, bins=int(max(dist)))
        return dist     # counts[0]


# Runs the simulation using simulation parameters
def run(days, ad_rate):
    hospital = Hospital()
    for i in range(days):
        print(f"Day {i}")
        for j in range(ad_rate + 1):
            if len(hospital.patients_list) < 300:           # Checks bed occupancy hasn't been reached
                hospital.patients_list.append(Patient(i))   # Patients get admitted if there is an available bed
            else:
                break
        print(f"Number of patients admitted: {j}")
        hospital.treat_patients(i)
        print(Fore.BLUE + f"Occupancy: {hospital.occupancy:.1f}%" + Style.RESET_ALL)


if __name__ == '__main__':
    print(f"Start Simulation")
    # Allows repeat results i.e same random values generated per seed
    np.random.seed(SEED)
    rn.seed(SEED)
    run(SIM_TIME, AD_RATE)  # Begins simulation

