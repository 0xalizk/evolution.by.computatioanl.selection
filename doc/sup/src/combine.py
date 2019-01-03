import os,sys,shutil

root_directory =""
HEADER    = []
CONTENT   = []
try:
    root_directory  = str(sys.argv[1])
except:
    print ('Usage: python3 *.py [directory with *.tex files]  \nExiting...')
    sys.exit(1)
print("\n")
for root, dirs, files in os.walk(root_directory):
    for f in sorted(files):
        #print (str(f))
        if f.split('.')[-1] == 'tex' and f.split('/')[-1].strip() != 'combined.tex' and f.split('/')[-1].strip() != '00_preamble.tex':
            current_file   = open(os.path.join(root,f)).readlines()
            print (f.split('/')[-1].ljust(25,' ')+str(len(current_file))+"\tlines")
            cursor         = 0
            for line in current_file:
                if line.strip()=='%begin_custom_header':
                    #HEADER.append("%======================="+f.split('/')[-1].strip()+"==========================\n")
                    cursor+=1
                    while current_file[cursor].strip() != '%end_custom_header':
                        HEADER.append(current_file[cursor])
                        cursor +=1
                    break
                else:
                    cursor +=1
            
            for line in current_file[cursor:]:
                if line.strip()=='%begin_custom_content':
                    #CONTENT.append("%======================="+f.split('/')[-1].strip()+"==========================\n")
                    cursor += 1
                    while current_file[cursor].strip() != '%end_custom_content':
                        CONTENT.append(current_file[cursor])
                        cursor +=1
                    break
                else:
                    cursor+=1
print ("\ncombined into: "+str(os.path.join(root,"combined.tex"))+"\n")
output = open (os.path.join(root,"combined.tex"),'w')
for line in HEADER:
    output.write(line)
for line in CONTENT:
    output.write(line)
