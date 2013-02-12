from sprites import torpedo,	torpedo_destroy
from copy import deepcopy

class Entity(object):
	def __init__(self, logger, display, game, x=0, y=0):
		self.logger = logger
		self.display = display

		self.speed = 1
		self.nb_tick = 0

		self.game = game

		try:
			if not self.sprites:
				self.sprites = None
		except:
			self.sprites = None

		try:
			if not self.sprites_destroy:
				self.sprites_destroy = None
		except:
			self.sprites_destroy = None

		self.height = len(self.sprites[0])
		self.width = len(self.sprites[0][0])

		self.x = x
		self.y = y

		self.atRight = False
		self.atLeft = False
		self.atTop = False
		self.atBottom = False

		self.destroyed = False
		self.onDestroy = False

		self.life = 1
		self.point = 0

		#logger.debug("Create entity, height: %s, width: %s at %s, %s" % (self.height, self.width, self.x, self.y))

	def check_pos(self):
		self.atRight = False
		self.atLeft = False
		self.atTop = False
		self.atBottom = False

		if (self.x + self.width) >= self.display.width:
			self.atRight = True
			self.x = self.display.width - self.width

		if self.x <= 0:
			self.atLeft = True
			self.x = 0

		if self.y <= 0:
			self.atTop = True
			self.y = 0

		if self.y + self.height >= self.display.height:
			self.atBottom = True
			self.y = self.display.height - self.height

	def move_right(self, speed=None):
		if speed == None:
			speed = self.speed

		self.x += speed
		self.check_pos()

	def move_left(self, speed=None):
		if speed == None:
			speed = self.speed

		self.x -= speed
		self.check_pos()

	def move_up(self, speed=None):
		if speed == None:
			speed = self.speed

		self.y -= speed
		self.check_pos()

	def move_down(self, speed=None):
		if speed == None:
			speed = self.speed

		self.y += speed
		self.check_pos()

	def destroy(self):
		#self.destroyed = True
		self.onDestroy = True
		self.nb_tick = 0

	def fire(self, way=True):
		x = int(self.x + self.width/3)+1
		
		if way:
			y = self.y - self.height
		else:
			y = self.y + self.height

		torpedo = Torpedo(
			logger=self.logger,
			display=self.display,
			game=self.game,
			parent=self,
			way=way,
			x=x,
			y=y
		)

		self.game.torpedos.append(torpedo)

	def touch(self):
		self.life -= 1
		if not self.life:
			self.destroy()

	def tick(self):
		if self.destroyed:
			return None, None

		if self.onDestroy:
			self.nb_tick += 0.2

			if self.sprites_destroy:
				index = int(self.nb_tick) % len(self.sprites_destroy)
				sprite = self.sprites_destroy[index]
				if index >= len(self.sprites_destroy)-1:
					self.destroyed = True
					self.game.score += self.point
				return (self.x, self.y), sprite
			else:
				self.destroyed = True
				self.game.score += self.point
				return None, None

		self.nb_tick += 0.1

		index = int(self.nb_tick) % len(self.sprites)
		return (self.x, self.y), self.sprites[index]


class Torpedo(Entity):
	def __init__(self, parent, way=True, *args, **kwargs):
		self.sprites = deepcopy(torpedo)
		self.sprites_destroy = deepcopy(torpedo_destroy)

		Entity.__init__(self, *args, **kwargs)

		if not way:
			for sprite in self.sprites_destroy:
				sprite.reverse()

		# True: Up, False: Down
		self.way = way
		self.parent = parent
		self.speed = 3

	def destroy(self):
		# Center explode
		self.x -= len(self.sprites_destroy[0][0]) / 2
		Entity.destroy(self)

	def move(self, way=None):
		if not way:
			way = self.way

		if way:
			self.move_up()
		else:
			self.move_down()
