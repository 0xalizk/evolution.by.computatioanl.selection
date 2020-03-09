import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
import numpy as np
import pandas as pd
from matplotlib import rcParams
#import seaborn as sns
import os,sys
import math

pd.set_option('display.precision', 3)
offx, offy = 0,0 #.75,-0.5
azim = -38  #-83  #81 # -81  #-38   #-15 
elev = 28  #19   #24 #  24  # 28   # 35 
alpha =.9
rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 16
rcParams['xtick.labelsize'] = 8
rcParams['ytick.labelsize'] = 8
#rcParams['font.family'] = 'sans-serif'  
#rcParams['font.family'] = 'serif'  
rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
rcParams['grid.alpha'] = 0.1
rcParams['axes.grid']=False
rcParams['ytick.minor.pad']=0.01
rcParams['ytick.major.pad']=0.01
rcParams['savefig.pad_inches']=.01
rcParams['grid.color']='white'
#rcParams['legend.facecolor']='#FFFFFF'
#rcParams['figure.frameon']=True
#rcParams['savefig.frameon']=True

#--------------------------------------------------------------------------------------
def get_plots():
    plots = {
                    '1-Bin':           {'title':'Gained Benefits (knapsack value)',            'color':'YlGn',    'measure_column':'Bin_avg',        'Z_label':'Benefits (norm. by no. nodes in deg. range)',     'location':(9,2)},
                    '2-Din':           {'title':'Incurred Damages (knapsack weight)',          'color':'OrRd',    'measure_column':'Din_avg',        'Z_label':'Damages (norm. by no. nodes in deg. range)',      'location':(9,2)},
                    '3-Bout':          {'title':'Lost Benefits (outside knapsack)',            'color':'OrRd',    'measure_column':'Bout_avg',       'Z_label':'Benefits (norm. by no. nodes in deg. range)',     'location':(9,2)},
                    '4-Dout':          {'title':'Cleansed Damages (outside knapsack)',         'color':'YlGn',    'measure_column':'Dout_avg',       'Z_label':'Damages (norm. by no. nodes in deg. range)',      'location':(9,2)},
         
                    '5-Bin_over_Din':  {'title':'Knapsack Benefit-to-Damage ratio',            'color':'YlGnBu',  'measure_column':'Bin_over_Din',   'Z_label':'Benefits-in / Damages-in (norm. by no. nodes in deg. range)',    'location':(9,2)},
                    '6-Bin_over_Bout': {'title':'Inside/Outside Knapsack Benefits Ratio',      'color':'PuBu',    'measure_column':'Bin_over_Bout',  'Z_label':'Benefits-in / Benefits-out (norm. by no. nodes in deg. range)',  'location':(9,2)},
                    '7-Dout_over_Din': {'title':'Outside/Inside Knapsack Damage Ratio',       'color':'YlGn',    'measure_column':'Dout_over_Din',  'Z_label':'Damages-out / Damages-in (norm. by no. nodes in deg. range)',    'location':(9,2)},
                    '8-Bout_over_Dout':{'title':'Outside Benefit/Outside Damage ratio',        'color':'Spectral','measure_column':'Bout_over_Dout', 'Z_label':'Benefits-out / Damages-out (norm. by no. nodes in deg. range)',  'location':(9,2)},
                    '9-Bout_over_Bin': {'title':'Outside/Inside knapsack Benefit Ratio',      'color':'GnBu',    'measure_column':'Bout_over_Bin',  'Z_label':'Benefits-out / Benefits-in (norm. by no. nodes in deg. range)',  'location':(9,2)}
                }
    return plots
