from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np


def word_clustering():
    # 1. Prepare Data (Corpus)
    # We create a small dummy corpus with two distinct topics:
    # Topic A: Computers/Tech
    # Topic B: Nature/Outdoors
    sentences = [
        ['computer', 'system', 'interface', 'user'],
        ['user', 'response', 'time', 'code'],
        ['computer', 'code', 'program', 'system'],
        ['interface', 'system', 'user', 'eps'],
        ['tree', 'forest', 'rain', 'grass'],
        ['grass', 'ground', 'tree', 'green'],
        ['rain', 'river', 'water', 'forest'],
        ['river', 'fish', 'water', 'swim']
    ]

    print("1. Training Word2Vec Model...")
    # vector_size=10: We create small 10-dimensional vectors (since data is small)
    # min_count=1: 
    # window=2: Context window size
    model = Word2Vec(sentences, vector_size=10, window=2, min_count=1, workers=4)

    # Extract vocabulary and vectors
    words = list(model.wv.index_to_key)
    word_vectors = model.wv[words]
    
    print(f"   Vocabulary Size: {len(words)}")
    print(f"   Vector Dimensions: {model.vector_size}")

    # 2. Clustering (K-Means)
    # We expect 2 clusters (Tech vs Nature)
    num_clusters = 2
    print(f"\n2. Clustering words into {num_clusters} groups using K-Means...")
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(word_vectors)
    clusters = kmeans.labels_

    # Print Cluster Results
    print("-" * 40)
    print(f"{'Word':<15} {'Cluster ID'}")
    print("-" * 40)
    for word, cluster in zip(words, clusters):
        print(f"{word:<15} {cluster}")

    # 3. Dimensionality Reduction (PCA)
    # Reduce 10 dimensions -> 2 dimensions for plotting
    print("\n3. Applying PCA for visualization...")
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(word_vectors)

    # 4. Plotting
    print("4. Generating Plot...")
    plt.figure(figsize=(10, 8))
    
    # Define colors for clusters (0 = Red, 1 = Blue)
    colors = ['red', 'blue']
    
    for i, word in enumerate(words):
        x, y = reduced_vectors[i]
        cluster_id = clusters[i]
        
        # Plot the point
        plt.scatter(x, y, c=colors[cluster_id], s=100, alpha=0.7, edgecolors='k')
        
        # Annotate the word slightly offset from the point
        plt.text(x + 0.02, y + 0.02, word, fontsize=12)

    plt.title('Word Clustering using Word2Vec & PCA')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Save the output for the LaTeX record
    plt.savefig('Q8OUTPUT.png')
    print("   Plot saved as 'Q8OUTPUT.png'")
    plt.show()

if __name__ == "__main__":
    word_clustering()