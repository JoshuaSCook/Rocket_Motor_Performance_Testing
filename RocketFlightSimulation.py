#### Rocket Performance
####
#### last modified by
#### Josh Cook
#### 03/24/16
####
#### This code simulates the kinematics of a rocket, given the mass of the
#### rocket body, motor and fuel as well as the thrust given off by the motor.
####
#### Future additions will include importing real thrust curves derived from
#### static motor tests via Arduino pressure sensor.
####
#### #### #### ####
#### #### #### ####
class rocketSpecs(object):
    def __init__(self, name="", massBody=0.0, dragCoef=0.0, crossSecArea=0.0):
        self.name = name
        self.massBody = massBody
        self.dragCoef = dragCoef
        self.crossSecArea = crossSecArea

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

class parachuteSpecs(object):
    def __init__(self, name="", dragCoef=0.0, crossSecArea=0.0):
        self.name = name
        self.dragCoef = dragCoef
        self.crossSecArea

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

class motorSpecs(object):
    def __init__(self, name="", massMotor=0.0, massFuel=0.0):
        self.name = name
        self.massMotor = massMotor
        self.massFuel = massFuel

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()
        
def total_impulse(time_data, thrust_data):
    total_impulse = 0
    index = 1
    while index < len(time_data):
        differential_time = time_data[index] - time_data[index - 1]
        total_impulse += differential_time * thrust_data[index]
        index += 1
    return(round(total_impulse, 1))
    
def average_thrust(time_data, total_impulse):
    average_thrust = total_impulse / time_data[len(time_data) - 1]
    return(round(average_thrust, 1))
    
def motor_rating(total_impulse, average_thrust, time_data):
    if total_impulse > 0.0 and total_impulse <= 2.5:
        letter = "A"
    elif total_impulse > 2.5 and total_impulse <= 5.0:
        letter = "B"
    elif total_impulse > 5.0 and total_impulse <= 10.0:
        letter = "C"
    elif total_impulse > 10.0 and total_impulse <= 20.0:
        letter = "D"
    elif total_impulse > 20.0 and total_impulse <= 40.0:
        letter = "E"
    elif total_impulse > 40.0 and total_impulse <= 80.0:
        letter = "F"
    elif total_impulse > 80.0 and total_impulse <= 160.0:
        letter = "G"
    else:
        letter = "NA"
    burn_time = time_data[-1]
    return(letter + str(int(round(average_thrust, 0))) + "-" + str(int(round(burn_time, 0))))

#### #### #### ####
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Constants
g = -9.8    # acceleration due to gravity (m/s^2)
m_R = 0.057    # mass of rocket (kg)
m_M = 0.065    # mass of motor (kg)

# Air Resistance
rho = 1.29    # density of air (kg/m^3)

cd_R = 0.1    # coefficient of drag (unitless) for a typical model rocket
a_R = 0.071    # cross-sectional area of rocket (m^2): body + fins
k_R = 0.5 * rho * cd_R * a_R    # proportionality constant (kg/m) for rocket

cd_P = 1.35    # coefficient of drag (unitless) for a typical parachute
a_P = 0.28    # cross-sectional area of parachute (m^2)
k_P = 0.5 * rho * cd_P * a_P    # proportionality constant (kg/m) for parachute

# Motor Performance - Thrust (N) as a function of time (s)
data = np.genfromtxt('thrust_data.csv', dtype=None, names=True, delimiter=",")
time_data = [0.0]
thrust_data = [0.0]
for row in data:
    time_data.append(round(row[0], 3))
    thrust_data.append(round(row[1], 3))

total_impulse = total_impulse(time_data, thrust_data)
print ("TOTAL IMPULSE: " + str(total_impulse) + " Ns")

average_thrust = average_thrust(time_data, total_impulse)
print("AVERAGE THRUST: " + str(average_thrust) + " N")

burn_time = time_data[-1]
print("BURN TIME: " + str(round(burn_time, 1)) + " s")

