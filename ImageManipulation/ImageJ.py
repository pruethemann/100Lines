from PIL import Image
import numpy as np
import torch
import matplotlib.pyplot as plt
from numba.typed import List
from numba import njit
from timeit import default_timer as timer




def testset_generator():
	im = Image.open('lines.jpg')
	im_grey = im.convert('L')  # convert the image to *greyscale*
	im_array = np.array(im_grey)
	# pl.imshow(im_array, cmap=cm.Greys_r)
	# pl.show()
	im = torch.Tensor(im_array)
	label = torch.Tensor([6])
	testset = (im, label)
	return im_array

def horicontal(im):
    nrow, ncol = im.shape
    print(nrow, ncol)

    T = np.zeros((nrow,ncol))
    for n in range(nrow):
        T[n][ncol-n-1] = 1

    return T @ im

@njit
def filter(im, kernel, stride = 1):
	nrow, ncol = im.shape

	im_filter = np.zeros((nrow-2,ncol-2))

	for r in range(0,nrow-2,stride):
		for c in range(0,ncol-2,stride):
			x = im[r:r+3,c:c+3]
			im_filter[r][c] = np.sum(x * kernel)

	return im_filter


# edge detection
kernel1 = np.zeros((3,3))
kernel1[0][0] = 5
kernel1[2][2] = 5
kernel1[0][2] = -5
kernel1[2][0] = -5

# vertical lines
kernel2 = np.zeros((3,3))
kernel2[0][0] = 1
kernel2[1][0] = 1
kernel2[2][0] = 1

kernel2[0][2] = -1
kernel2[1][2] = -1
kernel2[2][2] = -1

# horicontal lines
kernel3 = np.zeros((3,3))
kernel3[0][0] = 1
kernel3[0][1] = 1
kernel3[0][2] = 1
kernel3[2][0] = -1
kernel3[2][1] = 1
kernel3[2][2] = -1



im = testset_generator()

plt.subplot(2, 2, 1)
plt.imshow(im.squeeze(), cmap='gray')
plt.axis('off')


test = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[5,6,7,8]])
stride = 1
start = timer()
k1 = filter(im, kernel1, stride)
k2 = filter(im, kernel2,stride)
k3 = filter(im, kernel3, stride)

print(timer()-start)

plt.subplot(2, 2, 2)
plt.imshow(k1, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(k2, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(k3, cmap='gray')
plt.axis('off')

plt.show()