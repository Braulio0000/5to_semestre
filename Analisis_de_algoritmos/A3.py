import pandas as pd
import numpy as np
import umap
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, RadioButtons
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

base_path = os.path.dirname(os.path.abspath(__file__))
archivo = os.path.join(base_path, 'fashion-mnist_test.csv')

nombres = ['Camiseta', 'Pantalón', 'Suéter', 'Vestido', 'Abrigo',
           'Sandalia', 'Camisa', 'Tenis', 'Bolsa', 'Bota de tobillo']

class UMAPSubclusterApp:
    def __init__(self):
        self.embedding = None
        self.y = None
        self.X = None
        self.selected_cluster = None
        self.n_subclusters = 3
        self.sub_embedding = None
        self.sub_labels = None
        self.fig = None
        self.ax_main = None
        self.ax_sub = None

    def cargar_y_calcular(self):
        print("Cargando datos...")
        df = pd.read_csv(archivo)
        self.X = df.drop('label', axis=1).values
        self.y = df['label'].values
        self.X = self.X / 255.0
        print(f" Datos cargados: {self.X.shape[0]} imágenes.")

        print("Calculando UMAP global... (esto puede tardar unos segundos)")
        reductor = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
        self.embedding = reductor.fit_transform(self.X)
        print(" UMAP global completado.")

    def graficar_principal(self):
        self.ax_main.clear()
        scatter = self.ax_main.scatter(
            self.embedding[:, 0], self.embedding[:, 1],
            c=self.y, cmap='Spectral', s=5, alpha=0.7
        )
        # Resaltar cluster seleccionado
        if self.selected_cluster is not None:
            mask = self.y == self.selected_cluster
            self.ax_main.scatter(
                self.embedding[mask, 0], self.embedding[mask, 1],
                s=10, alpha=0.9, color='black', zorder=3, label='Seleccionado'
            )
            self.ax_main.set_title(
                f"UMAP Global — Cluster seleccionado: {nombres[self.selected_cluster]}",
                fontsize=12, fontweight='bold'
            )
        else:
            self.ax_main.set_title("UMAP Global — Selecciona un cluster", fontsize=12)

        self.ax_main.set_xlabel("UMAP Dimensión 1")
        self.ax_main.set_ylabel("UMAP Dimensión 2")
        self.ax_main.set_facecolor('#f5f5f5')

        # Leyenda
        patches = [mpatches.Patch(color=plt.cm.Spectral(i / 9), label=nombres[i]) for i in range(10)]
        self.ax_main.legend(handles=patches, loc='upper right', fontsize=7, ncol=2,
                            title="Categorías", framealpha=0.9)

    def calcular_subcluster(self):
        if self.selected_cluster is None:
            return

        mask = self.y == self.selected_cluster
        X_sub = self.X[mask]

        print(f"\nCalculando UMAP para subcluster: {nombres[self.selected_cluster]} ({X_sub.shape[0]} puntos)...")
        reductor_sub = umap.UMAP(n_neighbors=10, min_dist=0.05, random_state=42)
        self.sub_embedding = reductor_sub.fit_transform(X_sub)

        print(f"Aplicando KMeans con {self.n_subclusters} subclusters...")
        kmeans = KMeans(n_clusters=self.n_subclusters, random_state=42, n_init=10)
        self.sub_labels = kmeans.fit_predict(X_sub)
        print("✅ Subclustering completado.")

    def graficar_subcluster(self):
        self.ax_sub.clear()
        if self.sub_embedding is None or self.selected_cluster is None:
            self.ax_sub.text(0.5, 0.5, 'Selecciona un cluster\ny presiona Calcular',
                             ha='center', va='center', fontsize=12, color='gray',
                             transform=self.ax_sub.transAxes)
            self.ax_sub.set_facecolor('#fafafa')
            self.ax_sub.set_title("Sub-UMAP del Cluster Seleccionado", fontsize=12)
            return

        colores_sub = plt.cm.tab10(np.linspace(0, 1, self.n_subclusters))
        for i in range(self.n_subclusters):
            idx = self.sub_labels == i
            self.ax_sub.scatter(
                self.sub_embedding[idx, 0], self.sub_embedding[idx, 1],
                color=colores_sub[i], s=8, alpha=0.8, label=f'Subcluster {i+1}'
            )

        self.ax_sub.set_title(
            f"Sub-UMAP: {nombres[self.selected_cluster]} → {self.n_subclusters} subclusters",
            fontsize=12, fontweight='bold'
        )
        self.ax_sub.set_xlabel("Sub-UMAP Dimensión 1")
        self.ax_sub.set_ylabel("Sub-UMAP Dimensión 2")
        self.ax_sub.set_facecolor('#f5f5f5')
        self.ax_sub.legend(loc='upper right', fontsize=8)

        # Estadísticas por subcluster
        for i in range(self.n_subclusters):
            conteo = np.sum(self.sub_labels == i)
            cx = np.mean(self.sub_embedding[self.sub_labels == i, 0])
            cy = np.mean(self.sub_embedding[self.sub_labels == i, 1])
            self.ax_sub.annotate(f'n={conteo}', (cx, cy), fontsize=7,
                                 ha='center', va='center',
                                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))

    def ejecutar(self):
        self.cargar_y_calcular()

        self.fig = plt.figure(figsize=(18, 8))
        self.fig.suptitle("Fashion-MNIST — UMAP Interactivo con Subclusters", fontsize=14, fontweight='bold')

        # Diseño: gráfico principal | subgráfico | controles
        gs = self.fig.add_gridspec(1, 3, width_ratios=[5, 5, 2], wspace=0.35)
        self.ax_main = self.fig.add_subplot(gs[0])
        self.ax_sub = self.fig.add_subplot(gs[1])
        ax_ctrl = self.fig.add_subplot(gs[2])
        ax_ctrl.axis('off')

        self.graficar_principal()
        self.graficar_subcluster()

        # --- Botones de radio para seleccionar cluster ---
        ax_radio = self.fig.add_axes([0.72, 0.35, 0.25, 0.45])
        radio = RadioButtons(ax_radio, nombres, activecolor='steelblue')
        ax_radio.set_title("Seleccionar\nCluster", fontsize=10, fontweight='bold', pad=8)

        # --- Radio para número de subclusters ---
        ax_nsub = self.fig.add_axes([0.72, 0.18, 0.25, 0.15])
        radio_nsub = RadioButtons(ax_nsub, ['2', '3', '4', '5'], active=1, activecolor='coral')
        ax_nsub.set_title("Nº Subclusters", fontsize=9, fontweight='bold', pad=6)

        # --- Botón para calcular ---
        ax_btn = self.fig.add_axes([0.74, 0.08, 0.20, 0.07])
        btn = Button(ax_btn, ' Calcular\nSubcluster', color='steelblue', hovercolor='navy')
        btn.label.set_color('white')
        btn.label.set_fontsize(10)
        btn.label.set_fontweight('bold')

        def al_seleccionar_cluster(etiqueta):
            self.selected_cluster = nombres.index(etiqueta)
            self.sub_embedding = None
            self.sub_labels = None
            self.graficar_principal()
            self.graficar_subcluster()
            self.fig.canvas.draw_idle()

        def al_cambiar_subclusters(etiqueta):
            self.n_subclusters = int(etiqueta)

        def al_hacer_clic(event):
            if self.selected_cluster is None:
                print("Selecciona un cluster primero.")
                return
            self.calcular_subcluster()
            self.graficar_principal()
            self.graficar_subcluster()
            self.fig.canvas.draw_idle()

        radio.on_clicked(al_seleccionar_cluster)
        radio_nsub.on_clicked(al_cambiar_subclusters)
        btn.on_clicked(al_hacer_clic)

        print("\n Interfaz lista:")
        print("  1. Selecciona un cluster en el panel derecho")
        print("  2. Elige el número de subclusters")
        print("  3. Haz clic en ' Calcular Subcluster'")

        plt.show()


if __name__ == "__main__":
    app = UMAPSubclusterApp()
    app.ejecutar()
