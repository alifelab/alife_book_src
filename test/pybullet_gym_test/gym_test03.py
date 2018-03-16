import os, inspect
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(os.path.dirname(currentdir))
#os.sys.path.insert(0,parentdir)

import gym
import numpy as np
import pybullet as p
import pybullet_envs
import time


def main():
    env = gym.make("HopperBulletEnv-v0")
    env.render(mode="human")

    env.reset()
    for i in range (p.getNumBodies()):
        print(p.getBodyInfo(i))
        if (p.getBodyInfo(i)[1].decode() == "hopper"):
           torsoId=i
           print("found torso")
           print(p.getNumJoints(torsoId))
           for j in range (p.getNumJoints(torsoId)):
              print(p.getJointInfo(torsoId,j))#LinkState(torsoId,j))
    while 1:
        frame = 0
        score = 0
        restart_delay = 0
        #disable rendering during reset, makes loading much faster
        obs = env.reset()

        while 1:
            time.sleep(1./60.)
            #a = pi.act(obs)
            a = env.action_space.sample()
            obs, r, done, _ = env.step(a)
            score += r
            frame += 1
            distance=5
            yaw = 0
            humanPos = p.getLinkState(torsoId,4)[0]
            camInfo = p.getDebugVisualizerCamera()
            curTargetPos = camInfo[11]
            distance=camInfo[10]
            yaw = camInfo[8]
            pitch=camInfo[9]
            targetPos = [0.95*curTargetPos[0]+0.05*humanPos[0],0.95*curTargetPos[1]+0.05*humanPos[1],curTargetPos[2]]
            p.resetDebugVisualizerCamera(distance,yaw,pitch,targetPos);

if __name__=="__main__":
    main()
