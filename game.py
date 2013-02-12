import curses
import sys, subprocess, traceback, os
import time

from logger import Logger
from display import Display
from entity import Entity

from mobs import Alien1, Alien2, Ship, Block
from entity import Torpedo
from sprites import game_over, you_win

class Game(object):
	def __init__(self):
		self.logger = Logger(level='debug')

		self.logger.debug("Create display")
		self.display = Display()

		self.logger.debug(" + size: %sx%s" % (self.display.width, self.display.height))

		## Config
		self.blocks_width = 5
		self.aliens_width = 10
		self.aliens_height = 4
		self.aliens_margin = 2

		self.torpedos = []
	
		self.max_speed = 10
		self.frame_rate = 25
		self.speed_down = 3

		self.score = 0

		# Build Aliens
		self.aliens = self.build_aliens()

		# Build Blocks
		self.blocks = self.build_blocks()

		# Build ship
		self.ship = Ship(
			logger=self.logger,
			display=self.display,
			game=self
		)

	def build_blocks(self):
		step = int(self.display.width / self.blocks_width)
		blocks = []
		start_y = self.display.height - 13
		start_x = 0
		for x in range(0, self.blocks_width):
			block = Block(
				logger=self.logger,
				display=self.display,
				game=self,
				x=start_x + x * step,
				y=start_y
			)
			blocks.append(block)

		if block:
			# Center blocks
			offset = (self.blocks_width-1) * step
			offset = offset + block.width
			offset = self.display.width - offset
			offset = offset / 2
			for block in blocks:
				block.x += offset

		return blocks

	def build_aliens(self):
		# Build level
		start_x=2
		start_y=1
		alien_width = 0
		alien_height = 0

		aliens = []

		for x in range(0, self.aliens_width):
			for y in range(0, self.aliens_height):

				objAlien = Alien1
				if y == 0:
					objAlien = Alien2

				alien = objAlien(
						logger=self.logger,
						display=self.display,
						game=self,
						x=start_x + x * (alien_width + self.aliens_margin),
						y=start_y + y * (alien_height + self.aliens_margin),
						line=y
					)

				alien_width = alien.width
				alien_height = alien.height

				aliens.append(alien)

		return aliens

	def win(self):
		self.display.clear()
		self.display.write(
					pos=self.display.get_center(you_win),
					sprite=you_win
				)
		self.display.refresh()
		time.sleep(5)

	def game_over(self):
		self.display.clear()
		self.display.write(
			pos=self.display.get_center(game_over),
			sprite=game_over
		)
		self.display.refresh()
		time.sleep(5)		

	def start(self):
		err = None
		lastfire = time.time() - 5
		way = True

		try:
			self.logger.debug("Start game")
			run = True
			while run:
				time.sleep(1.0/self.frame_rate)
				self.display.clear()

				# GAME OVER
				if self.ship.life <= 0:
					self.game_over()
					break

				# Choose way right or left
				nb_mob = 0
				ori_way = way
				for index, alien in enumerate(self.aliens):
					if not alien.destroyed:
						nb_mob += 1
						if alien.atRight or alien.atLeft:
							#ways[alien.line] = not ways[alien.line]
							way = not way
							break

				# You WIN
				if not nb_mob:
					self.win()
					break

				# Display Blocks
				for block in self.blocks:
					self.display.write(block)

				# Display Ship
				self.display.write(self.ship)

				# Move down Aliens
				if ori_way != way:
					for index, alien in enumerate(self.aliens):
						alien.move_down(self.speed_down)

				# Move right or left Aliens
				for index, alien in enumerate(self.aliens):
					if not alien.destroyed:
						#if ways[alien.line]:
						if way:
							alien.move_right()
						else:
							alien.move_left()

						collisions = self.display.write(alien)
						if collisions:
							self.game_over()
							run = False

				if not run:
					break

				# Move Torpedos
				for index, torpedo in enumerate(self.torpedos):
					if torpedo.destroyed:
						del self.torpedos[index]
					else:
						# Destroy torpedo 
						if torpedo.atTop or torpedo.atBottom:
							# Touch the sky
							torpedo.destroy()
							self.display.write(torpedo)
						else:
							torpedo.move()
		
							# Display torpedo
							collisions = self.display.write(torpedo)
							if collisions:
								for entity in collisions:
									if type(entity) == Torpedo:
										# Align sprite
										torpedo.y = entity.y + entity.height

										# Destroy torpedo
										entity.touch()
										torpedo.touch()
									elif type(entity) in [Alien1, Alien2] and type(torpedo.parent) in [Alien1, Alien2]:
										# Alien2 vs Alien1
										pass
									else:
										# Self shot :)
										if torpedo.parent != entity:
											entity.touch()
											torpedo.destroyed = True

				# Display map
				self.display.refresh()

				# Display score
				self.display.addStr((1,1), "Score: %s" % self.score)
				lifeStr = "Life: %s" % self.ship.life
				self.display.addStr((1,self.display.width - len(lifeStr)), lifeStr)

				# Bind keys
				c = self.display.getch()
				if 		c == curses.KEY_LEFT:
					self.ship.move_left()

				elif    c == curses.KEY_RIGHT:
					self.ship.move_right()

				# Space
				elif    c == 32:
					if (time.time() - lastfire) > 0.1:
						lastfire = time.time() 
						self.ship.fire()

				# Q
				elif 	c == 113:
					self.logger.debug("Quit game")
					break

				elif c != -1:
					self.logger.debug("Key %s preseed" % c)

			self.logger.debug("End of game")

		except Exception, err:
			pass

		finally:
			self.display.close()
			self.logger.dump()
			if err:
				traceback.print_exc(limit=20, file=sys.stdout)