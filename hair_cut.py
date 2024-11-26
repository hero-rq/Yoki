import numpy as np
import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

dimensions = 10
vertices = np.array(list(itertools.product([0, 1], repeat=dimensions)))

from sklearn.decomposition import PCA
pca = PCA(n_components=3)
projected_vertices = pca.fit_transform(vertices)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(projected_vertices[:, 0], projected_vertices[:, 1], projected_vertices[:, 2], alpha=0.6)

ax.set_title('3D Projection of a 10D Hypercube')
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')
plt.show()
