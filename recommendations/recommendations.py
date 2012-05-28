from __future__ import with_statement

import simplejson as json
from math import sqrt
from pprint import pprint as pp

def sim_distance(prefs, p1, p2):
	si = set(prefs.get(p1, {}).keys()).intersection(set(prefs.get(p2, {}).keys()))
	if si:
		sum_of_squares = sum([
			pow(prefs[p1][item] - prefs[p2][item], 2) for item in si
		])
		return 1 / (1 + sqrt(sum_of_squares))
	else:
		return 0

def sim_pearson(prefs, p1, p2):
	si = set(prefs.get(p1, {}).keys()).intersection(set(prefs.get(p2, {}).keys()))
	n = len(si)
	if not n:
		return 0

	sum1 = sum([prefs[p1][item] for item in si])
	sum2 = sum([prefs[p2][item] for item in si])

	sum1_sq = sum([pow(prefs[p1][item], 2) for item in si])
	sum2_sq = sum([pow(prefs[p2][item], 2) for item in si])

	p_sum = sum([prefs[p1][item] * prefs[p2][item] for item in si])
	
	num = p_sum - (sum1 * sum2 / n)
	den = sqrt( (sum1_sq - pow(sum1, 2) / n) * (sum2_sq - pow(sum2, 2) / n) )
	if den == 0:
		return 0
	else:
		return num / den
		
def sim_manhattan(prefs, p1, p2):
	raise NotImplemented('Not implemented')
	
def top_matches(prefs, person, n=5, similarity=sim_pearson):
	scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
	scores.sort()
	scores.reverse()
	return scores[0:n]

def print_similarity(prefs, func, trunc=6, rjust=7):
	""" Prints prefs as pretty-looking table calculating by a provided function."""
	def _get_name(name):
		return name

	rows = [['']]
	for name in prefs:
		rows[0].append(_get_name(name))
	for name in prefs:
		row = [_get_name(name)]
		for name2 in prefs:
			row.append(func(prefs, name, name2))
		rows.append(row)
	for i, row in enumerate(rows):
		print ' | '.join(map(lambda x: str(x)[:trunc].rjust(rjust), row))
		if i == 0:
			print '+'.join('-' * (rjust + (2 if i else 1)) for i in rows[0])

def load_data(input_filename):
	with open(input_filename) as f:
		return json.loads(f.read())

def main(input_filename):
	critics = load_data(input_filename)
	print_similarity(critics, sim_distance)
		
if __name__ == '__main__':
	main('input.json')