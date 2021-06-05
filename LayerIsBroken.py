# Created by: MHagarGIS
# For: GEOG499
# For use in ArcGIS Pro.

# Create variable that points to current map document
mxd = arcpy.mapping.MapDocument("CURRENT")
# Create a variable to hold count of broken layers
broken = 0

# Create a list of all layers in current map document
layerlist = arcpy.mapping.ListLayers(mxd)

for lyr in layerlist:                                          # Step through each layer in list
    if lyr.isBroken:                                           # If the isBroken boolean returns true
        broken += 1                                            # Add 1 to broken count
    else:
        broken = broken                                        # Do nothing to count
print "There are",broken,"broken layers in this map document." # Print number of broken layers


