import base64

from azure.storage.file import FileService

def readFiles(fs: FileService, fileList):
	shareEnumerator = fs.list_directories_and_files('prismo-unmodified')
	files = {}
	for file in shareEnumerator:
		if (file.name in fileList):
			pakFile = fs.get_file_to_text('prismo-unmodified', None, file.name, 'latin-1')
			files[file.name] = pakFile.content.splitlines(True)
	return files

def createResponseBody(files, spoilerLog, hasSpoiler):
	response = {}
	if (hasSpoiler == 1):
		response["spoilerLog"] = ''.join(spoilerLog)
	for key in files:
		fileBytes = ''.join(files[key]).encode('latin-1')
		response[key] = base64.b64encode(fileBytes).decode('latin-1')
	return response