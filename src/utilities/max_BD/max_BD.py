import sys, os
sys.path.insert(0, os.getenv('lib'))
import init, utilv4 as util
sys.path.insert(0, util.slash(os.getenv('util'))+'collect_files_by_name_pattern')
import collector_by_ANDin_patterns as collect 

########################################################################
def getCommandLineArgs():
    if len(sys.argv) < 2:
        sys.stdout.write ("Usage: python3 max_BD.py [/path/to/scratch/dir/]\nExiting..\n")
        sys.exit()
    return  str(sys.argv[1])
########################################################################
def print_title(patterns,root_dir):
    sys.stdout.write("\n  inspecting csv files in "+str(root_dir)+"  that meet the patterns "+str(patterns)+"\n")
    sys.stdout.write("\n "+"="*70)
    sys.stdout.write ("\n |     "+"Network"+" "*7+" "*11+"configs"+" "*14+"max(B)".ljust(7,' ')+"max(D)".ljust(7,' ')+'   |')
    sys.stdout.write("\n "+"="*70)
    sys.stdout.flush()
########################################################################
patterns     = ['RAW','INSTANCES', 'p100.0', 't100.0', 'csv']
root_dir     = getCommandLineArgs().strip()
MATCHES      = collect.get_matches(patterns, root_dir)
print_title(patterns,root_dir)
#$scratches/IntAct/AN_IntAct/v4_alpha0.2/v4eb_minknap_4X_target_scramble/02_raw_instances_simulation/data_points/AN_IntAct_RAW_INSTANCES_p000.1_t005.0_V4EB_MINKNAP_4X_TARGET_SCRAMBLE_alpha0.2.November-08-2016-h06m07s37.csv
STAMPS = []

for file_path in MATCHES:    
    if not os.path.isfile(file_path):
        sys.stdout.write ("\nnot a file, skipping: "+file_path)
        continue
    stamp = file_path.split('/')[-6].ljust(13,' ')+ file_path.split('/')[-4].ljust(35,' ')
 
    df = open (file_path, 'r')
    max_B, max_D = 0, 0
    try:
        while True:
            next(df) # skip G
            max_B    = max (max_B, max([int(b) for b in next(df).strip().split()]))
            max_D    = max (max_D, max([int(d) for d in next(df).strip().split()]))        
            next(df) # skip X
            next(df) # skip exec_time, core
    except: # EOF
        pass
    STAMPS.append((stamp, max_B, max_D))
    sys.stdout.write ("\n"+" "*7+str(stamp)+str(max_B).ljust(7,' ')+str(max_D))
    sys.stdout.flush()
sys.stdout.write ("\nDone: "+str(len(MATCHES))+" files inspected")