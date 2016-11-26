import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import mmap
import numpy as np
import posix_ipc
import struct

def main():
    a = posix_ipc.SharedMemory('/pixeldumper')
    mm = mmap.mmap(a.fd, (1 << 20) * 10)

    width = struct.unpack('@i', mm[0:4])[0]
    height = struct.unpack('@i', mm[4:8])[0]
    stride = struct.unpack('@i', mm[8:12])[0]
    total = abs(height * stride)
    array = np.fromstring(mm[13:13+total], dtype=np.uint8)
    array = np.reshape(array, (height, abs(stride/4), 4))

    fig = plt.figure()
    im = plt.imshow(array, animated=True)

    def update(*args):
        array = np.fromstring(mm[13:13+total], dtype=np.uint8)
        array = np.reshape(array, (height, abs(stride/4), 4))
        im.set_array(array)
        return im,
    ani = animation.FuncAnimation(fig, update, interval = 10, blit=False)
    plt.show()
