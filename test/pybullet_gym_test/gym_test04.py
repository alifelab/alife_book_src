

class HopperBulletEnv(WalkerBaseBulletEnv):
	def __init__(self):
		self.robot = Hopper()
		WalkerBaseBulletEnv.__init__(self, self.robot)
