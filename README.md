# 🌍 Ecosystem Service Value (ESV) Assessment Using Remote Sensing & Python

This project focuses on assessing **Ecosystem Service Values (ESVs)** using remote sensing data and satellite imagery. 
It involves preprocessing of spatial data, performing ESV calculations based on land use/land cover (LULC) data, and visualizing the results using spatial plots.

---

## 📌 Project Overview

- **Objective**: To quantify and visualize the changes in ESVs across different years using LULC raster datasets.
- **Tools Used**: Python, Remote Sensing techniques, GIS data, Excel, Raster processing libraries.
- **Output**: ESV values per LULC category saved to Excel and spatial plots representing ESV distribution.

---

## 🧠 Key Features

- 📡 Satellite image and LULC raster (.tif) file handling
- 🧮 Automated ESV value computation using standard coefficients
- 📊 Export of results to Excel (.xlsx)
- 🗺️ Generation of spatial maps for ESV visualization
- ⌛ Multi-temporal analysis for years like 1995, 2005, 2015, 2022

---

## 🛠️ Tech Stack

- **Language**: Python
- **Libraries**:
  - `rasterio` for reading satellite data
  - `numpy` and `pandas` for data manipulation
  - `matplotlib`, `geopandas`, `seaborn` for plotting
  - `openpyxl` or `xlsxwriter` for Excel export

---

## 🧾 Data Input

- LULC raster files: e.g., `LULC_1995.tif`, `LULC_2005.tif`, ...
- Coefficient table: ESV coefficients for each land class
- Output: ESV per LULC class saved as an Excel sheet and spatial ESV maps