#--------------------------------------------------------------------------------------
def get_colors():
    colors = {'green':          ['#003300', '#006600', '#009900', '#00cc00', '#00ff00', '#99ff99'], 
          'red':            ['#003300', '#006600', '#009900', '#00cc00', '#00ff00', '#99ff99'],
          'red':            ['#330000', '#800000', '#b30000', '#ff0000', '#ff4d4d', '#ff9999'],
          'stack':          ['#ff8000', '#1ad1ff', '#ff00ff', '#1a1aff', '#00cc00', '#7575a3'],
          'stack2':         ['#1a75ff', '#ffcc00', '#d2ff4d', '#ff33cc', '#800000', '#4da6ff'],
          
          'flatui':         ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"],
          'sns_hls_palette':[  x for x in ([ 
                                                   (0.33999999999999997, 0.85999999999999988, 0.86), 
                                                   (0.33999999999999997, 0.54799999999999993, 0.86),
                                                   (0.44399999999999962, 0.33999999999999997, 0.86), 
                                                   (0.75599999999999989, 0.33999999999999997, 0.86),
                                                   (0.86, 0.33999999999999997, 0.65199999999999991), 
                                                   (0.86, 0.33999999999999997, 0.33999999999999997),
                                                   (0.86, 0.65200000000000025, 0.33999999999999997), 
                                                   (0.75599999999999956, 0.86, 0.33999999999999997),
                                                   (0.44399999999999995, 0.86, 0.33999999999999997), 
                                                   (0.33999999999999997, 0.86, 0.54799999999999982)
                             ][2:])],
          'sns_cubehelix':[  x for x in reversed([
                                                   (0.10361479515598847, 0.094974942610061161, 0.20622110711523312),
                                                   (0.082593859561937211, 0.27284810506762325, 0.30772012231798751),
                                                   (0.17004232121057958, 0.43679759647517286, 0.22372555555555551),
                                                   (0.45876197523191747, 0.48057366087571074, 0.19972785287539777),
                                                   (0.75766937518242217, 0.47696440257052414, 0.43775520971413712),
                                                   (0.82995767878942039, 0.56320240352482709, 0.77627444444444438),
                                                   (0.76389785476493899, 0.75726887694191825, 0.94940230233452083),
                                                   (0.81065432716524155, 0.92184470519847239, 0.9373759048616408),  
                          ][2:])],
                          
                          
          'PRGn':[(0.51926183349945965, 0.2777393355089075, 0.57831605742959413), (0.73871589408201332, 0.61853135274905791, 0.79238755562726193), (0.92310650208417111, 0.86905037304934329, 0.92595156150705671), (0.88327567016377173, 0.94871203689014205, 0.8662053136264577), (0.61007306797831662, 0.83460208598305197, 0.59354096592641348), (0.20761246102697709, 0.55778547595528993, 0.28350634785259471)],
          'RdYlGn':[(0.88996540448244876, 0.28673587476505952, 0.19815456516602459), (0.98731257284388818, 0.64736641446749377, 0.36424452942960406), (0.99715494057711429, 0.91180315789054422, 0.60107653281267948), (0.89188774193034459, 0.95447904923382931, 0.60107653281267948), (0.61653212180324624, 0.83590927544762106, 0.41191849813741799), (0.22468281756429109, 0.65582470332874976, 0.34440600696732016)],
          'dark':[(0.0, 0.10980392156862745, 0.4980392156862745), (0.00392156862745098, 0.4588235294117647, 0.09019607843137255), (0.5490196078431373, 0.03529411764705882, 0.0), (0.4627450980392157, 0.0, 0.6313725490196078), (0.7215686274509804, 0.5254901960784314, 0.043137254901960784), (0.0, 0.38823529411764707, 0.4549019607843137)],
          'RdBu':[(0.75617071810890646, 0.21038062695194693, 0.22352941947824814), (0.94071511310689593, 0.60991928098248505, 0.48127645896930321), (0.98569780938765583, 0.88896578900954304, 0.83206460055182963), (0.86051519478068639, 0.91741638323839969, 0.94871203689014205), (0.53002693664793876, 0.74563630889443788, 0.85605537190156822), (0.18431373554117539, 0.47266437376246734, 0.7116493828156415)],
          'BrBG':[(0.63137257099151611, 0.39515572786331177, 0.095732413232326508), (0.85728566786822147, 0.72579778643215409, 0.44713571813761022), (0.96362937548581296, 0.92379854356541358, 0.81853134491864377), (0.82991158261018638, 0.92948866241118488, 0.91526336529675656), (0.46159172145759358, 0.77485583810245284, 0.72995003531960878), (0.087889274527483116, 0.47912342758739696, 0.44775088043773875)],
          'YlOrBr':[(0.99949250291375558, 0.95847751112545243, 0.71543254291310032), (0.99607843160629272, 0.85491734813241393, 0.4935178992795009), (0.99607843160629272, 0.69787006798912499, 0.24727413414740096), (0.95510957591673906, 0.50668205747417372, 0.11298731641442167), (0.83641677253386559, 0.33900808341362898, 0.02832756745537706), (0.62588237524032597, 0.21610150337219236, 0.014671281144461212)],
          'RdYlBu':[(0.8899654020900134, 0.2867358697326951, 0.19815456285608668), (0.9873125690696154, 0.64736638720885364, 0.36424451684869474), (0.99715494040753561, 0.91180315263360245, 0.61530182195690586), (0.91180317891830498, 0.96585929506515034, 0.91118797124327044), (0.6409842354868186, 0.82729718875812119, 0.9008073795488023), (0.34648211460899503, 0.54925027766716339, 0.75271050033547027)],
          'YlOrRd':[(0.99949250291375558, 0.91926182718837968, 0.60613612111876991), (0.99607843160629272, 0.80659747404210713, 0.41494810195530163), (0.99443291075089402, 0.6371549620347865, 0.27171088778505137), (0.98988081567427688, 0.40955019090689865, 0.19432526283404405), (0.91864667920505294, 0.1611380281693795, 0.12573625740467334), (0.76046137529260971, 0.013194925206549024, 0.14394464203540017)],
          'BuGn':[(0.88535179460749902, 0.95621684228672699, 0.96682814499911141), (0.74196079969406126, 0.90272972513647642, 0.86895810085184433), (0.51607844771123401, 0.81085737382664402, 0.72735103509005383), (0.31578624704304864, 0.71526337721768551, 0.53843907211341113), (0.17139562607980241, 0.58492889825035543, 0.32635141365668352), (0.017762399946942051, 0.44267590116052069, 0.18523645330877864)],
          'husl':[(0.9677975592919913, 0.44127456009157356, 0.5358103155058701), (0.7350228985632719, 0.5952719904750953, 0.1944419133847522), (0.3126890019504329, 0.6928754610296064, 0.1923704830330379), (0.21044753832183283, 0.6773105080456748, 0.6433941168468681), (0.23299120924703914, 0.639586552066035, 0.9260706093977744), (0.9082572436765556, 0.40195790729656516, 0.9576909250290225)],
          'pastel':[(0.5725490196078431, 0.7764705882352941, 1.0), (0.592156862745098, 0.9411764705882353, 0.6666666666666666), (1.0, 0.6235294117647059, 0.6039215686274509), (0.8156862745098039, 0.7333333333333333, 1.0), (1.0, 0.996078431372549, 0.6392156862745098), (0.6901960784313725, 0.8784313725490196, 0.9019607843137255)],
          'cubehelix':[(0.10231025194333628, 0.13952898866828906, 0.25601203194091809), (0.10594361078604106, 0.38097390115953311, 0.27015111282899046), (0.41061302726727622, 0.48044780541672255, 0.1891154277778484), (0.78291833825305668, 0.48158303462490826, 0.48672451968362596), (0.80461683292764064, 0.63657335693018458, 0.87965784029261251), (0.77756083743784588, 0.88403925212124479, 0.94520079923450517)],
          'PuBu':[(0.91128028210471657, 0.89471742265364707, 0.94292964584687178), (0.7678892871912788, 0.79684737850637999, 0.88944252869662122), (0.5687043576848273, 0.708266068907345, 0.83907728756175326), (0.31378700744872001, 0.6058439296834609, 0.77762400402742271), (0.075371012303466878, 0.47563245915899088, 0.70840447720359356), (0.016193772523718723, 0.3641061211333555, 0.57070360113592711)],
          'YlGn':[(0.95340254026300764, 0.98214532978394453, 0.7143252765431124), (0.80090735519633571, 0.91955402248045981, 0.61531720862669104), (0.59121877387458199, 0.82881969493978169, 0.5223068210424161), (0.34540562244022593, 0.71501731802435486, 0.4107804743682637), (0.17139562607980241, 0.56203001457102153, 0.29233373017872077), (0.017762399946942051, 0.42205306501949535, 0.22177624351838054)],
          'PiYG':[(0.81291811957078819, 0.25444060125771689, 0.56931950064266434), (0.93487120726529294, 0.67981547058797354, 0.83121877207475547), (0.98569780938765583, 0.90319108612397137, 0.94586697746725645), (0.9202614426612854, 0.96293733400457049, 0.85767013535780068), (0.6908881342878529, 0.86243753222858199, 0.48835066077755945), (0.38269896892940297, 0.64036911024766807, 0.18108420862871058)],
          'Set2':[(0.40000000596046448, 0.7607843279838562, 0.64705884456634521), (0.98131487965583808, 0.55538641635109398, 0.38740485135246722), (0.55432528607985565, 0.62711267120697922, 0.79595541393055635), (0.90311419262605563, 0.54185316071790801, 0.76495195557089413), (0.65371782148585622, 0.84708959004458262, 0.32827375098770734), (0.9986312957370983, 0.85096502233954041, 0.18488274134841617)],
          'RdGy':[(0.75617071810890646, 0.21038062695194693, 0.22352941947824814), (0.94071511310689593, 0.60991928098248505, 0.48127645896930321), (0.99430988115422869, 0.8975778607761159, 0.84067667231840248), (0.91180315789054422, 0.91180315789054422, 0.91180315789054422), (0.70196080207824707, 0.70196080207824707, 0.70196080207824707), (0.39561708885080671, 0.39561708885080671, 0.39561708885080671)],
          'OrRd':[(0.9955709345200483, 0.8996539852198433, 0.76299886072383205), (0.99215686321258545, 0.80292196484173051, 0.59001924781238335), (0.99051134235718674, 0.65763938987956327, 0.44688967828657111), (0.95864667682086724, 0.46189928428799498, 0.3103268086910248), (0.87044983471141146, 0.24855056188854516, 0.16822760867721892), (0.720230697183048, 0.024359862068120158, 0.01573241063777138)],
          'Paired':[(0.65098041296005249, 0.80784314870834351, 0.89019608497619629), (0.12572087695201239, 0.47323337360924367, 0.707327968232772), (0.68899655751153521, 0.8681737867056154, 0.54376011946622071), (0.21171857311445125, 0.63326415104024547, 0.1812226118410335), (0.98320646005518297, 0.5980161709820524, 0.59423301088459368), (0.89059593116535862, 0.10449827132271793, 0.11108035462744099)],
          'GnBu':[(0.8682814380701851, 0.94888120258555697, 0.84765860192915976), (0.75903115623137529, 0.90563629935769474, 0.75434065285850971), (0.58477509874923561, 0.83869282007217405, 0.73448675169664268), (0.3799308030044331, 0.74309882346321554, 0.80276817784589882), (0.20845829207523198, 0.59340256172067973, 0.76899655356126673), (0.049134950339794162, 0.42611304170945108, 0.68364477087469666)],
          'YlGnBu':[(0.91012687963597916, 0.96493656495038205, 0.6956401565495659), (0.69845444992476824, 0.88186082980212044, 0.71384853685603422), (0.39601692276842454, 0.76607460064046529, 0.74814303692649398), (0.17296425104141233, 0.629511748341953, 0.75952327461803659), (0.12764321927930794, 0.42666667968619104, 0.68613612020716952), (0.14357555420959697, 0.22523645092459285, 0.5905421235982109)],
          'PuOr':[(0.77462515760870543, 0.41291812588186827, 0.0461361029130571), (0.97654748313567219, 0.69250290183460006, 0.34571319336400314), (0.98854286881054154, 0.90319108612397137, 0.78369859036277323), (0.88043061074088602, 0.88612072958665733, 0.93448673977571373), (0.67112650941399965, 0.6404459996550691, 0.80307575183756208), (0.40046137921950398, 0.27566321106518016, 0.59146484557320089)],
          'colorblind':[(0.0, 0.4470588235294118, 0.6980392156862745), (0.0, 0.6196078431372549, 0.45098039215686275), (0.8352941176470589, 0.3686274509803922, 0.0), (0.8, 0.4745098039215686, 0.6549019607843137), (0.9411764705882353, 0.8941176470588236, 0.25882352941176473), (0.33725490196078434, 0.7058823529411765, 0.9137254901960784)],
          'deep':[(0.2980392156862745, 0.4470588235294118, 0.6901960784313725), (0.3333333333333333, 0.6588235294117647, 0.40784313725490196), (0.7686274509803922, 0.3058823529411765, 0.3215686274509804), (0.5058823529411764, 0.4470588235294118, 0.6980392156862745), (0.8, 0.7254901960784313, 0.4549019607843137), (0.39215686274509803, 0.7098039215686275, 0.803921568627451)],
          'RdPu_r':[(0.5048212261760936, 0.0039215688593685627, 0.47021914825719946), (0.73584007725996126, 0.061960785275361703, 0.52256825028681286), (0.90945021685431982, 0.28948866210731805, 0.60861209560843077), (0.97545559546526739, 0.53302577465188272, 0.6768935217576868), (0.98595924728056961, 0.7293041299371158, 0.74042292973574475), (0.99164936612634103, 0.8647289584664738, 0.85194925911286301)],
          'muted':[(0.2823529411764706, 0.47058823529411764, 0.8117647058823529), (0.41568627450980394, 0.8, 0.396078431372549), (0.8392156862745098, 0.37254901960784315, 0.37254901960784315), (0.7058823529411765, 0.48627450980392156, 0.7803921568627451), (0.7686274509803922, 0.6784313725490196, 0.4), (0.4666666666666667, 0.7450980392156863, 0.8588235294117647)],
          'bright':[(0.0, 0.24705882352941178, 1.0), (0.011764705882352941, 0.9294117647058824, 0.22745098039215686), (0.9098039215686274, 0.0, 0.043137254901960784), (0.5411764705882353, 0.16862745098039217, 0.8862745098039215), (1.0, 0.7686274509803922, 0.0), (0.0, 0.8431372549019608, 1.0)],
          'coolwarm':[(0.40442129049411762, 0.53464349044705883, 0.93200191263529408), (0.60316206791764704, 0.73152747735294121, 0.99956527853725485), (0.78672070135686278, 0.84480721036862749, 0.93981038494901958), (0.93066859633333332, 0.81887699965490202, 0.75914639069803924), (0.96731651566666665, 0.65747082880784313, 0.53816015072941181), (0.88464343869411766, 0.41001709788235297, 0.32250654924705885)],
          'hls':[(0.86, 0.37119999999999997, 0.33999999999999997), (0.82879999999999987, 0.86, 0.33999999999999997), (0.33999999999999997, 0.86, 0.37119999999999997), (0.33999999999999997, 0.82879999999999987, 0.86), (0.37119999999999997, 0.33999999999999997, 0.86), (0.86, 0.33999999999999997, 0.82879999999999987)],
          'Spectral':[(0.88535179460749902, 0.31903114388970766, 0.29042677143040824), (0.98731257284388818, 0.64736641446749377, 0.36424452942960406), (0.99715494057711429, 0.91180315789054422, 0.60107653281267948), (0.92887351442785826, 0.97154940577114335, 0.63806230531019326), (0.6334486913447287, 0.85213380350786094, 0.64367553065804872), (0.28004614044638243, 0.6269896416103139, 0.70242216306574201)]         
          }
    return colors
