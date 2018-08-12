## Use python 3.6
## Syntax: python3 vcfparser.py --vcf "Challenge_data (1).vcf"
import requests
import json
import argparse
import time
time_start = time.time()
parser = argparse.ArgumentParser(
     prog='vcfparser',
     usage='''python3 vcfparser.py --vcf [vcf file]''',
     description='''This program analyzes a vcf file for various variants, their corresponding reads support and queries the ExAC database for allele frequency and dbSNP ID''',
     epilog='''This program requires python3 with requests,json,argparse and time libraries.''')
parser.add_argument('--vcf', type=str, help='The vcf file', required=True)
args = parser.parse_args()
vcffile=args.vcf

with open("annotated."+vcffile.replace("vcf","")+"csv",'w') as xyz:
  xyz.write('sep="\\t"\n')
  xyz.write("Chromosome\tPosition\tReference allele\tAlternate allele\tType of substitution\tTotal depth of locus\tNumber of reads supporting variant\tPercentage of reads supporting variant\tAllele frequency\tdbSNP id\n")
  for line in open(vcffile,'r'):
    if line.startswith("#")==True: # Ignoring the comment lines of a vcf file
       pass
    else:
       line2=line.split("\t")
       chromosome=line2[0] # Chromosome
       position=line2[1] # Position
       reference=line2[3] # Reference allele
       alternate=line2[4] # Alternate allele
       alternate2=alternate.split(",")
       num_alt_all=len(alternate2) # Number of alternate alleles
       info=line2[7].split(";")
       for i in range(len(info)):
           # Looking for type of variation
           if "TYPE=" in info[i]:
              variation=info[i][5:]
              variation2=variation.split(",")
           # Looking for depth of coverage
           elif "DP=" in info[i]:
              depth=int(info[i][3:])       
           # Number of reads supporting the variant
           elif "RPR=" in info[i]:
              rightreads=info[i][4:] # Extracting the number of supporting reads lying right to the proposed variant
              rightreads2=rightreads.split(",")
           elif "RPL=" in info[i]:
              leftreads=info[i][4:] # Extracting the number of supporting reads lying left to the proposed variant
              leftreads2=leftreads.split(",")
       # Iterating over each of the alternate alleles
       for i in range(num_alt_all):  
           # Using REST API for getting allele frequency and dbSNP ID from ExAC database
           r = requests.get('http://exac.hms.harvard.edu/rest/variant/variant/'+chromosome+'-'+position+'-'+reference+'-'+alternate2[i])
           #print (chromosome+'-'+position+'-'+reference+'-'+alternate2[i])
           r = json.dumps(r.json()) # Converting the ExAC output into json 
           loaded_r = json.loads(r)
           try:
              allele_freq=loaded_r['allele_freq'] # Extracting allele frequency
           except KeyError:
              allele_freq="NA" # Print "NA" when no allele frequency is found corresponding to the variant
           try:
              rsid=loaded_r['rsid'] # Extracting dbSNP ID
           except KeyError:
              rsid="." # Print "." when no dbSNP ID is found corresponding to the variant
           xyz.write(chromosome+"\t"+position+"\t"+reference+"\t"+alternate2[i]+"\t"+variation2[i]+"\t"+str(depth)+"\t"+str(int(leftreads2[i])+int(rightreads2[i]))+"\t"+str(((int(leftreads2[i])+int(rightreads2[i]))*100)/depth)+"\t"+str(allele_freq)+"\t"+rsid+"\n") # Writing to table
xyz.close()

print ("Output written to "+"annotated."+vcffile.replace("vcf","")+"txt")
print ("Time taken to parse "+vcffile+": "+str(time.time()-time_start)+" seconds")
