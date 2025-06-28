# Imports
import ifcopenshell.util.element
import os
import json

# Put your directory and file name here
dirPath = "C:\\Users\\Gavin\\Downloads"
fileName = "Building-Architecture.ifc"

# Path of the Ifc file to read
filePath = os.path.join(dirPath, fileName)

# Open the model, get all IfcProducts
# Note that most elements inherit from IfcProduct
model = ifcopenshell.open(filePath)
all_elements = model.by_type("IfcProduct")

# List of dictionaries
elements_data = []

# For each element in Ifc model...
for e in all_elements:

    # New dictionary with Id, name, class and type
    element_data ={
        "GlobalId": e.GlobalId,
        "Name": e.Name,
        "IfcClass": e.is_a(),
        "ObjectType": e.ObjectType}

    # Get all property sets (psets) of element
    element_sets = ifcopenshell.util.element.get_psets(e)

    # For each set name and properties list...
    for set_name, properties in element_sets.items():

        # For each property and value...
        for prop_name, prop_value in properties.items():

            # Create a nested dictionary for the property
            element_data[set_name + "::" + prop_name] = {
                "PropertySetName": set_name,
                "PropertyName": prop_name,
                "Value": prop_value
            }

    # Append the dictionary
    elements_data.append(element_data)

# Path to write the data to
writePath = os.path.join(dirPath, "IfcDump.ndjson")

# With the file...
with open(writePath, "w") as f:

    # For each dictionary...
    for data in elements_data:

        # Convert to json, write the data
        json_data = json.dumps(data)
        f.write(json_data)
        f.write("\n")