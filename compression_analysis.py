import matplotlib.pyplot as plt
import lzma
import gzip
import bz2
import os
import time

DATA_PATH = "./data"

files = [file_name for file_name in os.listdir(DATA_PATH) if file_name.endswith(".txt")]
files = sorted(files, key=lambda x: int(x[:-4]))
filesizes = [int(os.path.getsize(os.path.join(DATA_PATH, filename))/1024) for filename in files]

# Compression times for each algorithm
lzma_comprtimes = []
gzip_comprtimes = []
bz2_comprtimes = []

# Decompression times for each algorithm
lzma_decomprtimes = []
gzip_decomprtimes = []
bz2_decomprtimes = []

# Compression ratios for each algorithm
lzma_ratio = []
gzip_ratio = []
bz2_ratio = []

for filename in files:
    with open(os.path.join(DATA_PATH, filename), 'rb') as f:
        data = f.read()

    # LZMA compression
    lzma_start = time.time()
    lzma_compressed_data = lzma.compress(data)
    lzma_comprtimes.append(time.time() - lzma_start)

    # LZMA decompression
    lzma_start = time.time()
    lzma_decompressed_data = lzma.decompress(lzma_compressed_data)
    lzma_decomprtimes.append(time.time() - lzma_start)

    # Gzip compression
    gzip_start = time.time()
    gzip_compressed_data = gzip.compress(data)
    gzip_comprtimes.append(time.time() - gzip_start)

    # Gzip decompression
    gzip_start = time.time()
    gzip_decompressed_data = gzip.decompress(gzip_compressed_data)
    gzip_decomprtimes.append(time.time() - gzip_start)

    # Bzip2 compression
    bz2_start = time.time()
    bz2_compressed_data = bz2.compress(data)
    bz2_comprtimes.append(time.time() - bz2_start)

    # Bzip2 decompression
    bz2_start = time.time()
    bz2_decompressed_data = bz2.decompress(bz2_compressed_data)
    bz2_decomprtimes.append(time.time() - bz2_start)

    # Compression ratios
    lzma_ratio.append((len(data) - len(lzma_compressed_data))/len(data) * 100)
    gzip_ratio.append((len(data) - len(gzip_compressed_data))/len(data) * 100)
    bz2_ratio.append((len(data) - len(bz2_compressed_data))/len(data) * 100)

# Plotting compression times
plt.figure(figsize=(10, 6))
plt.plot(filesizes, lzma_comprtimes, label='LZMA')
plt.plot(filesizes, gzip_comprtimes, label='Gzip')
plt.plot(filesizes, bz2_comprtimes, label='Bzip2')
plt.xlabel('File Size (KB)')
plt.ylabel('Compression Time (s)')
plt.title('Compression Time vs File Size')
plt.legend()
plt.grid(True)
plt.savefig("compr")
# plt.show()

# Plotting decompression times
plt.figure(figsize=(10, 6))
plt.plot(filesizes, lzma_decomprtimes, label='LZMA')
plt.plot(filesizes, gzip_decomprtimes, label='Gzip')
plt.plot(filesizes, bz2_decomprtimes, label='Bzip2')
plt.xlabel('File Size (KB)')
plt.ylabel('Decompression Time (s)')
plt.title('Decompression Time vs File Size')
plt.legend()
plt.grid(True)
plt.savefig("decompr")
# plt.show()

# Plotting compression ratios
plt.figure(figsize=(10, 6))
plt.plot(filesizes, lzma_ratio, label='LZMA')
plt.plot(filesizes, gzip_ratio, label='Gzip')
plt.plot(filesizes, bz2_ratio, label='Bzip2')
plt.xlabel('File Size (KB)')
plt.ylabel('Compression Ratio (%)')
plt.title('Compression Ratio vs File Size')
plt.legend()
plt.grid(True)
plt.savefig("ratio")
# plt.show()
