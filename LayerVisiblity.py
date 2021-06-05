# Created by: MHagarGIS
# For: GEOG499
# For use in ArcGIS Pro.

# Create a new variable that points to the current map document
mxd = arcpy.mapping.MapDocument("CURRENT")
# Create a list of all the layers contained in current map document
layerlist = arcpy.mapping.ListLayers(mxd)

for lyr in layerlist:            # Step through each layer in the list (layerlist)
    if lyr.isFeatureLayer:       # Check to see if layer is vector
        lyr.visible = True       # Set layer to visible
    else:
        lyr.visible = False      # If layer is raster set visiblity to false
arcpy.RefreshTOC()               # Refresh the table of contents to see changes
arcpy.RefreshActiveView()        # Refresh active view to see changes


