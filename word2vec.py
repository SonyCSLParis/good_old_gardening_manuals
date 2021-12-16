import json
import numpy as np
import pandas as pd
import plotly.express as px

vecs_umap = np.loadtxt("verbs/word2vec/w2v_umap.txt")
vecs = json.load(open("verbs/word2vec/verbs_w2v.json"))
freqs=np.loadtxt("verbs/word2vec/freqs.txt")

legend = []
for i,f in enumerate(freqs):
   if f<10:
   	legend.append("")
   else: legend.append(list(vecs.keys())[i])	

df = pd.DataFrame({
	    "verbs": list(vecs.keys()),
	    "N_occ": freqs,
	    "color": np.log(freqs),
	    "u0"   : vecs_umap[:,0],
	    "u1"   : vecs_umap[:,1],
	    "legend": legend

     })

fig = px.scatter(df, x="u0", y="u1", hover_name="verbs", hover_data=["N_occ"], text="legend", color= "color")
fig.show()
