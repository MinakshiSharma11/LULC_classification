import pandas as pd

def read_excel_matrix_and_constants(file_path):
    df = pd.read_excel(file_path, header=None)

    # Extract matrix: B2:F18 (rows 1:18, cols 1:6)
    matrix = df.iloc[1:18, 1:6].values.tolist()

    # Extract constants: B19:F22 (rows 18:22, cols 1:6)
    constants_list = df.iloc[19:23, 1:6].values.tolist()

    return matrix, constants_list

#def safe_float(val):
   # try:
       # return float(val)
   # except ValueError:
      #  return 0.0  # or raise error/log warning

def multiply_columns(matrix, constants):
    return [[(value) * (constants[i])/10000 for i, value in enumerate(row)] for row in matrix]


def calculate_sums(matrix):
    row_sums = [sum(row) for row in matrix]
    col_sums = [sum(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))]
    return row_sums, col_sums

def write_output_to_excel(all_results, row_labels, col_labels, output_path):
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for idx, (matrix, row_sums, col_sums) in enumerate(all_results, start=1):
            # Append row-wise totals
            for i in range(len(matrix)):
                matrix[i].append(row_sums[i])

            # Append column totals
            col_sums.append(None)
            matrix.append(col_sums)

            # Prepare labels
            full_row_labels = row_labels + ["column sum"]
            full_col_labels = col_labels + ["row sum"]

            df = pd.DataFrame(matrix, index=full_row_labels, columns=full_col_labels)

            sheet_name = f'Output_{idx}'
            df.to_excel(writer, sheet_name=sheet_name)

# -------- Main Program --------
input_path = r"C:\Users\91913\Downloads\input_data.xlsx"
output_path = r'C:\Users\91913\Downloads\output_file.xlsx'

# Fixed labels
row_labels = [
    'Gas', 'Climate', 'Disturbance', 'Water reg', 'Water supply', 'Erosion', 'Soil formation',
    'Nutrient', 'Waste', 'Pollination', 'Biological', 'Habitat', 'Food', 'Raw',
    'Genetic services', 'Recreation', 'Cultural'
]

col_labels = ['Vegetation', 'Cropland', 'Builtup','Water','Barren Land']

# Read and process
matrix, constants_list = read_excel_matrix_and_constants(input_path)

all_results = []
for constants in constants_list:
    result_matrix = multiply_columns(matrix, constants)
    row_sums, col_sums = calculate_sums(result_matrix)
    all_results.append((result_matrix, row_sums, col_sums))

write_output_to_excel(all_results, row_labels, col_labels, output_path)

print("All outputs written successfully to:", output_path)

