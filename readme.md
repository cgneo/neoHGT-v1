
<p align="center">
	<a href="https://github.com/cozv/neoHGT">
		<img src="./neoHGT.png" width="250">
	</a><br>
</p>

# neoHGT: Horizontal gene transfer in Archaea

You are visiting neoHGT v1, which is no longer maintained.

Please visit neoHGT v2 which can be found [here](https://www.github.com/cgneo/neoHGT).

## Table of Contents
1. [About](#about)
2. [Installation](#installation)
3. [Database](#database)
4. [Search](#search)
5. [Analyze](#analyze)
6. [License](#license)
7. [Copyright](#copyright)

## About
**neoHGT** can predict the horizontal/lateral gene transfer (HGT) for species of interest. This project is based on [HGTector](https://github.com/qiyunlab/HGTector) developed by Qiyun lab, but the difference is that useful utilities (listed below) are added:

File name | Functionality
--- | ---
`automate_1.1_NCBI_downloadLink.py` | To obtain a `.txt` summary of all the NCBI RefSeq's descriptions and download links so that you can download the corrupted files.
`automate_1.2_download_print_progress.py` | Given the `.txt` summary of all the NCBI RefSeq's descriptions, we can now download the `.gz` files.
`automate_1.3_verify_gz.py` | To verify the integrity of `.gz` files and print the corrupted ones' file names (because a single corrupted file will cause building database to fail).
`automate_2_sort_escore.py` | (Pre-requisite: doing a native diamond search) To sort each of the BLASTP result by e-score, filter out results (for example, we're interested in the proteins where aftering sorting by e-score, the second one must be a bacteria), and then output the list of proteins that fits the pattern and save it into `Excel` or `CSV` file.
`automate_3_read_gtf.py` | To generate `Excel` file with human-readable annotations (see "product" column) for HGTector: analysis.py's generated txt file (containing the predicted HGT-derived genes).
`automate_3_plot_close_distal.py` | To print close and distal scores in the console so that you can copy paste them into analyze.py in order to make a scatter plot with labels.

  


## Installation
The project is written in Python3.<br>
Recommended installation method:

```
python setup.py install --record location.txt
```
This way, you have `location.txt` which tracks the path of the program.
This could be useful for uninstalling and modifying the code.

To uninstall, run:
```
xargs rm -rf < location.txt
```
or
```
pip uninstall hgtector
```



For more comprehensive guideline, please refer to [HGTector's Installation](https://github.com/qiyunlab/HGTector/blob/master/doc/install.md) for full information.



## Database

The problem with HGTector's databasr.py is that it uses FTP library for downloading which isn't reliable, and triggers [EOFError when downloading genomes for the database](https://github.com/qiyunlab/HGTector/issues/74).

neoHGT adated `urllib` instead of FTP to solve the `EOFError` in the downloading phase.

<hr/>

Another common problem with HGTector's databasr.py is that in the diamond database compiling phase, most users will encounter [Error: Tokenizer Exception](https://github.com/qiyunlab/HGTector/issues/76).

I personally solved this problem by replacing the `prot.accession2taxid.gz` with the official one avaliable on NCBI: ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz.


Please refer to [HGTector's Database](https://github.com/qiyunlab/HGTector/blob/master/doc/database.md) for more information.



## Search

neoHGT added `try` and `except` to make the searching process more robust.

To perform a search, please refer to [HGTector's Search](https://github.com/qiyunlab/HGTector/blob/master/doc/search.md) for more information.



## Analyze

neoHGT changed the output format of the graph from `.png` to `.pdf` for better resolution and publication purposes.

(optional): To add labels to your scatter plot, please locate to the path where analyze.py is running (`location.txt`), and modify the code of analyze.py on that path by scrolling to the very bottom and uncommenting the last function. You'll see a list of `ax.scatter(close, distal, marker=next(marker), label="")`, feel free to modify as you need.
For your convenience, run `automate_3_plot_close_distal.py` to copy paste a list of close scores (1st parameter in ax.scatter), and then a list of distal scores (2nd parameter in ax.scatter) into your analyze.py to save time.

To perform analysis, please refer to [HGTector's Analyze](https://github.com/qiyunlab/HGTector/blob/master/doc/analyze.md) for more information.


## Publication

This repository was a result of my internship at LOB - Laboratoire d'Optique et Biosciences, where we published a paper on [Nature Communication](https://www.nature.com/articles/s41467-023-36487-z).

> Filée, J., Becker, H. F., Mellottee, L., Eddine, R. Z., Li, Z., Yin, W., Lambry, J.-C., Liebl, U., & Myllykallio, H. (2023, February 15). Bacterial origins of thymidylate metabolism in Asgard Archaea and Eukarya. Nature Communication. Retrieved February 18, 2023, from https://www.nature.com/articles/s41467-023-36487-z



## Works cited

> Zhu Q, Kosoy M, Dittmar K. HGTector: [an automated method facilitating genome-wide discovery of putative horizontal gene transfers](https://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-15-717). *BMC Genomics*. 2014. 15:717.


## License

Copyright (c) 2021, [Zhihui Li](https://github.com/cozv). Licensed under [BSD 3-clause](http://opensource.org/licenses/BSD-3-Clause).


Copyright (c) 2013-2020, [Qiyun Zhu](mailto:qiyunzhu@gmail.com) and [Katharina Dittmar](mailto:katharinad@gmail.com). Licensed under [BSD 3-clause](http://opensource.org/licenses/BSD-3-Clause). See full license [statement](LICENSE).