#--------------------------------------------------------------------------------------
def verify_and_print_stats(df1, df2):
    duplicates1          = len(df1.duplicated (subset=['p','t', 'Gene'])) - len(df1.drop_duplicates (subset=['p','t', 'Gene']))   
    duplicates2          = len(df2.duplicated (subset=['p','t', 'Gene'])) - len(df2.drop_duplicates (subset=['p','t', 'Gene']))
    
    # -------------------------drop duplicates if you have to------------------------------
    #df2                  = pd.DataFrame (df2.drop_duplicates (subset=['p','t', 'Gene']))
    #--------------------------------------------------------------------------------------
    
    print ("duplicates1: "+ str(duplicates1))
    print ("duplicates2: "+ str(duplicates2))


    #number of entries should be = |P| x |T| x |no. genes|
    try:      
        assert len (df1['p'])       ==     (len(set (df1['p'].tolist()))  * len(set (df1['t'].tolist()))   * len(set (df1['Gene'].tolist()))  )
        assert len (df1['t'])       ==     (len(set (df1['p'].tolist()))  * len(set (df1['t'].tolist()))   * len(set (df1['Gene'].tolist()))  )
        assert len (df1['Gene'])    ==     (len(set (df1['p'].tolist()))  * len(set (df1['t'].tolist()))   * len(set (df1['Gene'].tolist()))  )
        assert len (df2['p'])       ==     (len(set (df2['p'].tolist()))  * len(set (df2['t'].tolist()))   * len(set (df2['Gene'].tolist()))  )
        assert len (df2['t'])       ==     (len(set (df2['p'].tolist()))  * len(set (df2['t'].tolist()))   * len(set (df2['Gene'].tolist()))  )
        assert len (df2['Gene'])    ==     (len(set (df2['p'].tolist()))  * len(set (df2['t'].tolist()))   * len(set (df2['Gene'].tolist()))  )        
    except:
        print ("FAILED ...check the input file, possible duplicates")
        return False

    unique_degrees1, unique_degrees2 = list(sorted(set (df1['degree'])))  , list(sorted(set (df2['degree'])))
    print ("unique_degrees1: "+str(unique_degrees1)+"\nunique_degrees1: "+str(unique_degrees2))

    grouped1, grouped2 = df1.groupby(['Gene','degree']).sum().reset_index() , df2.groupby(['Gene','degree']).sum().reset_index()
    print ("number of genes1 : "+str(len(grouped1))+"\nnumber of genes : "+str(len(grouped1)))
    
    deg_count1 = {}
    for deg in unique_degrees1:
        deg_count1[deg] = len (         grouped1[         (grouped1['degree'] == deg)     ]        )
    deg_count2 = {}
    for deg in unique_degrees2:
        deg_count2[deg] = len (         grouped2[         (grouped2['degree'] == deg)     ]        )

    printout=[]
    for deg in sorted(deg_count1.keys()):
        printout.append([deg, deg_count1[deg]])
    print ("degree_count1: "+str(printout))
    printout=[]  
    for deg in sorted(deg_count2.keys()):
        printout.append([deg, deg_count2[deg]])
    print ("degree_count2: "+str(printout))    
    return True
