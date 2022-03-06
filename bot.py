from nltk.stem.porter import PorterStemmer

from fileReader import FileReader

class Bot:
	"""
		Constructor to initialize constant class variables, and setup the responses.
	"""
	def __init__(self):
		self.name = ""
		self.stemmer = PorterStemmer()
		self.conditions = {}
		self.initialize()

	"""
		Using the file reader to read in the data. using the stemmer class to check if the key matches the condition of the word.
	"""
	def initialize(self):
		self.data = FileReader().getFileContent()
		self.nodes = self.data['nodes']

		for key in self.data['conditions'].keys():
			words = [self.stemmer.stem(word) for word in self.data['conditions'][key]]
			self.conditions[key] = words

	"""
		Returns a node for the given id, if exists.
	"""
	def findNode(self, id):
		if id is None:
			return None
		for node in self.nodes:
			if node['id'] == id:
				return node
		return None

	"""
		Method sets the name to a class variable.
		The response to the second question is saved to the node, which will be used in initializeChat method.
	"""
	def setUserName(self, name):
		self.name = name
		self.current = self.nodes[0]
		return f"> Bot: Hello {self.name}.\nI am glad to have you here today, How are you feeling?\n\n"

	"""
		Return the user's name.
	"""
	def getUserName(self):
		if len(self.name) == 0:
			return -1
		return self.name
 
	"""
		TODO: Rewrite the purpose of the method.
		This runs the main chat loop, exits when the next node is none.
	"""
	def getResponse(self, answer):
		nodeValue = self.current
		
		if 'print' in nodeValue:
			nodeValue = self.findNode(nodeValue['children'][0])
			self.current = nodeValue
			return nodeValue

		if answer.lower() == "quit":
			return -1
		
		if len(nodeValue['children']) == 1:
			nodeValue = self.findNode(nodeValue['children'][0])
		else:
			answer_words = [self.stemmer.stem(word) for word in answer.lower().split(" ")]
			for child in nodeValue['children']:
				child = self.findNode(child)
				if 'default' in child:
					nodeValue = child
					break
				for word in self.conditions[child['condition']]:
					if word in answer_words:
						nodeValue = child
				if nodeValue == child:
					break

		self.current = nodeValue
		return nodeValue
"""
	Runs the chat with the command 'python bot.py'.
"""
if __name__ == '__main__':
	Bot()