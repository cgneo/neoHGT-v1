
"""
///////////////////////////////////////////////////////
│	
│	Filename:	automate_3_plot_close_distal.py
│	Description:
│	To print close scores (and distal scores)
│	so that you can copy paste them into analyze.py
│	in order to make a scatter plot with labels
│	==================================================
│	Authorship:	@cgneo
│	Copyright:	Modified BSD License.
│	Made with love by @cgneo https://github.com/cgneo
│	
///////////////////////////////////////////////////////
"""


list_of_protein_id = [  'WP_162306552.1',
						'WP_147664389.1',
						'WP_162306824.1',
						'WP_147664305.1',
						'WP_147662173.1',
						'WP_147661599.1',
						'WP_147661598.1',
						'WP_147661168.1',
						'WP_147661826.1',
						'WP_147664706.1' ]


""" 
│	⬇️ Mandatory !!!
│	Please enter the name of the folder
│	that contains the "scores.tsv" file,
│	which is generated after running analyze.py
│	
│	For example:
│	folder_name = "./search_dir"
"""
#============================================================
folder_name = "./"
#============================================================



final_dict = dict()

with open(f'./{folder_name}/scores.tsv', 'r') as reader1:
	temp = reader1.readlines()
	for line in temp:
		temp_str = line.split('\t')
		if temp_str[1] in list_of_protein_id:
										# 5 is close, 6 is distal
			final_dict[temp_str[1]] = ( temp_str[5], temp_str[6] )

# according to the order
for i in range(len(list_of_protein_id)):
	close, distal = final_dict[list_of_protein_id[i]]
	"""
	│	Uncomment below to print close scores
	"""
	#============================================================
	#print( float(close) )
	#============================================================
	"""
	│	Uncomment below to print distal scores
	"""
	#============================================================
	print( float(distal) )
	#============================================================