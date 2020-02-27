import os
os.system('yapf --in-place --recursive --style=google src/ *.py')
os.system('mypy src/* --ignore-missing-imports')
