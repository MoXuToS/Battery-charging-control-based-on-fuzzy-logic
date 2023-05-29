# Battery-charging-control-based-on-fuzzy-logic
Introduction

The task was to write a program that implements battery charging using fuzzy logic.

The input data of the program will be the following properties of the device:
Battery capacity, Battery temperature, Battery usage level, The maximum and minimum values of the output voltage that the charging adapter gives, The maximum and minimum current that the charging adapter has,Desired charge level, Current charge level, Battery voltage

Output:
The time it takes to charge the device, Graph of how the device is charging.
I will use the Internet and study the operation of the charging adapter based on the characteristics of Xiaomi 33W Charging Combo.

Looking at these data, you can see that as the output voltage increases, the current decreases.
For calculations, we take the standard formulas from the textbook on physics.

Battery capacity is calculated by the formula:
E=qU (1)
,where q is the stored charge in amp-hours, and U is the average voltage in volts, and E is the amount of energy in watt-hours.

To calculate the battery capacity in Joules, multiply formula (1) by 3600.

To calculate the amount of energy supplied to the battery from the charging adapter, we use the formula for the work of an electric current
A=UIt (2)

Where, U is the output voltage of the charging adapter in volts, I is its current strength in amperes, t is the time in seconds that the device is connected to the network, and A is the work of the current itself in Joules.
Knowing these formulas, it will not be difficult to form a rule by which the current strength is calculated.

t=E/UI

The input data of the example implementation of this algorithm will be the battery of the Oneplus Nord CE device with the SUPERVOOC 80W charging adapter.

Input data: Battery capacity 4500 mAh,We find out the battery voltage using the AccuBattery program and it is 4.1 V,Battery temperature 27.6 degrees Celsius, Usage will be 3% of the maximum, The maximum voltage is 20 V, the minimum is also 2 V, The maximum current is 15 A, 4 A, Desired charge level 80%, The current level is 3%
