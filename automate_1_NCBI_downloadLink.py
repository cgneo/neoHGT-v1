"""
///////////////////////////////////////////////////////
│	
│	Filename:	automate_1_NCBI_downloadLink.py
│	Description:
│	To obtain a `.txt` summary of all the NCBI RefSeq's
│	descriptions and download links
│ 	so that you can download the corrupted files.
│	==================================================
│	Authorship:	@cgneo, @HGTector
│	HGTector https://github.com/qiyunlab/HGTector
│	Made with love by @cgneo https://github.com/cgneo
│	Copyright:	Modified BSD License.
│	
///////////////////////////////////////////////////////
"""


from os import sep
import pandas as pd
from os.path import join
import ftplib



"""
│	(optional)
│	Change the directory where you want to save the RefSeq summary:
│	For example:
│	output = './hgtdb'
"""
#============================================================
output = './'
#============================================================

def get_summary(target):
	key = target.lower()
	fname = f'assembly_summary_{key}.txt'
	remote_file = f'/genomes/{key}/{fname}'
	local_file = join(output, fname)

	ftp = ftplib.FTP('ftp.ncbi.nlm.nih.gov', timeout=500)
	ftp.login()
	
	f = open(local_file, "w")
	
	# download summary
	print(f'Downloading {target} assembly summary...', end='', flush=True)
	with open(local_file, 'wb') as f:
		ftp.retrbinary('RETR ' + remote_file, f.write)
	print(' done.')

	# read summary
	print(f'Reading {target} assembly summary...', end='', flush=True)
	df = pd.read_csv(local_file, sep='\t', skiprows=1)
	print(' done.')
	return df



"""
│	Optional:
│	Uncomment below to enable downloading genebank's summary (~350MB),
"""
#============================================================
#df = pd.concat([df, get_summary('GenBank')])
#============================================================
df = get_summary('RefSeq')
print(f'Total number of genomes: {df.shape[0]}.')
