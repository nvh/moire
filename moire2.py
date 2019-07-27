"""
Simple moire with two gratings encoding two color images
"""
import moirelib as m
import sys

T = 1./40  # grating period as fraction of image width
offset = 1./8  # offset as a fraction of the image height

input1 = sys.argv[1] if len(sys.argv) > 1 else 'audrey'
input2 = sys.argv[2] if len(sys.argv) > 2 else 'mona'

print 'Loading images...'
img = (
    m.prepImage(input1, mag=1, sigma=(0, T/4, 0)),
    m.prepImage(input2, mag=1, sigma=(0, T/4, 0))
)
fig = m.figure(figsize=(8, 10))
m.show(img[0], 321, 'original')
m.show(img[1], 322, 'original')
m.saveImage(img[0], 'original1')
m.saveImage(img[1], 'original2')

print 'generating gratings...'
offset = round(offset*img[0].shape[0])  # convert to pixels
dims = img[0].shape
dims = (dims[0]+offset, dims[1], dims[2])
g1 = m.makeCarrier(dims, T)
g2 = g1.copy()

# iterative adjustment of gratings to images
L = 0.04       # learning rate
niter = 501    # of iterations

for i in range(niter):
    if i % 25 == 0:
        print "iteration [%4d/%4d]" % (i, niter)

    # update gratings
    err1 = (1-img[0])/2 - (g1[:-offset, :, :] - g2[offset:, :, :])
    err2 = (1-img[1])/2 - (g2[:-offset, :, :] - g1[offset:, :, :])
    g1[:-offset, :, :] += L*err1
    g2[offset:, :, :] -= L*err1
    g2[:-offset, :, :] += L*err2
    g1[offset:, :, :] -= L*err2

    # enforce grating smoothness by clipping the laplacian
    g1 = m.smoothenPhase(g1, 1e-4/T)

print 'saving image...'
g1 = m.makeGrating(g1)
g2 = m.makeGrating(g2)

# visualize gratings
m.saveImage(g1, 'grating1')
m.saveImage(g2, 'grating2')
m.show(g1, 323, 'grating 1')
m.show(g2, 324, 'grating 2')

# visualize superpositions
e = m.ones((offset, dims[1], dims[2]))
s1 = m.vstack((e, g1))*m.vstack((g2, e))
s2 = m.vstack((e, g2))*m.vstack((g1, e))
m.saveImage(s1, 'superposition1')
m.saveImage(s2, 'superposition2')

m.show(s1, 325, 'superposition 1')
m.show(s2, 326, 'superposition 2')

fig.savefig('./results/moire2.png', dpi=300)
