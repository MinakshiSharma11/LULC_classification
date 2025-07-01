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

# --- LULC class mapping ---
lulc_classes = {
    0: "Vegetation",
    1: "Cropland",
    2: "Builtup",
    3: "Water",
    4: "Barren Land"
}

# --- ESV Ranges and Color Setup ---
# Adjusted for finer visual distinction
ranges = [0, 30, 50, 80, 100, 200, 1500]
labels = ['0–30', '30–50', '50-80', '80-100', '100-200', '200-1500']
colors = ["#ece93d", "#eb3d1b", "#4ed933", "#e108c1", "#2466ca", "#5c0a3d"]
cmap = ListedColormap(colors)

# --- Load shapefile ---
gdf = gpd.read_file(shapefile_path)

# --- Set up subplot layout ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='white')
axes = axes.flatten()

# --- Loop through years ---
for i, (year, raster_path) in enumerate(raster_paths.items()):
    # Load ESV values for the year
    df = pd.read_excel(excel_path, sheet_name=f'Output_{i+1}', index_col=0)
    column_sum = df.loc["column sum"].drop("row sum", errors="ignore")
    esv_mapping = {code: round(column_sum.get(name, 0), 3) for code, name in lulc_classes.items()}

    # Read and clip raster
    with rasterio.open(raster_path) as src:
        if gdf.crs != src.crs:
            gdf = gdf.to_crs(src.crs)

        masked_image, masked_transform = mask(src, gdf.geometry, crop=True, nodata=-9999)
        lulc_masked = masked_image[0]
        lulc_masked = np.where(lulc_masked == -9999, np.nan, lulc_masked)

        # Create ESV raster for this year
        esv_raster = np.full_like(lulc_masked, np.nan, dtype=np.float32)
        for code, esv_val in esv_mapping.items():
            esv_raster[lulc_masked == code] = esv_val

        # Classify ESV into defined ranges
        classified = np.digitize(esv_raster, bins=ranges, right=False).astype(float) - 1
        classified[np.isnan(esv_raster)] = np.nan

        # Define extent for plotting
        height, width = lulc_masked.shape
        x_min = masked_transform[2]
        y_max = masked_transform[5]
        x_max = x_min + masked_transform[0] * width
        y_min = y_max + masked_transform[4] * height
        extent = [x_min, x_max, y_min, y_max]

        # Plot
        ax = axes[i]
        im = ax.imshow(classified, cmap=cmap, extent=extent, vmin=0, vmax=5)
        ax.set_title(f"(Ahmedabad) ESV - {year}", fontsize=14)
        ax.axis('off')
        ax.set_facecolor('white')

# --- Shared Legend ---
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

# --- Save the output image ---
output_path = r"C:\Users\91913\Downloads\ESV_MultiYear_Warangal.png"
plt.savefig(output_path, dpi=1200, bbox_inches='tight', pad_inches=0.1, transparent=False)
print("All outputs written successfully to:", output_path)





