"""
///////////////////////////////////////////////////////
│	
│	Filename:	automate_2_sort_escore.py
│	
│	Input:		The text file of BLASTP result by performing diamond search (example below):
│				> diamond blastp --query $YOUR_FAA_FILE --db hgtdb_new/diamond/db --taxonmap hgtdb_new/taxon.map --taxonnames hgtdb_new/taxdump/names.dmp --outfmt 6 qseqid sseqid pident evalue bitscore staxids sscinames > diamond_result.tsv
│	Output:		Either printing in terminal, or 'Matched_Protein.csv', 'Matched_Protein.xlsx'
│	
│	Description:
│	To sort each of the BLASTP result by e-score,
│	and match the pattern:
│		In this research, we're interested in the proteins
│ 		where aftering sorting the BLASTQ by e-score
│		the first one is [Candidatus Prometheoarchaeum] (itself)
│		and the second one must be a bacteria
│	then output the list of proteins that fits the pattern
│	and save it into Excel / CSV file (Matched_Protein.csv)
│	==================================================
│	Authorship:	@cgneo
│	Copyright:	Modified BSD License.
│	Made with love by @cgneo https://github.com/cgneo
│	
///////////////////////////////////////////////////////
"""


""" 
│	⬇️ Mandatory !!!
│	Please enter the filename of the diamond BLASTP search result
│	For example:
│	folder_name = "./diamond_result.tsv"
"""
#============================================================
diamond_output = "./"
#============================================================
""" 
│	(optional) but you must comment out the last part of the code #sectionOptional
│
│	For the purpose of getting annotations of each protein,
│	Please enter the GTF file (annotated protein) of the species of interest
│	(avaliable on NCBI, for download link see `automate_1_NCBI_downloadLink.py`)
│	For example:
│	GTF_file_name = "GCF_008000775.1_ASM800077v1_genomic.gtf"
"""
#============================================================
GTF_file_name = "./"
#============================================================


with open(diamond_output, 'r') as reader1:
	templines = reader1.readlines()
	final_result = {}
	temp_score = {}
	temp_everything = {}
	previous_query = ''
	for line in templines:
		temp = line.replace('\n','').split('\t');
		qseqid = temp[0]
		sseqid = temp[1]
		pident = temp[2]
		evalue = temp[3]
		bitscore = temp[4]
		staxids = temp[5]
		sscinames = temp[6]
		"""
		Record the e-value scores into a dictionary: temp_score
  		"""
		if sscinames not in temp_score:
			temp_score[sscinames +'-'+ sseqid] = float(evalue)
			temp_everything[sscinames +'-'+ sseqid] = [qseqid,sseqid,pident,evalue,bitscore,staxids]
		else:
			print(sscinames)
			raise(f'error multiple ID')
		if previous_query != qseqid:
			"""
   			sort ascending:
	  			verify sorted by using: #print(sorted(temp_score.items(), key=lambda x: x[1]))
			"""
			temp_score = {k: v for k, v in sorted(temp_score.items(), key=lambda x: x[1])} 
			try:
				"""
				set record if fulfill requirement
				we want the second item of the sorted list to contain 'bacteria'
				"""
				taxNameOf2ndElement = list(temp_score.items())[1][0]
				print('📚',taxNameOf2ndElement)
			except:
				print(temp_score)
				taxNameOf2ndElement = ''
			if 'bac' in taxNameOf2ndElement:
				print('💘',taxNameOf2ndElement)
				final_result[previous_query] = temp_score
			# new result
			temp_score = {}
			temp_everything = {}
			# set current id
			previous_query = qseqid


for k,v in final_result.items():
    print(k,v)

#============================================================
"""
│	(optional) #sectionOptional
│	Reading gtf file and saving into Excel
│	If you don't have access to .gtf file your protein,
│	you can comment out the following code
"""

from collections import defaultdict
import gzip
import pandas as pd
import re

GTF_HEADER  = ['seqname', 'source', 'feature', 'start', 'end', 'score',
			   'strand', 'frame']
R_SEMICOLON = re.compile(r'\s*;\s*')
R_COMMA     = re.compile(r'\s*,\s*')
R_KEYVALUE  = re.compile(r'(\s+|\s*=\s*)')

def dataframe(filename):
	"""
	Open an optionally gzipped GTF file and return a pandas.DataFrame.
i	Istruction for reading .gtf:
		df = dataframe( ".gtf" )
	"""
	# Each column is a list stored as a value in this dict.
	result = defaultdict(list)

	for i, line in enumerate(lines(filename)):
		for key in line.keys():
			# This key has not been seen yet, so set it to None for all
			# previous lines.
			if key not in result:
				result[key] = [None] * i

		# Ensure this row has some value for each column.
		for key in result.keys():
			result[key].append(line.get(key, None))

	return pd.DataFrame(result)

def lines(filename):
	"""Open an optionally gzipped GTF file and generate a dict for each line.
	"""
	fn_open = gzip.open if filename.endswith('.gz') else open

	with fn_open(filename) as fh:
		for line in fh:
			if line.startswith('#'):
				continue
			else:
				yield parse(line)

def parse(line):
	"""Parse a single GTF line and return a dict.
	"""
	result = {}

	fields = line.rstrip().split('\t')

	for i, col in enumerate(GTF_HEADER):
		result[col] = _get_value(fields[i])

	# INFO field consists of "key1=value;key2=value;...".
	infos = [x for x in re.split(R_SEMICOLON, fields[8]) if x.strip()]

	for i, info in enumerate(infos, 1):
		# It should be key="value".
		try:
			key, _, value = re.split(R_KEYVALUE, info, 1)
		# But sometimes it is just "value".
		except ValueError:
			key = 'INFO{}'.format(i)
			value = info
		# Ignore the field if there is no value.
		if value:
			result[key] = _get_value(value)

	return result

def _get_value(value):
	if not value:
		return None

	# Strip double and single quotes.
	value = value.strip('"\'')

	# Return a list if the value has a comma.
	if ',' in value:
		value = re.split(R_COMMA, value)
	# These values are equivalent to None.
	elif value in ['', '.', 'NA']:
		return None

	return value


"""
│	(optional) Uncomment below if:
│	1. you want the previous matched result
│		to be constrained within the HGT proteins
│	2. you have already ran the analysis.py
│		and obtained the list of predicted HGT proteins (.txt)
│	Please enter the file path of the list of predicted HGT proteins (.txt)
│
│	For example:
│	HGT_txt_file = "result/hgts/nameOfSpecies.txt"
│	
"""
#============================================================
HGT_txt_file = ""
#============================================================
"""
read predicted HGT,
"""
#list_of_predicted_protein = []
#with open('', 'r') as reader2:
#	tempLines = reader2.readlines()
#	for line in tempLines:
#		temp = line.split('\t')
#		list_of_predicted_protein.append(temp[0])
		


#============================================================
"""
save result
"""
import pandas as pd
from IPython.display import display

df = dataframe( )
output_df = pd.DataFrame(columns=['Protein name','Evidence'])


for k,v in final_result.items():
	#if k in list_of_predicted_protein:
	temp_df = df[df["protein_id"] == k].head(1)
	#============================================================
	temp_df.insert(0, 'Protein name', [k], True)
	temp_df.insert(1, 'Evidence', [v], True)
	#============================================================
	toBeConcatenated = [output_df, temp_df]
	output_df = pd.concat(toBeConcatenated)
	


display(output_df)

output_df.to_csv( 'Matched_Protein.csv' )
output_df.to_excel( 'Matched_Protein.xlsx' )