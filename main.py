# PROJECT AIM: Forcast bed occupancy based on distribution data and patient parameters
# e.g Age, Area, Illness, Time of year (flu season etc.)

# !CAUTION! Colorama used to format output, may cause errors in other IDE's
import numpy as np
from colorama import Fore, Style

# Simulation parameters
AD_RATE = 55                # Patient admission rate (number per day)
SIM_TIME = 90               # Simulation run time (days)
SEED = 1


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
        self.illness = assign_illness()
        self.los = self.assign_a_los()
        self.discharge_prob = self.probability_distribution()
        self.ad_day = admission

    # Returns average length of stay for each illness
    def assign_a_los(self):
        a_los = [10, 12, 8, 9]
        los = a_los[self.illness.index(1)]
        return los

    # -NEEDS UPDATING TO EXPONENTIAL- Returns distribution of probability of leaving per day for given illness
    def probability_distribution(self):
        dist = np.random.normal(self.los, 2, size=100)
        dist = dist / np.linalg.norm(dist)
        return dist


# Returns randomly assigned illness
def assign_illness():
    illnesses = [0, 0, 0, 0]                    # Discrete set of possible illnesses
    ind = np.random.randint(0, len(illnesses))
    illnesses[ind] = 1
    return illnesses


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
    np.random.seed(SEED)        # Allows repeat results i.e same random values generated per seed
    run(SIM_TIME, AD_RATE)


