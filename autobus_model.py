import numpy as np
import math
import random

tau = 1.5 / 60

def V(L_t, H, n):
    return L_t * n / H

def v_net(L_t, H, n, v_Cr, tau, s):
    return L_t / ((L_t / v_Cr) + (H + tau) * ((L_t / s) * (1 / (n + 1))))

def M(L_t, H, n, v_Cr, tau, s):
    return math.ceil(V(L_t, H, n) / v_net(L_t, H, n, v_Cr, tau, s) + 1 * L_t / s)

def Z_A(thresholds, inputs, tau):
    return inputs[8] * inputs[0] +\
           inputs[9] * V(inputs[0], thresholds[0], thresholds[2]) +\
           inputs[10] * M(inputs[0], thresholds[0], thresholds[2], inputs[3], tau, thresholds[1]) +\
           inputs[11] * M(inputs[0], thresholds[0], thresholds[2], inputs[3], tau, thresholds[1]) +\
           inputs[12] * thresholds[3] * M(inputs[0], thresholds[0], thresholds[2], inputs[3], tau, thresholds[1])

def Z_U(thresholds, inputs, tau):
    return inputs[1] * inputs[6] * (2 * inputs[5] / inputs[7] +\
                                    thresholds[0] / 2 +\
                                    (inputs[2] / inputs[3]) + tau)

def Z_T(thresholds, inputs, tau):
    return Z_A(thresholds, inputs, tau) + Z_U(thresholds, inputs, tau)


# Inputs [0:L_t, 1:Demand, 2:l, 3:v_Cr, 4:v_max, 5:a, 6:beta, 7:v_walk, 8:cost_L, 9:cost_V, 10:cost_M, 11:csot_ER, 12:cost_B]
V5_inputs = [15.2, 396, 3.8, 40, 50, 1.3 * 1e-3, 12.5, 4, 7.61, 0.696, 13.417, 0.98, 0.021]
H10_inputs = [23.7, 6247, 5.93, 40, 50, 1.3 * 1e-3, 12.5, 4, 7.61, 0.696, 13.417, 0.98, 0.021]

V5_Z_T_opt, H10_Z_T_opt = 1e10, 1e10
V5_thresholds_opt, H10_thresholds_opt = [], []

for i in range(int(1e7)):
    # thresholds [H, s, n(pods/convey), C]
    V5_thresholds = [random.uniform(5, 15) / 60, random.uniform(0.30, 0.75), random.randint(2, 10), random.uniform(50, 200)]
    H10_thresholds = [random.uniform(1, 7) / 60, random.uniform(0.30, 0.75), random.randint(3, 10), random.uniform(50, 200)]
    # print(H10_thresholds)
    V5_Z_T = Z_T(V5_thresholds, V5_inputs, tau)
    H10_Z_T = Z_T(H10_thresholds, H10_inputs, tau)
    V5_consumption = v_net(V5_inputs[0], V5_thresholds[0], V5_thresholds[2], V5_inputs[3], tau, V5_thresholds[1]) * 0.30 * 14 * (1 + 0.2)
    H10_consumption = v_net(H10_inputs[0], H10_thresholds[0], H10_thresholds[2], H10_inputs[3], tau, H10_thresholds[1]) * 0.30 * 14 * (1 + 0.2)
    V5_O = (V5_inputs[2] / V5_inputs[2]) * V5_inputs[1] * V5_thresholds[0] / V5_thresholds[2]
    H10_O = (H10_inputs[2] / H10_inputs[2]) * H10_inputs[1] * H10_thresholds[0] / H10_thresholds[2]
    # if H10_O < 15: print(H10_consumption, H10_thresholds[3], H10_O, 15)
    if V5_Z_T <= V5_Z_T_opt and V5_consumption < V5_thresholds[3] and V5_O < 15:
        V5_Z_T_opt =  V5_Z_T
        V5_thresholds_opt = V5_thresholds
    if H10_Z_T <= H10_Z_T_opt and H10_consumption < H10_thresholds[3] and H10_O < 15:
        H10_Z_T_opt =  H10_Z_T
        H10_thresholds_opt = H10_thresholds
        
print("V5")
print(f"Z_T = {V5_Z_T_opt}\tHeadways = {V5_thresholds_opt[0] * 60}\tStop spacing = {V5_thresholds_opt[1]}\tC = {V5_thresholds[3]}\tn(Pods/Convoy) = {V5_thresholds_opt[2]}")
print("H10")
print(f"Z_T = {H10_Z_T_opt}\tHeadways = {H10_thresholds_opt[0] * 60}\tStop spacing = {H10_thresholds_opt[1]}\tC = {H10_thresholds[3]}\tn(Pods/Convoy) = {H10_thresholds_opt[2]}")