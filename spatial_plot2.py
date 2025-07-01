import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap

# --- User-defined paths ---
shapefile_path = r"C:\Users\91913\Downloads\Warangal"  # folder containing .shp, .shx, .dbf
excel_path = r"C:\Users\91913\Downloads\output_file.xlsx"
raster_paths = {
    1995: r"C:\Users\91913\Downloads\Warangal_LULC_1995.tif",
    2005: r"C:\Users\91913\Downloads\Warangal_LULC_2005.tif",
    2015: r"C:\Users\91913\Downloads\Warangal_LULC_2015.tif",
    2022: r"C:\Users\91913\Downloads\Warangal_LULC_2022.tif",
}

# --- Load shapefile ---
gdf = gpd.read_file(shapefile_path)

# --- Load ESV values from Excel ---
df = pd.read_excel(excel_path, sheet_name="Output_1", index_col=0)
column_sum = df.loc["column sum"].drop("row sum", errors="ignore")

# --- LULC to Class Mapping ---
lulc_classes = {
    0: "Vegetation",
    1: "Cropland",
    2: "Builtup",
    3: "Water",
    4: "Barren Land"
}
esv_mapping = {code: round(column_sum.get(name, 0), 3) for code, name in lulc_classes.items()}

# --- ESV Ranges and Color Setup ---
ranges = [20, 40, 60, 80, 100, 200, 1500]
labels = ['20–40', '40–60', '60-80', '80-100', '100-200', '200-1500']
colors = ['#d1d110', "#3384da", '#0fbdb4', "#17be49", "#DF58E1", "#E36217"]
cmap = ListedColormap(colors)

# --- Set up subplot layout ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='white')
axes = axes.flatten()

# --- Loop through years and plot ---
for i, (year, path) in enumerate(raster_paths.items()):
    with rasterio.open(path) as src:
        if gdf.crs != src.crs:
            gdf = gdf.to_crs(src.crs)

        # Clip raster to district shape
        masked_image, masked_transform = mask(src, gdf.geometry, crop=True, nodata=-9999)
        lulc_masked = masked_image[0]
        lulc_masked = np.where(lulc_masked == -9999, np.nan, lulc_masked)

        # Create ESV raster
        esv_raster = np.full_like(lulc_masked, np.nan, dtype=np.float32)
        for code, esv_val in esv_mapping.items():
            esv_raster[lulc_masked == code] = esv_val

        # Classify to ESV range
        classified = np.digitize(esv_raster, bins=ranges, right=False).astype(float)
        classified[np.isnan(esv_raster)] = np.nan
        
        # Get extent
        height, width = lulc_masked.shape
        x_min = masked_transform[2]
        y_max = masked_transform[5]
        x_max = x_min + masked_transform[0] * width
        y_min = y_max + masked_transform[4] * height
        extent = [x_min, x_max, y_min, y_max]

        # Plotting
        ax = axes[i]
        im = ax.imshow(classified, cmap=cmap, extent=extent, vmin=1, vmax=len(ranges))
        ax.set_title(f"ESV - {year}", fontsize=14)
        ax.axis('off')
        ax.set_facecolor('white')

# --- Shared legend ---
legend_elements = [
    Patch(facecolor=colors[i], edgecolor='black', label=f"{labels[i]} USD/ha/year")
    for i in range(len(labels))
]

fig.legend(
    handles=legend_elements,
    title="ESV Ranges",
    loc='center right',
    bbox_to_anchor=(1.01, 0.5),
    frameon=True,
    fontsize=10,
    title_fontsize=11
)

plt.tight_layout()
plt.subplots_adjust(right=0.85)
output_path = r"C:\Users\91913\Downloads\ESV_MultiYear_Warangal.png"  # or .tiff, .pdf, etc.
plt.savefig(output_path, dpi=1200, bbox_inches='tight', pad_inches=0.1, transparent=False)

