import pybullet as p
import pybullet_data
import numpy as np
import os

from pybullet_envs.robot_bases import XmlBasedRobot, MJCFBasedRobot, URDFBasedRobot

from time import sleep

physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
#physicsClient = p.connect(p.DIRECT)#or p.DIRECT for non-graphical version

p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally

#print(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
#cubeStartPos = [0,0,1]
#cubeStartPos = [0,0,0]
#cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
#boxId = p.loadURDF("r2d2.urdf", [0,0,1])
#boxId = p.loadURDF("cube_small.urdf", [0,0,1])
p.setAdditionalSearchPath(os.getcwd())
#boxId = p.loadURDF("/Users/maruyama/Desktop/pybullet_test/test.urdf", [0,0,1])

#boxId = p.loadMJCF(os.path.join(pybullet_data.getDataPath(),"/mjcf/hopper.xml"))[0]
#boxId = p.loadURDF(os.path.join(pybullet_data.getDataPath(),"cartpole.urdf"),[0,0,0])

boxId = p.loadSDF("model_test01.sdf")[0]
#boxId = p.loadSDF("HingeRobot01/model.sdf")[0]

#boxId = p.loadURDF("model_test01.urdf",[0,0,0])

#cubeStartPos = [0,0,50]
#cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
#boxId = p.loadURDF("simple_robot01.urdf",cubeStartPos, cubeStartOrientation)

n = p.getNumJoints(boxId)
print("joint_num:", n)
for i in range(n):
    print(p.getJointInfo(boxId, i))
print()

maxForce = 5000
targetVel = 0.5
# p.setJointMotorControl2(
#     bodyUniqueId=boxId,
#     jointIndex=0,
#     controlMode=p.VELOCITY_CONTROL,
#     targetVelocity = targetVel,
#     force = maxForce)

#p.stepSimulation()

print(boxId)
print(planeId)

i = 0
p.setRealTimeSimulation(1)
while True:
    i += 1
    p.setGravity(0,0,-10)
    #p.stepSimulation()
    sleep(0.01)
    #print(p.getContactPoints(boxId))
    #p.setJointMotorControl2(boxId, 0, p.POSITION_CONTROL, -1, force = 15)
    if i % 100 == 0:
        th = (np.random.rand() - 0.5) * np.pi
        p.setJointMotorControl2(boxId, 0, p.POSITION_CONTROL, th, force = 15)
        #p.setJointMotorControl2(boxId, 0, p.VELOCITY_CONTROL, targetVelocity=v, force = 100)



p.disconnect()
