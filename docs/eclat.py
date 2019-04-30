from itertools import combinations


class Eclat(object):
	"""
        Custom library for Eclat Algorithm, how to use this library:
        1. Define your own object
            object = Eclat(dataset=(pd.read_csv('Sample data.csv', header=None), pair=2)
        2. Get scores will return 3 of list, there is combinations, scores and confidence
            object.getScores()
        3. You can use DataFrame
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
					values.append("0")
			self.transactions.append(values)

	def getUniqueItems(self):
		for i in range(0, len(self.transactions)):
			self.items.extend(self.transactions[i])
		self.uniqueItems = list(set(self.items))
		self.uniqueItems.remove("0")
		return self.uniqueItems

	def getScores(self):
		scores = list()
		confidence = list()
		lift = list()
		rules = list()
		comb = [x for x in combinations(self.uniqueItems, self.pair)]
		for i in comb:
			conditions = list()
			rule = list()
			for item in i:
				conditions.append('("{}") in x'.format(item))
				rule.append("{}".format(item))
			rules.append('Jika {}'.format(rule[0]) + ' maka ' + ', '.join(rule[1:]))
			cond_code = ('[x for x in self.transactions if ' + ' and '.join(conditions) + ']')
			conf_codeA = ('[x for x in self.transactions if ("{}") in x]'.format(i[0]))
			conf_codeB = ('[x for x in self.transactions if ("{}") in x]'.format(i[-1]))
			scores.append((len(eval(cond_code))/len(self.transactions))*100)
			confidence.append((len(eval(cond_code))/len(eval(conf_codeB)))*100)
			lift.append((len(eval(conf_codeA)) * len(eval(conf_codeB))) / ((len(eval(conf_codeB)) / len(self.transactions)) * 100))
		return [rules, scores, confidence, lift]
