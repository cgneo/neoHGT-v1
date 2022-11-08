"""
///////////////////////////////////////////////////////
│	
│	Filename:	auto_print_progress.py
│	Description:
│	To print progress abr
│	==================================================
│	Authorship:
│	stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
│	
///////////////////////////////////////////////////////
"""
import requests

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
		printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
	# Print New Line on complete
	if iteration == total: print()


with open("assembly_summary_genbank.txt") as f:
    temp = f.readlines()
    counter = 0
    for line in temp:
        counter += 1
        if counter >= 3:
            list_of_attr = line.split("\t")
            url = list_of_attr[-4]
            filename = list_of_attr[-4].split("/")[-1]
            r = requests.get(url + filename + "_genomic.fna.gz")
            with open(filename + "_genomic.fna.gz",'wb') as f_temp:
                f_temp.write(r.content)
                f_temp.close()
            print(printProgressBar(counter, 1435104))