import pandas as pd

import excelgdb

def main():
    # Geodatabase path
    gdb_path = r"Data\Ouput\example.gdb"
    # Function to check and add 'ORIG_FID' field if it does not exist

    # Function to read points from an Excel file and add them to the point layer
    def add_points_from_excel(layer, excel_file):
        df = pd.read_excel(excel_file,sheet_name="hospital")
        for _, row in df.iterrows():
            x, y = row['X'], row['Y']
            layer.add_point(x, y)

    # Function to read lines from an Excel file and add them to the line layer
    def add_lines_from_excel(layer, excel_file, sort_field):
        df = pd.read_excel(excel_file, sheet_name="railway")   
        # Grouping points by 'sort_field' column in the Excel file to create separate lines
        grouped = df.groupby(sort_field)   
        # Creating a dictionary to store coordinates grouped by `sort_field`
        coordinates_grouped = {}
        for name, group in grouped:
            # Extracting coordinates for the current line segment
            coordinates = [(row['X'], row['Y']) for _, row in group.iterrows()]
            coordinates_grouped[name] = coordinates  # Store coordinates with `sort_field` as the key

        # Adding grouped coordinates to the layer as lines
        layer.add_line_xls(coordinates_grouped)

    # Function to read polygons from an Excel file and add them to the polygon layer
    def add_polygons_from_excel(layer, excel_file,sort_field):
        df = pd.read_excel(excel_file, sheet_name="shahrestan")   
        # Grouping coordinates by 'sort_field' column if needed
        grouped = df.groupby(sort_field)   
        # Creating a dictionary to store coordinates grouped by `sort_field`
        coordinates_grouped = {}
        for name, group in grouped:
            # Extracting coordinates for the current polygon
            coordinates = [(row['X'], row['Y']) for _, row in group.iterrows()]
            coordinates_grouped[name] = coordinates  # Store coordinates with `sort_field` as the key

        # Adding grouped coordinates to the layer as polygons
        layer.add_polygon_xls(coordinates_grouped)

    # Creating layers & Reading data from Excel files and adding to layers
    point_layer = excelgdb.PointLayer(gdb_path, "Hospital")
    add_points_from_excel(point_layer, r"data\hospital.xlsx")

    line_layer = excelgdb.LineLayer(gdb_path, "Rails", "ORIG_FID")
    add_lines_from_excel(line_layer, r"data\railway.xlsx", "ORIG_FID")
    line_layer.delete_null_records()

    polygon_layer = excelgdb.PolygonLayer(gdb_path, "Shahrestan", "ORIG_FID")
    add_polygons_from_excel(polygon_layer, r"data\shahrestan.xlsx", "ORIG_FID")
    polygon_layer.delete_null_records()

if __name__ == "__main__":
     main()
