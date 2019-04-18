from itertools import combinations

class Eclat(object):

	"""
		Custom library for Eclat Algorithm, how to use this library:
		1. Define your own object
			object = Eclat(dataset=(pd.read_csv('Sample data.csv', header=None), pair=2)
		2. Get transactions
			object.getTransactions()
		3. Get unique item set
			object.getUniqueItems()
		4. Get scores will return 3 of list, there is combinations, scores and confidence
			object.getScores()
		5. You can use DataFrame 
			df = pd.DataFrame(object.getScores()).T
			df.columns = ['Pairs', 'Scores', 'Confidence']
			df.sort_values('Scores', ascending=False).head(10)

		Get your own research ^_^
	"""

	def __init__(self, dataset, pair):
		self.drugs = dataset.Drugs.tolist()
		self.dataWithoutLabels = dataset.drop(["Drugs"], axis=1)
		self.dataset = dataset
		self.transactions = list()
		self.columnsDate = list()
		self.items = list()
		self.uniqueItems = list()
		self.pair = pair
		self.newData = None

	def getCleanData(self):
		transaction = list()
		columnsDate = list()
		for i in self.dataWithoutLabels:
			columnsDate.append(i)
			values = list()
			for value in self.dataWithoutLabels[i]:
				if value is not 0:
					values.append(i)
				else:
					values.append(0)
			transaction.append(values)
		return transaction

	def getDataWithoutLabel(self):
		return self.dataWithoutLabels

	def getDrugs(self):
		return self.drugs

	def getTransactions(self):
		for i in self.dataWithoutLabels:
			self.columnsDate.append(i)
			values = list()
			for x, value in enumerate(self.dataWithoutLabels[i]):
				if value is not 0:
					values.append(self.drugs[x])
				else:
					values.append("nan")
			self.transactions.append(values)

	def getUniqueItems(self):
		self.getTransactions()
		for i in range(0, len(self.transactions)):
			self.items.extend(self.transactions[i])
		self.uniqueItems = list(set(self.items))
		self.uniqueItems.remove("nan")
		return self.uniqueItems

	def getScores(self):
		scores = []
		confidence = []
		comb = [x for x in combinations(self.getUniqueItems(), self.pair)]
		for i in comb:
			conditions = []
			for item in i:
				conditions.append('("{}") in x'.format(item))
			cond_code = ('[x for x in self.transactions if ' + ' and '.join(conditions)+']')
			conf_code = ('[x for x in self.transactions if ("{}") in x]'.format(i[0]))
			scores.append(len(eval(cond_code))/len(self.dataset))
			confidence.append(len(eval(cond_code))/len(eval(conf_code)))
		return [comb, scores, confidence]