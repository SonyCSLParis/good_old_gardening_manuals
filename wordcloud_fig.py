import json
import wordcloud as wc


def mk_fig_wordcloud(fname, N):
   vs = json.load(open("verbs/"+fname))
   vs = {i: vs[i] for i in list(vs.keys())[:N]}

   w=wc.WordCloud(width=2000,height=1600,max_words=N)
   w.generate_from_frequencies(vs)
   w.to_file("figs/"+fname[:-4]+".png")

N = 300
fs = ["MOM_freq_verbs_sorted_freqs.json","MOM_freq_verbs_sorted_tfidf.json"] 
for f in fs: mk_fig_wordcloud(f, N)
