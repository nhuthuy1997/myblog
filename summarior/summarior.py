import pickle
import numpy as np
from pyvi import ViTokenizer
import nltk
from gensim.models import KeyedVectors 
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from django.conf import settings
from crawler.general import get_page_content
from functools import reduce
from crawler.models import *

w2v = KeyedVectors.load_word2vec_format(settings.DATA_DIR)

def exec(post, content):
  try:
    if post.source_info.name == 'V' and not post.has_summary:
      content.lower().strip()
      sentences = nltk.sent_tokenize(content)
      vocab = w2v.wv.vocab
      X = []
      for sentence in sentences:
        sentence = ViTokenizer.tokenize(sentence)
        words = sentence.split(" ")
        sentence_vec = np.zeros((100))
        for word in words:
          if word in vocab:
            sentence_vec+=w2v.wv[word]
        X.append(sentence_vec)
      n_clusters = post.sentences_of_summary
      kmeans = KMeans(n_clusters=n_clusters)
      kmeans = kmeans.fit(X)
      avg = []
      for j in range(n_clusters):
        idx = np.where(kmeans.labels_ == j)[0]
        avg.append(np.mean(idx))
      closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
      ordering = sorted(range(n_clusters), key=lambda k: avg[k])
      summary = ' '.join([sentences[closest[idx]] for idx in ordering])

      post.summary = summary
      post.has_summary = True
      post.save()
  except:
    post.has_summary = True
    post.save()
    return 'fail post ' + post.id

def get_paragraph(url):
  try:
    content = get_page_content(url)[1]
    for blockquote in content.find_all('blockquote'):
      blockquote.decompose()
    content = content.find_all('article', attrs={'class':'post-content'})[0].find_all('p')
    content[0] = content[0].get_text()
    return reduce(lambda x, y: x + y.get_text(), content).replace('\n', '.')
  except:
    return 'fail: ' + url
