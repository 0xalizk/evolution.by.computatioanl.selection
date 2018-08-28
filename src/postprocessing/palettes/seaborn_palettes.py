import seaborn as sns
palettes = ['deep','muted','bright','dark','colorblind','Paired','BuGn','GnBu','OrRd',
            'PuBu','YlGn','YlGnBu','YlOrBr','YlOrRd','BrBG','PiYG','PRGn','PuOr','RdBu',
            'RdGy','RdYlBu','RdYlGn','Spectral','cubehelix',
'coolwarm','RdPu_r','hls','husl','deep','muted','pastel','bright','dark','Set2'] 

for pal in set(palettes):
    print("\'"+pal+"\':"+str(sns.color_palette (pal, 6))+",")