#--------------------------------------------------------------------------------------
def getCommandLineArg():
    try:
        input_file  = str(sys.argv[1])
    except:
        print ('Usage: python3 [input-file (containing paths to BY_GENE.csv files) ] \nExiting...')
        sys.exit(1)
    return input_file
#--------------------------------------------------------------------------------------
def get_zlim_normalized (network1, network2, measure):
    df1                  = pd.read_csv(network1,header=0,delimiter='\t', dtype={
                                                                            'Gene':str,
                                                                            'p':float,
                                                                            't':float,
                                                                            'degree':float,
                                                                            'in-degree':float,
                                                                            'out-degree':float,
                                                                            'Bin_avg':float,
                                                                            'Bin_std':float,
                                                                            'Din_avg':float,
                                                                            'Din_std':float,
                                                                            'Bout_avg':float,
                                                                            'Bout_std':float,
                                                                            'Dout_avg':float,
                                                                            'Dout_std':float,
                                                                            'Bin_over_Din':float,
                                                                            'Bin_over_Bout':float,
                                                                            'Bin_over_Dout':float,
                                                                            'Din_over_Bin':float,
                                                                            'Din_over_Bout':float,
                                                                            'Din_over_Dout':float,
                                                                            'Bout_over_Bin':float,
                                                                            'Bout_over_Din':float,
                                                                            'Bout_over_Dout':float,
                                                                            'Dout_over_Bin':float,
                                                                            'Dout_over_Din':float,
                                                                            'Dout_over_Bout':float
                                                                            })
    df2                  = pd.read_csv(network2,header=0,delimiter='\t', dtype={
                                                                            'Gene':str,
                                                                            'p':float,
                                                                            't':float,
                                                                            'degree':float,
                                                                            'in-degree':float,
                                                                            'out-degree':float,
                                                                            'Bin_avg':float,
                                                                            'Bin_std':float,
                                                                            'Din_avg':float,
                                                                            'Din_std':float,
                                                                            'Bout_avg':float,
                                                                            'Bout_std':float,
                                                                            'Dout_avg':float,
                                                                            'Dout_std':float,
                                                                            'Bin_over_Din':float,
                                                                            'Bin_over_Bout':float,
                                                                            'Bin_over_Dout':float,
                                                                            'Din_over_Bin':float,
                                                                            'Din_over_Bout':float,
                                                                            'Din_over_Dout':float,
                                                                            'Bout_over_Bin':float,
                                                                            'Bout_over_Din':float,
                                                                            'Bout_over_Dout':float,
                                                                            'Dout_over_Bin':float,
                                                                            'Dout_over_Din':float,
                                                                            'Dout_over_Bout':float
                                                                            })
    bins1, bins2         = get_bins()
    plots                = get_plots()

    print ("\t\t"+("calculating zlimit for "+network1.split('/')[-1].split('_BY_GENE_')[0]+" ..") .ljust(45,' '),end='')
    
    zlim = 0
    for df, bins in [(df1, bins1), (df2, bins2)]:
        i=0 
        agg  = []
        for deg_range in bins:
                
            if (i<(len(bins)-1)):                  
                current_slice       = pd.DataFrame (df[         (df['degree'] >= bins[i])   &    (df['degree'] < bins[i+1])    ])                        
            else:                 
                current_slice       = pd.DataFrame (df[         (df['degree'] >= bins[i])      ])
                       
            divider       = float (len (current_slice.groupby(['Gene'])))                
            current_slice = current_slice.groupby(['p', 't']).sum().reset_index()               
            zdata         = current_slice[plots[measure]['measure_column']].tolist()                
            zdata         = [z/max(1,divider) for z in zdata]
            assert len(zdata) == 100 or len(zdata)==0
            if len(zdata)>0:                    
                if len(agg)>0:                        
                    agg = [(a+b) for a,b in zip(agg,zdata)]
                else:                       
                    agg = [z for z in zdata]
                
            i+=1
        zlim = max (zlim, max (agg))
    #ZLIMS [measure] = math.ceil(zlim)
    print (str(math.ceil(zlim)))
    return zlim
