import os,sys, numpy as np
sys.path.insert(0, os.getenv('lib'))
import fitting_lib

###########################################################
networks =    fitting_lib.networks
###########################################################

target_families = ['DB-sourced']#['PPIs', 'Regulatory','Regulatory','DB-sourced'] # , 'PPIs_orig']#optional, default: all families


nets        = [elem[0] for elem in sorted(networks().items(), key=lambda x: x[1]['abs_accuracy'])]#[n for n in networks().keys() ]#[0:]
if len(target_families)>0:
    nets        = [n for n in nets if networks()[n]['Family'] in target_families]
i=1
for n in nets:
    print (str(i).ljust(3,' ')+n.ljust(35,' ')+str(round(networks()[n]['abs_accuracy'],3)).ljust(7,' ') +' %  accuracy')
    #print(str(str(round(networks()[n]['abs_accuracy'],3))))
    i+=1

