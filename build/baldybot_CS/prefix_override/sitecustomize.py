import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/itti_jammy/RoverBaldies_ws/install/baldybot_CS'
