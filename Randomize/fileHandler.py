from azure.storage.file import FileService

def readFiles(fs: FileService, fileList, seed):
	shareEnumerator = fs.list_directories_and_files('prismo-unmodified')
	files = {}
	# this optimizes randomizing with a seed that was already randomized
	# todo: include the options in the identifier so that the same seed can be randomized with different options
	for file in shareEnumerator:
		if (file.name == seed):
			return files, True
	for file in shareEnumerator:
		if (file.name in fileList):
			pakFile = fs.get_file_to_text('prismo-unmodified', None, file.name, 'latin-1')
			files[file.name] = pakFile.content.splitlines(True)
	return files, False

def writeFiles(fs: FileService, files, identifier):
	fs.create_directory('prismo-unmodified', identifier)
	for key in files:
		fs.create_file_from_text('prismo-unmodified', identifier, key, ''.join(files[key]), 'latin-1')
	return

def writeLog(fs: FileService, spoilerLog, identifier):
	log = ''.join(spoilerLog)
	fs.create_file_from_text('prismo-unmodified', identifier, 'spoilerLog.txt', log)