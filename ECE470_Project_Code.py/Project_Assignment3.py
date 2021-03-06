#
# Project_Assignment3.py
#
# Created by Felipe F. and Di Z.
# 3/12/18
#
# To show forward kinematics for robot in V_Rep Simulator


import vrep
import math
import time
import numpy as np
import scipy as sp
from scipy import linalg

#def forward_kinematics (S1_skew,S2_skew,S3_skew,S4_skew,S5_skew,S6_skew, M, theta1,theta2,theta3,theta4,theta5,theta6,t1,t2,t3,t4,t5,t6):
#    #T_1in0 = sp.linalg.expm(S1_skew * theta1) * sp.linalg.expm(S2_skew * theta2) * sp.linalg.expm(S3_skew * theta3) * sp.linalg.expm(
#    #   S4_skew * theta4) * sp.linalg.expm(S5_skew * theta5) * sp.linalg.expm(S6_skew * theta6) * M
#    a = np.dot(linalg.expm(S1_skew * theta1*t1),linalg.expm(S2_skew * theta2*t2))
#    b = np.dot(a,linalg.expm(S3_skew * theta3*t3))
#    c = np.dot(b, linalg.expm(S4_skew * theta4*t4))
#    d = np.dot(c, linalg.expm(S5_skew * theta5*t5))
#    e = np.dot(d, linalg.expm(S6_skew * theta6*t6))
#    T_1in0 = np.dot(e,M)
#    #T_1in0 = np.dot(linalg.expm(S1_skew * theta1) * linalg.expm(S2_skew * theta2) * linalg.expm(
#     #   S3_skew * theta3) * linalg.expm(
#     #  S4_skew * theta4) * linalg.expm(S5_skew * theta5) * linalg.expm(S6_skew * theta6), M)
#    return T_1in0

def forward_kinematics (S1_skew,S2_skew,S3_skew,S4_skew,S5_skew,S6_skew, M, theta1,theta2,theta3,theta4,theta5,theta6):
    #T_1in0 = sp.linalg.expm(S1_skew * theta1) * sp.linalg.expm(S2_skew * theta2) * sp.linalg.expm(S3_skew * theta3) * sp.linalg.expm(
    #   S4_skew * theta4) * sp.linalg.expm(S5_skew * theta5) * sp.linalg.expm(S6_skew * theta6) * M
    a = np.dot(linalg.expm(S1_skew * theta1),linalg.expm(S2_skew * theta2))
    b = np.dot(a,linalg.expm(S3_skew * theta3))
    c = np.dot(b, linalg.expm(S4_skew * theta4))
    d = np.dot(c, linalg.expm(S5_skew * theta5))
    e = np.dot(d, linalg.expm(S6_skew * theta6))
    T_1in0 = np.dot(e,M)
    #T_1in0 = np.dot(linalg.expm(S1_skew * theta1) * linalg.expm(S2_skew * theta2) * linalg.expm(
     #   S3_skew * theta3) * linalg.expm(
     #  S4_skew * theta4) * linalg.expm(S5_skew * theta5) * linalg.expm(S6_skew * theta6), M)
    return T_1in0


# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])

print('Enter the six angles (in radians) for each joint that you would like to robot to achieve. ')
theta1 = eval(input('Angle 1: '))
theta2 = eval(input('Angle 2: '))
theta3 = eval(input('Angle 3: '))
theta4 = eval(input('Angle 4: '))
theta5 = eval(input('Angle 5: '))
theta6 = eval(input('Angle 6: '))

#S = np.matrix([[0, -1, -1, -1, 0, -1], [0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, -0.152, -0.396, -0.396, 0.11, -0.692], [0, 0, 0, 0, 0, 0]])

S = np.matrix([[0, -1, -1, -1, 0, -1], [0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, -0.152, -0.396, -0.609, 0.11, -0.692], [0, 0, 0, 0, 0, 0]])


S1_skew = np.matrix([[0, -1, 0, 0], [1, 0, 0,  0    ], [0,  0, 0, 0], [0, 0, 0, 0]])
S2_skew = np.matrix([[0,  0, 0, 0], [0, 0, 1, -0.152], [0, -1, 0, 0], [0, 0, 0, 0]])
#S3_skew = np.matrix([[0,  0, 0, 0], [0, 0, -1, 0.396], [0,  1, 0, 0], [0, 0, 0, 0]])
S3_skew = np.matrix([[0,  0, 0, 0], [0, 0, 1, -0.396], [0,  -1, 0, 0], [0, 0, 0, 0]])

#S4_skew = np.matrix([[0,  0, 0, 0], [0, 0, 1, -0.396], [0, -1, 0, 0], [0, 0, 0, 0]])

S4_skew = np.matrix([[0,  0, 0, 0], [0, 0, 1, -0.609], [0, -1, 0, 0], [0, 0, 0, 0]])
S5_skew = np.matrix([[0, -1, 0, 0], [1, 0, 0,  0.11 ], [0,  0, 0, 0], [0, 0, 0, 0]])
#S6_skew = np.matrix([[0, -1, 0, 0], [1, 0, 0,  0.11 ], [0,  0, 0, 0], [0, 0, 0, 0]])

