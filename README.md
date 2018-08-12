# vcfparser
Python code to analyze a vcf file

## Introduction

The python script parses out the position, alternate alleles at each position. It also looks for number of reads that are supporting the presence of the alternalte allele. This is calulated by counting the percentage of the number of left (5' end, RPL tag) and right (3' end, RPR tag) and dividing against the total number of reads covering that particular locus. Then it searches for the allele frequency and the dbSNP ID in the [ExAC database](http://exac.hms.harvard.edu/) using its REST API. If no allele frequency is found it returns "NA" and if no dbSNP ID is found "." is returned. The output is stored in the form of a table in the file annotated.{vcf filename}.txt

## Dependencies
1) Python3.6+
2) Python libaries used:
   a) requests (for REST API)
   b) json (for parsing json records)
   c) argparse (for passing inputs from bash into python)
   d) time (calculating execution time)

## Syntax
python3 vcfparser.py --vcf {vcf filename}

## Example
python3 vcfparser.py --vcf "Challenge_data (1).vcf"

Output
annotated.{vcf filename}.csv
