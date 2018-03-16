import gym
#import gym_pull
#import pybullet_envs
import ipdb

#env = gym.make('MountainCar-v0')
#env = gym.make('LunarLander-v2')
#env = gym.make('FrozenLake-v0')
#env = gym.make('Hopper-v2')
#env = gym.make('Swimmer-v2')
#env = gym.make('MinitaurBulletEnv-v0')
#env = gym.make('HopperBulletEnv-v0')
#env = gym.make('Walker2DBulletEnv-v0')
#env = gym.make("HopperBulletEnv-v0")
#env = gym.make("CartPoleBulletEnv-v0")
#env = gym.make("CarRacing-v0")
env = gym.make("Pendulum-v0")


#gym_pull.pull('github.com/ppaquette/gym-super-mario')        # Only required once, envs will be loaded with import gym_pull afterwards
#env = gym.make('ppaquette/SuperMarioBros-1-1-v0')

#env.render(mode="human")
#env.render()

observation = env.reset()
print(env.action_space)
while True:
    #env.render(mode="human")
    env.render()
    action = env.action_space.sample()
    env.step(action)
