# Add path to source code
import sys, os
if os.getcwd().endswith('tests'):
	sys.path.insert(0, '..')
elif os.getcwd().endswith('websocket-server'):
	sys.path.insert(0, '.')