#--------------------------------------------------------------------------------------
def getPairs (BY_GENE_datafiles, measure):
    PAIRS = []
    counter = 0
    for f in range(int(len(BY_GENE_datafiles)/2)):
        network1 = BY_GENE_datafiles[counter].strip()
        network2 = BY_GENE_datafiles[counter+1].strip()
        zlim     = get_zlim_normalized(network1, network2, measure)
        PAIRS.append([  network1, network2, zlim  ])
        counter +=2
    return PAIRS
#--------------------------------------------------------------------------------------        
def init_ax(fig, dim1,dim2,loc,zlim,zlabel, title):
    ax = fig.add_subplot(dim1,dim2,loc, projection='3d')
            
    ax.set_title(title)
    dx = [.2]*(100)	 #bar_width
    dy = [.2]*(100)  #bar length
    
    xticks, yticks = get_ticks() 

    ax.set_xticks (  [x + offx for x in xticks]  )
    ax.set_yticks (  [y + offy for y in yticks]  )
    ax.set_zticks (    range(5,int(zlim)+1,math.ceil(float(zlim+1)/5.0))         )
 
    ax.set_xticklabels (['0.1','1','5','10','15','20','25','50','75','100'], rotation=-45, verticalalignment='baseline', horizontalalignment='right')    #ax.w_xaxis.set_ticklabels(['0.1','1','5','10','15','20','25','50','75','100'])
    ax.set_yticklabels (['100','75','50','25','20','15','10','5','1','0.1'], rotation=-45, verticalalignment='baseline', horizontalalignment='left')    #ax.w_yaxis.set_ticklabels(['100','75','50','25','20','15','10','5','1','0.1'])    
    ax.set_zticklabels ([str(zl) for zl in range(5,int(zlim)+1,5)])

    ax.set_xlabel ('Tolerance (% edges)')
    ax.set_ylabel ('Pressure (% nodes)')
    ax.set_zlabel (zlabel)
                
    ax.tick_params (axis='x', pad=0.1, width=1,length=1,labelsize=8,direction='in') #valid keywords: ['size', 'width', 'color', 'tickdir', 'pad', 'labelsize', 'labelcolor', 'zorder', 'gridOn', 'tick1On', 'tick2On', 'label1On', 'label2On', 'length', 'direction', 'left', 'bottom', 'right', 'top', 'labelleft', 'labelbottom', 'labelright', 'labeltop']
    ax.tick_params (axis='y', pad=0.1, width=1,length=1,labelsize=8,direction='in')
    ax.tick_params (axis='z', pad=0.1, width=1,length=1,labelsize=8,direction='in')
                
    ax.set_zlim   (top=zlim)
    ax.view_init  (elev=elev,azim=azim)
    return ax, dx, dy
