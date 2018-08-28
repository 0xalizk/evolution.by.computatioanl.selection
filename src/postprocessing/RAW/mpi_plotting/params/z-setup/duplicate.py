import os, sys

def usage():
    print ("Usage: python duplicate.py [/abs/path/to/params/dir]\nExiting ..\n")
    sys.exit(1)
def getCommandLineArgs():
    try:
        return os.path.abspath(sys.argv[1])
    except:
        usage()
def setup(copy):
    if copy[-1]=='/':
        copy = copy[:-1]
    paste = '/'.join(copy.split('/')[:-1])+'/paste'
    if not os.path.isdir(copy):
        usage()
    if not os.path.isdir(paste):
        os.makedirs(paste)
    return copy, paste
def write_comments(output_file):
    comment  = "\n\n# this line is a comment, comments must be on separate lines\n"
    comment += "# 'input_files'      there will be 1 figure per each input file\n" 
    comment += "# 'columns'          used by master to determine figure dimensions\n"
    comment += "# 'files_per_pair'   used by master.py to determine how many files to to send to a worker, and by launcher.py to determine " 
    comment +="#                     the number of workers Pairing is useful is you want worker to impose xlim/ylim per pair for example\n" 
    comment += "# 'walltime'         optional, default = max (30, min(90, num_workers * 3))\n"
    comment += "# 'xlim','ylim'      optional (not applicable in wheel/bar3d). If not provided, these lims will be pair-specific"    
    output_file.write(comment)

#======================================================================================================
#old = ['Vinayagam', 'RDVina', 'USVina','URVina', 'USV',   'RDV',   'URV',   'ERV',    'Vina', 'Vin']
#old = ['Suratanee', 'RDSura', 'USSura','URSura', 'USSura','RDSura','URSura','ERSura', 'Sura', 'Sur']
#new = ['Perrimon', 'RDPerr', 'USPerr','URPerr', 'USPerr','RDPerr','URPerr','ERPerr', 'Perr', 'Per']
#old = ['Suratanee', 'Sura', 'Sur']
#new = ['IntAct', 'IntA', 'IntA']
#new = ['ER_IntAct', 'ER_IntA', 'ER_IntA']
old=[]
new=[]
override={}
# use this to override the value of some params, e.g. xlim/ylim .. use $util/max_deg.py to find the max degree, and use that as xlim/ylim in scatter
#override = {'file_extension':'png','dpi':300, 'files_per_worker':1} 					  # bar3d
#override = {'file_extension':'png','dpi':300, 'files_per_worker':6, 'xlim':50, 'ylim':50} # scatter
#override = {'file_extension':'png','dpi':300, 'files_per_worker':6, 'xlim':65, 'ylim':65} # wheel
skip     =  ['files_per_worker']# ['input_files','stamps']
#======================================================================================================

copy_dir, paste_dir = setup (getCommandLineArgs())

for root, dirs, files in os.walk(copy_dir.strip()):
    for f in files:
        if f[0]=='.' or f.split('.')[-1] != 'params':
            continue
        new_f=f
        for o,n in zip(old,new):
            new_f = new_f.replace(o,n)
        
        input  = open(os.path.join(root,f),'r').readlines()
        output = open(os.path.join(paste_dir,new_f),'w')
        
        for line in input:
            if line.strip() == '' or line.strip()[0]=='#': #skip comments and empty lines
                continue
            for o,n in zip(old,new):
                line = line.replace(o,n)
            try:
                key   = line.split('=')[0].strip()
            except:
                continue
            try:
                value = line.split('=')[1].strip()
            except:
                value =''
            if key in skip:
                continue
            if key in override.keys():
                value = str(override[key])
            output.write(key.ljust(30,' ')+' = '+value+'\n')
        write_comments(output)
print ("\n***********************************************")
print ('\n\t\tOnly *.params files were copy-pasted')
print ("\n\t\tThese params were overridden : "+str([k for k in override.keys()])+"\t(you can edit duplicate.py to change them)")
print ('\n\t\tFind the result in '+(paste_dir))
print ("\n***********************************************\n")
