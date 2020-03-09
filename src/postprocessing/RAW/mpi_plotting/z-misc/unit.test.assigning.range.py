def assign_range(slices, b, d):
    b2d_ratio, d2b_ratio = 0, 0 
    the_right_key=None                 
    if b>0 or d>0:
        b2d_ratio, d2b_ratio = (float(b)/float(b+d))*100,  (float(d)/float(b+d))*100
        the_right_key_for_b = [key for key in sorted(slices.keys()) if b2d_ratio >= slices[key]['range'][0]]
        the_right_key_for_d = [key for key in sorted(slices.keys()) if d2b_ratio <= slices[key]['range'][1]]
        the_right_key = [key for key in the_right_key_for_b if key in the_right_key_for_d][0]      
    else:
        the_right_key =  [key for key in slices.keys() if slices[key]['range'][0]==0 and  slices[key]['range'][1]==0     ][0]
        
    slices[the_right_key]['count'] += 1

    return slices[the_right_key]['label']


slices_detailed           = { 
                               1  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                               2  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'90:10', 'range':(90,10)},
                               3  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'80:20', 'range':(80,20)},
                               4  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'70:30', 'range':(70,30)},
                               5  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'60:40', 'range':(60,40)},
                               6  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},                               
                               7  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'40:60', 'range':(40,60)},
                               8  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'30:70', 'range':(30,70)},
                               9  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'20:80', 'range':(20,80)},
                               10 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'10:90', 'range':(10,90)}, 
                               11 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},                             
                               
                               12 :{'fractions':[], 'count':0, 'color':'black', 'avg':0, 'std':0, 'label':'0:0', 'range':(0,0)},
                }
b, d = 0, 0
print ("Enter a negative value to exit")
while True:
    b = input("b: ")
    d = input("d: ")
    if b*d>=0:
        print ("\trange:"+assign_range(slices, b, d)+"\n")
    else:
        break
print("\nGoodbye!\n")