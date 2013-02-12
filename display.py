import sys, os, curses
from copy import deepcopy

class Display(object):
	def __init__(self):
		self.screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		self.screen.keypad(1)
		self.screen.nodelay(1)

		self.display_map = []
		self.entity_map = []

		self.height, self.width = self.screen.getmaxyx()
		self.border = 0

		if self.border == 0:
			self.height -= 2
			self.width -= 2

		self.clear()
		self.refresh()

	def get_center(self, sprite):
		x = int( (self.width / 2) - (len(sprite[0])/2) )
		y = int( (self.height / 2) - (len(sprite)/2) )
		return (x, y)

	def clear(self):
		self.display_map = []
		for h in range(0, self.height):
			line = [ ' ' for w in range(0, self.width) ]
			self.display_map.append(line)
		
		self.entity_map = deepcopy(self.display_map)

	def refresh(self):
		self.screen.clear()
		self.screen.border(self.border)

		for y, line in enumerate(self.display_map):
			line = "".join(line)
			self.screen.addstr(y+1, 1, line)

		self.screen.refresh()

	def addStr(self, pos, message):
		self.screen.addstr(pos[0], pos[1], str(message))

	def write(self, entity=None, sprite=None, pos=None):

		if not entity and not sprite:
			return []

		if not sprite:
			epos, sprite = entity.tick()

		if not pos:
			pos = epos

		collision = []
		
		if pos:
			x = pos[0]
			y = pos[1]

			if sprite:
				for my, line in enumerate(sprite):
					for mx, value in enumerate(line):
						if y + my < self.height and x + mx < self.width:
							if entity:
								atPos = self.entity_map[y + my][x + mx]
								if atPos  and atPos != ' ' and atPos != entity and atPos not in collision:
									collision.append(atPos)
									
								self.entity_map[y + my][x + mx] = entity

							self.display_map[y + my][x + mx] = value

		return collision

	def getch(self):
		try:
			return self.screen.getch()
		except:
			raise Exception("screen.getch raised !")

	def close(self):
		self.screen.erase()
		self.screen.refresh()
		self.screen.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
		sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)