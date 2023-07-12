from window import * 
import importlib
import os

libs = []

for root, dirs, files in os.walk('.'):
	for file in files:
		if file.endswith('Nodes.py') and not file.startswith('__'):
			libs.append((root.strip('./').strip('.\\')+'.' if root != '.' else '')+file.strip('.py'))

	for dir in dirs:
		if dir.endswith('Nodes'):
			libs.append(dir)

for lib in libs:
	try:
		importlib.import_module(lib)
		print(f"Loaded {lib}")
	except Exception as e:
		print(f"Failed loading {lib}, skipping |",e)


app = QApplication([])

window = AppWindow()

app.exec_()