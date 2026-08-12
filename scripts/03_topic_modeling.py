# -*- coding: utf-8 -*-
"""
Step 2: BERTopic topic modeling for both tracks with data-driven K selection.

Pipeline per track:
  1. Embed documents (all-MiniLM-L6-v2, the BERTopic default encoder).
  2. Reduce to 5 dims with UMAP (fixed seed).
  3. Scan K (KMeans on reduced embeddings); for each K compute NPMI topic
     coherence over the top-10 c-TF-IDF terms.
  4. Pick K* = argmax coherence, fit final BERTopic model with KMeans(K*),
     save topic table, document assignments, coherence curve.

KMeans is used instead of HDBSCAN so that (a) the number of topics is an
explicit, tunable parameter as described in the manuscript, and (b) every
document receives a topic (no outlier bin), which makes the dimension
shares in the Results section fully accountable.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
SEED = 42

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from umap import UMAP

PATENT_STOP = ["invention", "utility", "model", "discloses", "disclosed",
               "comprises", "comprising", "according", "present", "said",
               "plurality", "wherein", "provided", "provide", "provides",
               "method", "device", "apparatus", "system", "includes",
               "including", "used", "use", "using", "thereof", "belongs",
               "field", "technical", "technology", "solves", "problem",
               "effect", "realize", "realizes", "achieved", "achieve"]

YT_STOP = ["im", "dont", "thats", "its", "youre", "cant", "didnt", "doesnt",
           "gonna", "got", "just", "like", "really", "video", "videos",
           "lol", "xd", "wow", "omg", "quot", "39", "amp"]


def ctfidf_top_words(docs, labels, stop_words, top_n=10, min_df=5):
    """Class-based TF-IDF (Grootendorst 2022) top words per cluster."""
    vec = CountVectorizer(stop_words=stop_words, min_df=min_df,
                          token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b")
    X = vec.fit_transform(docs)
    terms = np.array(vec.get_feature_names_out())
    ks = sorted(set(labels))
    tf = np.vstack([np.asarray(X[np.array(labels) == k].sum(axis=0)).ravel()
                    for k in ks])
    tf_norm = tf / np.maximum(tf.sum(axis=1, keepdims=True), 1)
    avg_count = tf.sum() / max(len(ks), 1)
    idf = np.log(1 + avg_count / np.maximum(tf.sum(axis=0), 1))
    scores = tf_norm * idf
    tops = {k: terms[np.argsort(scores[i])[::-1][:top_n]].tolist()
            for i, k in enumerate(ks)}
    return tops, X, terms


def npmi_coherence(top_words, X_bin, terms):
    """Mean pairwise NPMI over each topic's top words (doc co-occurrence)."""
    idx = {t: i for i, t in enumerate(terms)}
    D = X_bin.shape[0]
    df_t = np.asarray(X_bin.sum(axis=0)).ravel()
    scores = []
    for words in top_words.values():
        ids = [idx[w] for w in words if w in idx]
        vals = []
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                i, j = ids[a], ids[b]
                co = X_bin[:, i].multiply(X_bin[:, j]).sum()
                if co == 0:
                    vals.append(-1.0)
                    continue
                p_ij = co / D
                pmi = np.log(p_ij / ((df_t[i] / D) * (df_t[j] / D)))
                vals.append(pmi / -np.log(p_ij))
        if vals:
            scores.append(np.mean(vals))
    return float(np.mean(scores)) if scores else np.nan


def run_track(name, docs, k_range, stop_words):
    print(f"\n===== Track {name}: {len(docs)} documents =====")
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    emb = encoder.encode(docs, show_progress_bar=False, batch_size=64)
    print("embeddings:", emb.shape)

    reducer = UMAP(n_components=5, n_neighbors=15, min_dist=0.0,
                   metric="cosine", random_state=SEED)
    red = reducer.fit_transform(emb)

    sw = list(CountVectorizer(stop_words="english").get_stop_words()) + stop_words
    vec_bin = CountVectorizer(stop_words=sw, min_df=5, binary=True,
                              token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b")
    X_bin = vec_bin.fit_transform(docs)
    bin_terms = np.array(vec_bin.get_feature_names_out())

    rows = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(red)
        tops, _, _ = ctfidf_top_words(docs, km.labels_, sw)
        coh = npmi_coherence(tops, X_bin, bin_terms)
        rows.append({"K": k, "coherence_npmi": coh})
        print(f"  K={k:2d}  NPMI={coh:.4f}")
    curve = pd.DataFrame(rows)
    k_star = int(curve.loc[curve["coherence_npmi"].idxmax(), "K"])
    print(f"selected K* = {k_star}")

    km = KMeans(n_clusters=k_star, random_state=SEED, n_init=10).fit(red)
    labels = km.labels_
    tops, X_full, terms = ctfidf_top_words(docs, labels, sw)

    topic_rows = []
    for k in sorted(set(labels)):
        n = int((labels == k).sum())
        topic_rows.append({"topic": k, "count": n,
                           "share": round(n / len(docs) * 100, 1),
                           "top_words": ", ".join(tops[k])})
    topics_df = pd.DataFrame(topic_rows).sort_values("count", ascending=False)

    curve.to_csv(OUT / "track{name}_coherence_curve.csv", index=False)
    topics_df.to_csv(OUT / "track{name}_topics_K{k_star}.csv",
                     index=False, encoding="utf-8-sig")
    np.save(OUT / "track{name}_embeddings.npy", emb)
    pd.DataFrame({"doc": docs, "topic": labels}).to_csv(
        OUT / "track{name}_doc_topics.csv", index=False, encoding="utf-8-sig")
    print(topics_df.to_string(index=False, max_colwidth=80))
    return k_star, labels, topics_df


patents = pd.read_csv(OUT / "patents_clean.csv")
youtube = pd.read_csv(OUT / "youtube_clean.csv")

# K floors (10 / 8) keep enough topic granularity for the subsequent
# topic-to-dimension mapping (several constituent topics per dimension);
# within each range K* is chosen by NPMI coherence.
kA, labA, topA = run_track("A", patents["abstract_en"].tolist(),
                           range(10, 31), PATENT_STOP)
kB, labB, topB = run_track("B", youtube["comment"].tolist(),
                           range(8, 21), YT_STOP)

json.dump({"track_A_K": kA, "track_B_K": kB},
          open(OUT / "k_selection.json", "w"))
print("\nDONE")
