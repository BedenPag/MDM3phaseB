# PROJECT AIM: Forcast bed occupancy based on distribution data and patient parameters
# e.g Age, Area, Illness, Time of year (flu season etc.)

# !CAUTION! Colorama used to format output, may cause errors in other IDE's
import random as rn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from colorama import Fore, Style
from numpy.random import choice
from scipy.stats import bernoulli


# Simulation parameters
PATIENT_INIT = 280          # Number of patients already in hospital at the beginning of simulation
AD_RATE = 55                # Patient admission rate (number per day)
SIM_TIME = 90               # Simulation run time (days)
SEED = 1
ILLNESSES = {
    'Myocardial Infarction': [7.3, 6.5],
    'Stroke': [27.2, 29.2],
    'COVID 19': [15.7, 16.2],
    'Fracture of Femur': [32.3, 28.8],                         # Dictionary of illnesses and their aLOS (male/female)
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
        self.occupancy_timeline = np.zeros(SIM_TIME)

    def treat_patients(self, day):
        temp_patients = []
        for patients in self.patients_list:
            if bernoulli.rvs(patients.discharge_prob[day - patients.ad_day]) == 0:
                temp_patients.append(patients)
        print(f"Number of patients discharged: {len(self.patients_list) - len(temp_patients)}")
        self.patients_list = temp_patients
        self.occupancy = len(self.patients_list) / self.beds * 100
        self.occupancy_timeline[day] = self.occupancy

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

    def __init__(self, admission):
        self.gender = choice((0, 1), p=[0.5, 0.5])
        self.illness = rn.choice(list(ILLNESSES.keys()))
        self.av_los = self.assign_a_los()
        self.discharge_prob = self.probability_distribution()
        self.ad_day = admission

    # Returns average length of stay for each illness
    def assign_a_los(self):
        los = ILLNESSES[self.illness][self.gender]
        return los

    # Returns distribution of probability of leaving per day for given illness
    def probability_distribution(self):
        dist = sorted(np.random.exponential(self.av_los, size=100))
        dist = np.cumsum(dist)
        dist = dist/dist[-1]
        return dist


# Runs the simulation using simulation parameters
def run(days, ad_rate):
    hospital = Hospital()
    for num in range(PATIENT_INIT):
        hospital.patients_list.append(Patient(rn.randint(-30, 0)))  # Initialise hospital with existing patients
    for i in range(days):
        print(f"Day {i+1}")
        for j in range(ad_rate + 1):
            if len(hospital.patients_list) < hospital.beds:         # Checks bed occupancy hasn't been reached
                hospital.patients_list.append(Patient(i))  # Patients get admitted if there is an available bed
            else:
                break
        print(f"Number of patients admitted: {j}")
        hospital.treat_patients(i)
        print(Fore.BLUE + f"Occupancy: {hospital.occupancy:.1f}%" + Style.RESET_ALL)
    hospital.show_results()
    hospital.illness_breakdown()


if __name__ == '__main__':
    print(f"Start Simulation")
    # Allows repeat results i.e same random values generated per seed
    np.random.seed(SEED)
    rn.seed(SEED)
    run(SIM_TIME, AD_RATE)  # Begins simulation

