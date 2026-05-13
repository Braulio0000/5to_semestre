import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings; warnings.filterwarnings('ignore')

CLASS_NAMES = ['T-shirt','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Boot']
COLORS = plt.cm.tab10


np.random.seed(42)
X = np.vstack([np.random.randn(500,784)*12 + np.random.randn(784)*40 for _ in range(10)]).astype(np.float32)
y = np.repeat(np.arange(10), 500)
X_pca = PCA(50, random_state=42).fit_transform(MinMaxScaler().fit_transform(X))
X_2d  = PCA(2,  random_state=42).fit_transform(X_pca)

labels = KMeans(10, n_init=10, random_state=42).fit_predict(X_pca)
sil = silhouette_score(X_pca, labels, sample_size=1000, random_state=42)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Fashion-MNIST — PCA 2D', fontsize=13, fontweight='bold')
for i in range(10):
    axes[0].scatter(*X_2d[y==i].T,      c=[COLORS(i)], s=6, alpha=0.5, label=CLASS_NAMES[i])
    axes[1].scatter(*X_2d[labels==i].T, c=[COLORS(i)], s=6, alpha=0.5, label=f'Cluster {i}')
axes[0].set_title('Etiquetas reales');              axes[0].legend(markerscale=3, fontsize=7)
axes[1].set_title(f'KMeans k=10 (Sil={sil:.3f})'); axes[1].legend(markerscale=3, fontsize=7)
for ax in axes: ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('A_clusters.png', dpi=150, bbox_inches='tight')

table = np.zeros((10,10)); 
for kc,tc in zip(labels,y): table[kc,tc]+=1
table_n = table / table.sum(axis=1, keepdims=True) * 100
fig2, ax2 = plt.subplots(figsize=(12, 5))
im = ax2.imshow(table_n, cmap='YlOrRd', vmin=0, vmax=100)
plt.colorbar(im, ax=ax2, label='%')
ax2.set_xticks(range(10)); ax2.set_xticklabels(CLASS_NAMES, rotation=40, ha='right')
ax2.set_yticks(range(10)); ax2.set_yticklabels([f'Cluster {i}' for i in range(10)])
ax2.set_title('Composición de cada cluster KMeans (%)', fontweight='bold')
for i in range(10):
    for j in range(10):
        v=table_n[i,j]; ax2.text(j,i,f'{v:.0f}',ha='center',va='center',fontsize=7,color='w' if v>55 else 'k')
plt.tight_layout(); plt.savefig('B_heatmap.png', dpi=150, bbox_inches='tight')

main_c = np.argmax(np.bincount(labels)); mask = labels==main_c
sub_labels = KMeans(4, n_init=10, random_state=42).fit_predict(X_pca[mask])
fig3, axes3 = plt.subplots(1, 2, figsize=(12, 5))
fig3.suptitle(f'Sub-clusters — Cluster {main_c}', fontweight='bold')
for sc in range(4):
    axes3[0].scatter(*X_2d[mask][sub_labels==sc].T, c=[plt.cm.Set1(sc)], s=10, alpha=0.6, label=f'Sub {sc}')
for ci in np.unique(y[mask]):
    axes3[1].scatter(*X_2d[mask][y[mask]==ci].T, c=[COLORS(ci)], s=10, alpha=0.6, label=CLASS_NAMES[ci])
axes3[0].set_title('Sub-clusters (k=4)'); axes3[0].legend()
axes3[1].set_title('Clases reales');       axes3[1].legend(fontsize=8)
for ax in axes3: ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('C_subclusters.png', dpi=150, bbox_inches='tight')

plt.show()
print(f'Silhouette Score: {sil:.4f}')