S6_skew = np.matrix([[0, 0, 0, 0], [0, 0, 1,  -0.692 ], [0,  -1, 0, 0], [0, 0, 0, 0]])

M = np.matrix([[1, 0, 0, -0.342], [0, 1, 0, 0], [0, 0, 1, 0.692], [0, 0, 0, 1]])

T_1in0 = forward_kinematics(S1_skew,S2_skew,S3_skew,S4_skew,S5_skew,S6_skew, M, theta1,theta2,theta3,theta4,theta5,theta6)
#T_1in0 = forward_kinematics(S1_skew,S2_skew,S3_skew,S4_skew,S5_skew,S6_skew, M, theta1,theta2,theta3,theta4,theta5,theta6,t1,t2,t3,t4,t5,t6)
R_1in0 = np.array(T_1in0[0:3,0:3])
eulerAngles = rotationMatrixToEulerAngles(R_1in0)
p_1in0 = np.array(T_1in0[0:3,3])

print()
print('Pose of end-effector: ')
print(T_1in0)
print()
print('Euler Angles: ')
print(eulerAngles)
print()
#print(R_1in0)
#print(p_1in0)


# Close all open connections (just in case)
vrep.simxFinish(-1)

# Connect to V-REP (raise exception on failure)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID == -1:
    raise Exception('Failed connecting to remote API server')


# Get "handle" to ALL joints of robot
# Get "handle" to the first joint of robot
result, joint_one_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint1', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

# Get "handle" to the second joint of robot
result, joint_two_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

# Get "handle" to the third joint of robot
result, joint_three_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint3', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

# Get "handle" to the fourth joint of robot
result, joint_four_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint4', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

# Get "handle" to the fifth joint of robot
result, joint_five_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint5', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

# Get "handle" to the sixth joint of robot
result, joint_six_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint6', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

# Get "handle" to WorldReferenceFrame
result, WorldReferenceFrame_handle = vrep.simxGetObjectHandle(clientID, 'T_1in0_ReferenceFrame', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

# Get "handle" to T_1in0_ReferenceFrame
result, T_1in0_ReferenceFrame_handle = vrep.simxGetObjectHandle(clientID, 'T_1in0_ReferenceFrame', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

# Start simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

# Wait two seconds
time.sleep(2)

# Set T_1in0_ReferenceFrame position and orientation
vrep.simxSetObjectPosition(clientID,T_1in0_ReferenceFrame_handle,WorldReferenceFrame_handle,p_1in0,vrep.simx_opmode_oneshot)
vrep.simxSetObjectOrientation(clientID,T_1in0_ReferenceFrame_handle,WorldReferenceFrame_handle,eulerAngles,vrep.simx_opmode_oneshot)

# Position all the joint angles according to user input
# Set the desired value of the first joint variable
t = time.process_time()
vrep.simxSetJointTargetPosition(clientID, joint_one_handle, theta1, vrep.simx_opmode_oneshot)
t1 = time.process_time()-t
#t1 = vrep.simxGetLastCmdTime(clientID)
#print(t1)
time.sleep(2) # Wait two seconds


# Set the desired value of the second joint variable
t = time.process_time()
vrep.simxSetJointTargetPosition(clientID, joint_two_handle, theta2, vrep.simx_opmode_oneshot)
t2 = time.process_time()-t
#t2 = vrep.simxGetLastCmdTime(clientID)
time.sleep(2) # Wait two seconds


# Set the desired value of the third joint variable
t = time.process_time()
vrep.simxSetJointTargetPosition(clientID, joint_three_handle, theta3, vrep.simx_opmode_oneshot)
t3 = time.process_time()-t
#t3 = vrep.simxGetLastCmdTime(clientID)
time.sleep(2) # Wait two seconds


# Set the desired value of the fourth joint variable
t = time.process_time()
vrep.simxSetJointTargetPosition(clientID, joint_four_handle, theta4, vrep.simx_opmode_oneshot)
t4 = time.process_time()-t
#t4 = vrep.simxGetLastCmdTime(clientID)
time.sleep(2) # Wait two seconds


# Set the desired value of the fifth joint variable
t = time.process_time()
vrep.simxSetJointTargetPosition(clientID, joint_five_handle, theta5, vrep.simx_opmode_oneshot)
t5 = time.process_time()-t
#t5 = vrep.simxGetLastCmdTime(clientID)
time.sleep(2) # Wait two seconds


# Set the desired value of the sixth joint variable
t = time.process_time()
vrep.simxSetJointTargetPosition(clientID, joint_six_handle, theta6, vrep.simx_opmode_oneshot)
t6 = time.process_time()-t
#t6 = vrep.simxGetLastCmdTime(clientID)
time.sleep(2) # Wait two seconds


# Stop simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
vrep.simxGetPingTime(clientID)

# Close the connection to V-REP
vrep.simxFinish(clientID)

