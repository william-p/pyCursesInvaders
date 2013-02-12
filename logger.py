class Logger(object):
	def __init__(self, level='debug'):
		self.level = level
		self.messages = []

	def dump(self):
		print("Dump %s messages:" % len(self.messages))
		for message in self.messages:
			print(message)

	def debug(self, msg):
		if self.level == 'debug':
			self.messages.append(str(msg))