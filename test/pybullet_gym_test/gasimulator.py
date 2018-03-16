import os, time
import numpy as np
import pybullet as p
import pybullet_data


class GAPhysicsSimulator(object):
    AGENT_DATA_PATH = "."  # data directory of agent model

    def __init__(self, display=True):
        super(GAPhysicsSimulator, self).__init__()
        if display:
            physicsClient = p.connect(p.GUI)
        else:
            physicsClient = p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        planeId = p.loadURDF("plane.urdf")
        p.setAdditionalSearchPath(os.path.join(os.getcwd(), GAPhysicsSimulator.AGENT_DATA_PATH))
        self._agentId = p.loadURDF("model_test01.urdf", [0,0,0], [0,0,0,1])
        p.setGravity(0, 0, -9.80665)

    def reset(self):
        #p.resetBasePositionAndOrientation(self._agentId, [0,0,0], [0,0,0,1])
        p.removeBody(self._agentId)
        self._agentId = p.loadURDF("model_test01.urdf", [0,0,0], [0,0,0,1])

    def run_trial(self, genotype, time_sec=60, realtime=False):
        #p.setRealTimeSimulation(1)
        move_index = 0
        for i in range(time_sec*60):
            #p.setGravity(0,0,-10)
            p.stepSimulation()
            #time.sleep(0.01)
            #print(p.getContactPoints(boxId))
            #p.setJointMotorControl2(boxId, 0, p.POSITION_CONTROL, -1, force = 15)

            if i % 60 == 0:
                #th = (np.random.rand() - 0.5) * np.pi
                th = genotype[move_index]
                p.setJointMotorControl2(self._agentId, 0, p.POSITION_CONTROL, th, force = 15)
                move_index = (move_index + 1) % len(genotype)
                #p.setJointMotorControl2(boxId, 0, p.VELOCITY_CONTROL, targetVelocity=v, force = 100)
        pos, _ = p.getBasePositionAndOrientation(self._agentId)
        dist = pos[0]**2 + pos[1]**2
        #print(dist)
        return dist


    def finish(self):
        p.disconnect()
