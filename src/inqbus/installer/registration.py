from installer import Installer

from sys import argv

# reading parameter
if '-h' in argv:
    host = argv[argv.index('-h') + 1]
else:
    host = 'localhost'

if '-p' in argv:
    python = argv[argv.index('-p') + 1]
else:
    python = 'system'

if '-v' in argv:
    venv_name = argv[argv.index('-v') + 1]
else:
    venv_name = None