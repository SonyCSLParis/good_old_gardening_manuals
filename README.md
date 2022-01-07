# "Mining old manuals" (MOM) corpus



# Requirements

You need to install wordcloud, pandas, plotly if you want to visualize wordclouds and embeddings

# Wordclouds

We show the wordcloud of the 300 most significant words with the size of the word related its number of occurences in the corpus. The signifiance is [#occurences in the MOM corpus]/[#occurences in the Frantext corpus]

![MOM_freq_verbs_sorted_tfidf](figs/MOM_freq_verbs_sorted_tfidf.png?raw=true "300 most significant words with the size of the word related its number of occurences in the corpus. The signifiance is [#occurences in the MOM corpus]/[#occurences in the Frantext corpus]")

# Embedding

We used a Word2Vec embedding built on the french wikipedia. The embeddings are projected on 2D using UMAP. 

To visualize the map:
'''python
python3 word2vec.py
'''

![UMAP w2vec](figs/embed_verbs.png?raw=true "2d visualization of the embedding of verbs in MOM corpus")
