class Eclat(object):

	def __init__(self, dataset):
		self.dataset = dataset
		self.transactions = list()
		self.items = list()
		self.uniqueItems = list()

	def transaction(self):
		for i in range(0, len(self.dataset)):
			self.transactions.append([str(self.dataset.values[i,j]) for j in range(0, len(self.dataset.columns))])
		return self.transactions

	def getUniqueItems(self):
		for i in range(0, len(self.transactions)):
			self.items.extend(self.transactions[i])
		self.uniqueItems = list(set(self.items))
		self.uniqueItems.remove("nan")
		return self.uniqueItems

