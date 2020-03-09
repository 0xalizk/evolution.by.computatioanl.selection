import os, sys

input = open ('01.collect').readlines()
output = open ('04.batch_plot','w')

for line in input:
    output.write('bash 03.organize.batch '+line)

print ("Done. Now run: source 04.batch_plot")
