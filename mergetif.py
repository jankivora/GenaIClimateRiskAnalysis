# Import packages
import glob
import numpy as np
import rasterio
from rasterio.merge import merge

# Make a list of input GeoTIFF files to be referenced
input_files = glob.glob('Desktop/geotiff/*.tif')

# Open input datasets and read the data arrays
src_datasets = [rasterio.open(file) for file in input_files]
data_arrays = [src.read(1) for src in src_datasets]  # Read the first band (band indexing is 1-based)

# Merge datasets to get georeferencing information
merged, out_transform = merge(src_datasets)

# Update metadata for the merged dataset
out_meta = src_datasets[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "count": len(data_arrays),  # Number of bands
    "height": merged.shape[1],
    "width": merged.shape[2],
    "transform": out_transform
})

# Save the combined data to a new GeoTIFF file
with rasterio.open("Desktop/geotiff/output.tif", "w", **out_meta) as dest:
    for band_num, data in enumerate(data_arrays, start=1):
        dest.write(data, band_num)

# Close the input datasets
for src_dataset in src_datasets:
    src_dataset.close()