motor_rating = motor_rating(total_impulse, average_thrust, time_data)
print("MOTOR RATING: " + motor_rating)

t = 0.0    # time (s)
h0 = 0.0    # height (m)
v0 = 0.0    # velocity ()
m_F = ((-0.018 / 0.6) * t) + 0.018    # mass of fuel (kg)

a_max = 0.0
v_max = 0.0

# This loop calculates rocket kinematics while the engine if firing.
x1_data = []
y1_data = []
t_index = 0
for value in thrust_data:
    try:
        t_inter = time_data[t_index + 1] - time_data[t_index]
    
        m_T = m_R + m_M + m_F    # total mass (kg)
    
        thrust = value    # instantaneous thrust (N)
        a = g + (thrust / m_T) - ((k_R * (v0 ** 2)) / m_T)    # acceleration is the sum of the gravitational, thrust and air resistance accerlerations
        h = h0 + (v0 * t_inter) + (0.5 * a * (t_inter ** 2))    # calculates the hight of the rocket at the given time interval
    
        h0 = h    # sets the h0 for the next time interval
        v0 = v0 + (a * t_inter)    # sets v0 for the next time interval
    
        x1_data.append(t)
        y1_data.append(h)
    
        t_index += 1
        t = time_data[t_index]  
        
        if a > a_max:
            a_max = a
        if v0 > v_max:
            v_max = v0     
    except:
        t = time_data[t_index]

print("\nMAXIMUM G-FORCE: " + str(round((a_max / 9.8), 1)) + " G's")
print("MAXIMUM VELOCITY: " + str(round(v_max, 1)) + " m/s")

# This loop calculates the projectile motion after engine cutoff
t_inter = 0.05    # time interval for calculations (s)
x2_data = [time_data[-2]]
y2_data = [h]
while v0 > 0.0:
    a = g - ((k_R * (v0 ** 2)) / m_T)
    h = h0 + (v0 * t_inter) + (0.5 * a * (t_inter ** 2))

    h0 = h
    v0 = v0 + (a * t_inter)

    x2_data.append(t)
    y2_data.append(h)

    t += t_inter

print("APOGEE IN: " + str(round(t, 1)) + " s")
y_win = int(h + (0.1 * h))
print("MAXIMUM ALTITUDE: " + str(round(h, 1)) + " m")

# This loop calculates the kinematics after parachute deployment at apogee
x3_data = [t - t_inter]
y3_data = [h]
while h > 0.0:
    a = g + ((k_P * (v0 ** 2)) / m_T)
    h = h0 + (v0 * t_inter) + (0.5 * a * (t_inter ** 2))

    h0 = h
    v0 = v0 + (a * t_inter)

    x3_data.append(t)
    y3_data.append(h)

    t += t_inter

print("\nDESCENT RATE: " + str(round(v0, 1)) + " m/s")
x_win = int(t + (0.1 * t))   
print("TOTAL FLIGHT TIME: " + str(round(t, 1)) + " s")

#### #### #### ####
# Initiation
matplotlib.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
ax = fig.add_subplot(111)

# Add the points to the plot
ax.plot(x1_data, y1_data, 'r.-', markersize=12, markeredgecolor='none')
ax.plot(x2_data, y2_data, 'b-', markersize=12, markeredgecolor='none')
ax.plot(x3_data, y3_data, 'g-', markersize=12, markeredgecolor='none')
ax.plot(time_data, thrust_data, 'k.--', markersize=12, markeredgecolor='none')

# Labels and Axes
ax.set_title('Rocket Simulation', fontsize='18')
ax.set_xlabel('Time (s)', fontsize='14')
ax.set_ylabel('Altitude (m) :: Thrust (N)', fontsize='14')
ax.set_xlim(0, x_win)
ax.set_ylim(0, y_win)
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
plt.tight_layout()

# Open Plot in Pyplot
plt.show()