# Add path to source code
import sys, os
if os.getcwd().endswith('tests'):
	sys.path.insert(0, '..')
elif os.path.exists('websocket_server'):
	sys.path.insert(0, '.')
