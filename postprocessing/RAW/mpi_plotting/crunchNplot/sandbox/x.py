#######################################################################################
def assign_range(slices, b, d):
    right_key, b2d_ratio, d2b_ratio = 0,0,0
    if b==0 and d==0:
        right_key =   [key for key in slices['segments'].keys() if slices['segments'][key]['range'][0]==0 and  slices['segments'][key]['range'][1]==0]

    elif b>=d: 
        b2d_ratio, d2b_ratio = round((float(b)/float(b+d))*100, 12), round((float(d)/float(b+d))*100,12)
        right_key = [key for key in slices['segments'].keys() if (b2d_ratio-slices['segments'][key]['range'][0]) >=0 and (b2d_ratio-slices['segments'][key]['range'][0]) <slices['interval']  and (slices['segments'][key]['range'][1]-d2b_ratio)>=0 and (slices['segments'][key]['range'][1]-d2b_ratio)<slices['interval'] ]
    
    else:
        b2d_ratio, d2b_ratio = (float(b)/float(b+d))*100, (float(d)/float(b+d))*100
        right_key = [key for key in slices['segments'].keys() if (slices['segments'][key]['range'][0]-b2d_ratio) >=0 and (slices['segments'][key]['range'][0]-b2d_ratio) <slices['interval']  and (d2b_ratio-slices['segments'][key]['range'][1])>=0 and (d2b_ratio-slices['segments'][key]['range'][1])<slices['interval'] ]
    
    
    assert len(right_key)==1
    return right_key[0]
#######################################################################################

slices = {    'interval':10,
                                    'segments':{
                                                 1  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                                                 2  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'90:10', 'range':(90,10)},
                                                 3  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'80:20', 'range':(80,20)},
                                                 4  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'70:30', 'range':(70,30)},
                                                 5  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'60:40', 'range':(60,40)},
                                                 6  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},                               
                                                 7  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'40:60', 'range':(40,60)},
                                                 8  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'30:70', 'range':(30,70)},
                                                 9  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'20:80', 'range':(20,80)},
                                                 10 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'10:90', 'range':(10,90)}, 
                                                 11 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},                             
                                                 12 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'0:0',   'range':(0,0)}
                                                }
                                }
n=13
for i in range(0,n+1,1):
    for j in range(0,n+1,1):
        if i+j==n:
            print (str(i).ljust(4,' ')+'/  '+str(j).ljust(4,' ')+'=>  '+slices['segments'][assign_range(slices,i,j)]['label'])
