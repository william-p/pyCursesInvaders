#!/usr/bin/env python

from game import Game
import sys, subprocess

if len(sys.argv) <= 1:
	# Open new xterm
	subprocess.check_output(
		"xterm -fs 1 -font 5x7 -geometry 200x80 -e 'python %s run'" % sys.argv[0],
		stderr=subprocess.STDOUT,
		shell=True)
else:
	# Run game
	mygame = Game()
	mygame.start()