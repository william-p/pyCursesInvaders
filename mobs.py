from entity import Entity

from sprites import ship,		ship_destroy
from sprites import alien1,		alien1_destroy
from sprites import alien2
from sprites import block

import random
from copy import deepcopy

class Alien2(Entity):
	def __init__(self, line=0, *args, **kwargs):
		self.sprites = deepcopy(alien2)
		self.sprites_destroy = deepcopy(alien1_destroy)

		Entity.__init__(self, *args, **kwargs)

		self.line = line
		self.speed = 1

		self.life = 2
		self.point = 20

	def tick(self):
		if not random.randint(0, 150):
			self.fire(0)

		return Entity.tick(self)

class Alien1(Entity):
	def __init__(self, line=0, *args, **kwargs):
		self.sprites = deepcopy(alien1)
		self.sprites_destroy = deepcopy(alien1_destroy)

		Entity.__init__(self, *args, **kwargs)

		self.line = line
		self.speed = 1
		self.point = 10

class Ship(Entity):
	def __init__(self, *args, **kwargs):
		self.sprites = deepcopy(ship)
		self.sprites_destroy = deepcopy(ship_destroy)

		Entity.__init__(self, *args, **kwargs)

		# center
		self.y = (self.display.height - 1) - self.height
		self.x = int((self.display.width/2) - (self.width/2))

		self.speed = 5
		self.life = 3


class Block(Entity):
	def __init__(self, *args, **kwargs):
		self.sprites = deepcopy(block)
		self.sprites_destroy = None

		Entity.__init__(self, *args, **kwargs)

		self.speed = 0
		self.life = 5

		self.center = (
			len(self.sprites[0][0]) / 2,
			len(self.sprites[0]) / 2
		)

		self.print_life()

	def print_life(self):
		x = self.center[0]
		y = self.center[1]

		line = self.sprites[0][y]
		line = list(line)
		line[x] = str(self.life)
		self.sprites[0][y] = "".join(line)

	def tick(self):
		if not self.destroyed and not self.onDestroy:
			self.print_life()

		return Entity.tick(self)