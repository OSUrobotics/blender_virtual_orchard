import matplotlib.pyplot as plt
import numpy as np
import cv2
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
for i in range(1,10):
    nemo = cv2.imread('/Users/abhinav/Desktop/blender/noiseconcat0(0, 0, 0)/labelled.avi000{}.png'.format(i))
    nemo = cv2.cvtColor(nemo, cv2.COLOR_BGR2RGB)
    colors = np.unique(nemo.reshape(-1, nemo.shape[2]), axis=0)
    print(len(colors))
    # r, g, b = cv2.split(nemo)
    # fig = plt.figure()
    # axis = fig.add_subplot(1, 1, 1, projection="3d")
    # pixel_colors = nemo.reshape((np.shape(nemo)[0]*np.shape(nemo)[1], 3))
    # norm = colors.Normalize(vmin=-1.,vmax=1.)
    # norm.autoscale(pixel_colors)
    # pixel_colors = norm(pixel_colors).tolist()
    # axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
    # axis.set_xlabel("Red")
    # axis.set_ylabel("Green")
    # axis.set_zlabel("Blue")
    # plt.show()
    # plt.imshow(nemo)
    # plt.show()