#-------------------------------------------------------------------------------------- 
def get_ticks():
    xticks = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
    yticks = [9.5, 8.5, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5, 0.5]
    return xticks, yticks
#--------------------------------------------------------------------------------------  
def get_bins():
    return [1.0, 6.0, 11.0, 16] , [1.0, 6.0, 11.0, 16]
if __name__ == "__main__": 
    input_file, plots, colors, plots_dir = getCommandLineArg(), get_plots() , get_colors() , os.path.join(os.getcwd(),'plots')
    if not os.path.isdir(plots_dir):
        os.mkdir(plots_dir)
    datapoints_files = open (input_file).readlines()
    
    verify = True
    for measure in sorted(plots.keys()):
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\nprocessing "+measure)
        
        fig = plt.figure(figsize=(30, 70))
        fig.subplots_adjust(hspace = .01, wspace=.01)

        pos=1
        for pair in getPairs (datapoints_files, measure):
            data_file1, data_file2, zlim = pair[0].strip() ,  pair[1].strip()  ,  pair[2]
            title1, title2 = data_file1.split('/')[-1].split('_BY_GENE_')[0], data_file2.split('/')[-1].split('_BY_GENE_')[0]
            print ("\t\tplotting "+str(data_file1.split('/')[-1])+"\n\t\tplotting "+str(data_file2.split('/')[-1]))
            df1                  = pd.read_csv(data_file1,header=0,delimiter='\t', dtype={
                                                                            'Gene':str,
                                                                            'p':float,
                                                                            't':float,
                                                                            'degree':float,
                                                                            'in-degree':float,
                                                                            'out-degree':float,
                                                                            'Bin_avg':float,
                                                                            'Bin_std':float,
                                                                            'Din_avg':float,
                                                                            'Din_std':float,
                                                                            'Bout_avg':float,
                                                                            'Bout_std':float,
                                                                            'Dout_avg':float,
                                                                            'Dout_std':float,
                                                                            'Bin_over_Din':float,
                                                                            'Bin_over_Bout':float,
                                                                            'Bin_over_Dout':float,
                                                                            'Din_over_Bin':float,
                                                                            'Din_over_Bout':float,
                                                                            'Din_over_Dout':float,
                                                                            'Bout_over_Bin':float,
                                                                            'Bout_over_Din':float,
                                                                            'Bout_over_Dout':float,
                                                                            'Dout_over_Bin':float,
                                                                            'Dout_over_Din':float,
                                                                            'Dout_over_Bout':float
                                                                            })
            df2                  = pd.read_csv(data_file2,header=0,delimiter='\t', dtype={
                                                                            'Gene':str,
                                                                            'p':float,
                                                                            't':float,
                                                                            'degree':float,
                                                                            'in-degree':float,
                                                                            'out-degree':float,
                                                                            'Bin_avg':float,
                                                                            'Bin_std':float,
                                                                            'Din_avg':float,
                                                                            'Din_std':float,
                                                                            'Bout_avg':float,
                                                                            'Bout_std':float,
                                                                            'Dout_avg':float,
                                                                            'Dout_std':float,
                                                                            'Bin_over_Din':float,
                                                                            'Bin_over_Bout':float,
                                                                            'Bin_over_Dout':float,
                                                                            'Din_over_Bin':float,
                                                                            'Din_over_Bout':float,
                                                                            'Din_over_Dout':float,
                                                                            'Bout_over_Bin':float,
                                                                            'Bout_over_Din':float,
                                                                            'Bout_over_Dout':float,
                                                                            'Dout_over_Bin':float,
                                                                            'Dout_over_Din':float,
                                                                            'Dout_over_Bout':float
                                                                            })
            bins1, bins2         = get_bins () 
        
            #if verify:
            #    if not verify_and_print_stats(df1, df2):
            #        continue

            for  df, bins, col, title in [(df1,bins1,0, title1), (df2,bins2,1, title2)]:
                #----------------------------------------------------------------------------------------------------------------------------------------------
                ax, dx, dy = init_ax (fig, plots[measure]['location'][0], plots[measure]['location'][1], pos+col, zlim, plots[measure]['Z_label'], title)
                #----------------------------------------------------------------------------------------------------------------------------------------------              
                z_offset = [0.0]*len (set(df['p'].tolist())) * len (set(df['p'].tolist()))
                patches = []
                i=0
                for deg_range in bins:
                    
                    if (i<(len(bins)-1)):
                        current_slice       = pd.DataFrame (df[         (df['degree'] >= bins[i])   &    (df['degree'] < bins[i+1])    ])
                        #current_slice_label = (str(int(bins[i])) + "-"+str(int(bins[i+1]))).ljust(10,' ')  + "("+str(len(current_slice.groupby(['Gene'])))+")"    
                        label_left  = str(int(bins[i])) + "-"+str(int(bins[i+1]))
                        label_left = label_left.ljust(12-len(label_left),' ') 
                        current_slice_label = label_left + ("("+str(len(current_slice.groupby(['Gene'])))+")")
                    else:
                        current_slice       = pd.DataFrame (df[      (df['degree'] >= bins[i])      ])
                        #current_slice_label = (">="+str(int(bins[i]))).ljust(10,' ') + "("+str(len(current_slice.groupby(['Gene'])))+")"
                        label_left = str(">="+str(int(bins[i])))
                        label_left = label_left.ljust(10-len(label_left),' ') 
                        current_slice_label = label_left + ("("+str(len(current_slice.groupby(['Gene'])))+")")
                                            
                    divider = float (len (current_slice.groupby(['Gene'])))
                    current_slice = current_slice.groupby(['p', 't']).sum().reset_index()  
                
                    zdata  = current_slice[plots[measure]['measure_column']].tolist()
                    
                    #--------------NORMALIZE BY NO. OF GENES------------
                    zdata = [z/max(1,divider) for z in zdata]   
                    #---------------------------------------------------
                    assert len(zdata)==100 or len(zdata)==0
                    #---------------------------------------------------
                    if len(zdata)>0:
                        zdata         = (np.array(zdata)).reshape(10, 10)
                        Ts, Ps        = np.meshgrid ([x for x in get_ticks()[0]], [x for x in get_ticks()[0]] )               
                        zdata, Ps, Ts = zdata.flatten(), Ps.flatten(), Ts.flatten()
                        #------------------------------------------------------------------------------------------------------------------
                        ax.bar3d (Ts, Ps, z_offset, dx, dy, zdata , alpha=alpha, color=colors[plots[measure]['color']][i], edgecolor='')  #
                        #------------------------------------------------------------------------------------------------------------------                
                        z_offset = [a+b for a,b in zip(z_offset, zdata)]            
            
                    patches.append (mpatches.Patch(color=colors[plots[measure]['color']][i], label=current_slice_label))
            
                    i+=1
                
                #--------------------------------------------------LEGEND---------------------------------------------------------------------------
                patches.reverse()
                legend = ax.legend (handles=patches, frameon=False, borderaxespad=1.0, borderpad=1.0, fontsize= 8, markerscale=0.0, loc='upper left',
                                    bbox_to_anchor = (0.2, 0.825), title='degree range  (no. nodes)',shadow=False)                  
                legend.get_title().set_fontsize('9') #frame = legend.get_frame() #frame.set_facecolor('white') #frame.set_edgecolor('white')
                #------------------------------------------------------------------------------------------------------------------------------------
            pos +=2                          
        plt.savefig(plots_dir+"/"+measure+".png")
