import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import math
from skfuzzy import control as ctrl

# Input data
Battery_Capacity = 4500
Battery_U = 3.764
SoC_init, SoC_target = 0, 100
U_min, U_max = 5, 20
I_min, I_max = 1.35, 3
Battery_temp = 61 # battery temperature
Device_using = 21 # Percentage utilization rate

# Description of phase-fiction variables
SoC = ctrl.Antecedent(np.arange(0, 101, 1), 'SoC')
Temperature = ctrl.Antecedent(np.arange(15, 75, 1), 'Temperature')
Using = ctrl.Antecedent(np.arange(1, 101, 1), 'Using')
Charge_I = ctrl.Consequent(np.arange(I_min, I_max, 0.25), 'Charge_I')
Charge_U = ctrl.Consequent(np.arange(U_min, U_max, 1), 'Charge_U')

# Description of universal membership functions
SoC['low'] = fuzz.trimf(SoC.universe, [0, 0, 33])
SoC['medium'] = fuzz.trimf(SoC.universe, [30, 50, 70])
SoC['high'] = fuzz.trimf(SoC.universe, [67, 100, 100])

Temperature['low'] = fuzz.trapmf(Temperature.universe, [15, 15, 25, 35])
Temperature['medium'] = fuzz.trimf(Temperature.universe, [25, 40, 55])
Temperature['high'] = fuzz.trapmf(Temperature.universe, [45, 60, 75, 75])

Using['low'] = fuzz.trimf(Using.universe, [1, 1, 33])
Using['medium'] = fuzz.trimf(Using.universe, [30, 50, 70])
Using['high'] = fuzz.trimf(Using.universe, [67, 100, 100])

delta = (U_max - U_min)/3
delt = delta/6
Charge_U['low'] = fuzz.trimf(Charge_U.universe, [U_min, U_min, U_min + delta])
Charge_U['medium'] = fuzz.trimf(Charge_U.universe, [U_min + delta - delt, (U_min + U_max) / 2, U_max - delta - delt])
Charge_U['high'] = fuzz.trimf(Charge_U.universe, [U_max - delta, U_max, U_max])

delta = (I_max - I_min)/3
delt = delta/6
Charge_I['low'] = fuzz.trimf(Charge_I.universe, [I_min, I_min, I_min + delta])
Charge_I['medium'] = fuzz.trimf(Charge_I.universe, [I_min + delta - delt, (I_min + I_max) / 2, I_max - delta - delt])
Charge_I['high'] = fuzz.trimf(Charge_I.universe, [I_max - delta, I_max, I_max])

# Fuzzy Logic Rules for Voltage
Rule1 = ctrl.Rule(SoC['low'] | Temperature['low'] | Using['low'], Charge_U['high'])
Rule2 = ctrl.Rule(SoC['medium'] | Temperature['medium'] | Using['medium'], Charge_U['medium'])
Rule3 = ctrl.Rule(SoC['high'] | Temperature['high'] | Using['high'], Charge_U['low'])

# Fuzzy logic rules for current strength
Rule4 = ctrl.Rule(SoC['low'] | Temperature['low'] | Using['low'], Charge_I['medium'])
Rule5 = ctrl.Rule(SoC['medium'] | Temperature['medium'] | Using['medium'], Charge_I['high'])
Rule6 = ctrl.Rule(SoC['high'] | Temperature['high'] | Using['high'], Charge_I['low'])

# We create a fuzzy logic system
charge_ctrl = ctrl.ControlSystem([Rule1, Rule2, Rule3, Rule4, Rule5, Rule6])
charging = ctrl.ControlSystemSimulation(charge_ctrl)

def ChargingSimulation():
    current_capacity = [SoC_init]
    current_U = []
    current_I = []
    while current_capacity[-1] < SoC_target:
        # Get the current charge level as a percentage
        charging.input['SoC'] = current_capacity[-1]
        charging.input['Using'] = Device_using
        charging.input['Temperature'] = Battery_temp
        charging.compute()
        Charge_current_U_opt = charging.output['Charge_U']
        Charge_current_I_opt = charging.output['Charge_I']
        # Finding the battery capacity in Joules
        E = Battery_Capacity * Battery_U * 3600 / 1000
        # Finding capacity
        A = Charge_current_U_opt * Charge_current_I_opt
        # Let's find out how many percent of the charge this second gave us
        Change_capacity  = A/E * 100
        current_capacity.append(current_capacity[-1] + Change_capacity)
        current_U.append(Charge_current_U_opt)
        current_I.append(Charge_current_I_opt)
    return current_capacity, current_U, current_I

# We get the charge change per second
y, Changing_U, Changing_I = ChargingSimulation()
time_in_seconds = len(y)
# Get the number of hours
hours_count = math.ceil(time_in_seconds / 3600)

# Get every second change within an hour
x = np.linspace(0, time_in_seconds / 60, time_in_seconds)

# Create two arrays that will help make the graph more beautiful
needs_for_full_hour = hours_count * 3600 - time_in_seconds
x_add = np.linspace(time_in_seconds / 60, hours_count * 60, needs_for_full_hour)
y_add = np.linspace(y[-1], y[-1], needs_for_full_hour)

# Add them to the original arrays
x = np.append(x, x_add)
y = np.append(y, y_add)

plt.figure('Charge Simulation')
plt.plot(x, y, color = 'red')

# Limiting the Y axis
plt.ylim(-5, 105)

# We sign the axes
plt.ylabel('% of capacity')
plt.xlabel('Minuts for charge')

# Graph title customization
time  = round(time_in_seconds / 60, 2)
minuts = int(time)
seconds = round((time - minuts) * 60)
suptitle = "Total charging time is equal to " + str(minuts) + " minuts and " + str(seconds) + " seconds " + '\n'
suptitle += "for charging from " + str(SoC_init) + "% to " + str(SoC_target) + "% of battery capacity\n"
plt.title(suptitle)
# We show the graph
plt.show()

# clean up the data to show a graph of voltage and current
plt.clf()
x = np.linspace(0, time, len(Changing_I))

# Create a table of values
plt.plot(x, Changing_I, label='Changing I', color = 'red')
plt.plot(x, Changing_U, label='Changing U', color = 'green')

# We sign the axes
plt.ylabel('Value')
plt.xlabel('Minuts in Charging')

# limit the y axis
plt.ylim = (0, max(I_max, U_max) + 2)

# add title to chart
plt.title('Changing of I and U during charging \n')

# Adding a legend
plt.legend()

# We show the graph
plt.show()