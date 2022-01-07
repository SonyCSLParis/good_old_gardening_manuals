# "Mining old manuals" (MOM) corpus

- **Guide pratique du jardinier français - Traité complet d’horticulture** par P. Desmoulins 1881 *(495 p.)*
- **L’école du jardin potager** par M. de Combles 1802 *(587 p.)*
- **Le potager moderne** par Gressent 1863 *(499 p.)*
- **Manuel complet du jardinier maraîcher pépiniériste botaniste fleuriste et paysagiste** par L. Noisette 1825 *(637 p.)*
- **Manuel de culture maraîchere** par Deny et Rodigas 1853 *(317 p.)*
- **Manuel pratique de jardinage** par Courtois-Gérard 1868 *(500 p.)*
- **Manuel pratique de la culture maraîchere de Paris** par Moreau et Daverne 1845 *(389 p.)*


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
