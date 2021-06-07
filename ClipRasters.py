# By: MHagarGIS
# For: GIS470 
#
# Some functionality beyond assignment requirements was added to show more proficiency in Python/ArcPy.
# This script not only clips rasters but excludes subfolders from the arcpy.da.Walk() and will remove
# old rasters with the same name input by the user and replace them with new raster outputs.

#Import the arcpy module
import arcpy
#Import the current environment from arcpy
from arcpy import env
#os needed for operating system functionality
import os

#ask user for workspace location
env.workspace = arcpy.GetParameterAsText(0)

#ask user for clipping polygon location
cFeature = arcpy.GetParameterAsText(1)

#ask user for output location
outLocation = arcpy.GetParameterAsText(2)

#ask user to name output featureclass
name = arcpy.GetParameterAsText(3)

#ask user if they want to replace pre-existing raster(s) with same name
#this will be evaluated as a boolean  e.g. if there is text in the box
replaceold = arcpy.GetParameterAsText(4)

#reverse split to generate folder name to exclude from walk
#this split works from the right side of the string and is
#delimited by a \ which must be escaped by another \ because
#it is a special character
exclude = outLocation.rsplit("\\",1)[1]

#you'll need an empty list to hold the rasters and filenames
rasters = []
fnames = [] #probably a good idea to not use "filenames" here to avoid confusion in the following da.Walk

#you should also create a list containing restricted characters and the word "con" to check the raster names against
nRestrictions = ['con', '\\', ',', '~', "'", '"', '(', ')', '{', '}', '[', ']']
    
## strange though the following code may look, don't change this part -- it should work
walk = arcpy.da.Walk(env.workspace, datatype="RasterDataset")   #arcpy.da.Walk generates a list that returns the three variables below
                                                                #by using the arcpy data access module (da) and the Walk command
for dirpath, dirnames, filenames in walk:                       #dirpath is the path to the workspace as a string, dirnames is a list of names of subdirectories and other workspaces in dirpath                                                          #filenames is a list of names of nonworkspace contents in dirpath
    if exclude in dirnames:                                     #here the name of the subfolder is excluded from the walk to prevent
        dirnames.remove(exclude)                                #redundancy when generating new rasters down in the for "raster in rasters"
    arcpy.AddMessage(dirnames)
    for filename in filenames:                                  #create filename variable and loop through all the files found in filenames
        rasters.append(os.path.join(dirpath, filename))         #reconstruct the full path name for each file found in list
        fnames.append(filename)                                 #directory and filenames are listed seperately so os.path.join joins them together
                                                                #the Walk seeks out RasterDataset files and the joined directory is appended to rasters[]
        
#print out the list of rasters and filenames found in the directory paths
#likely a good idea just to show the user what is happening with the script
arcpy.AddMessage("Raster(s) location:")
arcpy.AddMessage(rasters)
arcpy.AddMessage("Name of raster(s) located:")
arcpy.AddMessage(fnames)
arcpy.AddMessage("Clipping feature:")
arcpy.AddMessage(cFeature)

#test for name restrictions within filename list
for f in fnames:
    for nr in nRestrictions:
        if nr in f:
            raise NameError('Special character ' + nr + 'found in ' + f + 'filename.')
        else:
            continue

#if there was no name error tell the user and continue
arcpy.AddMessage('No special characters found in raster filename(s). Continue...')
            
#check the user provided name for length so that it will work with all formats
#namely the ESRI grid which has short name limitations
if len(name) > 9:
    raise NameError('Output raster filename exceeds 9 character length limit.')

#tell the user their raster name of choice is within limits and continue script
arcpy.AddMessage('Raster filename(s) within maximum length limit. Continue...')

#reusing old code from prior implementation to handle naming scheme etc....
#time to fix up the naming scheme
fixedfn = []    #create a list to store the fixed final names for output
count = 0       #create a counter to keep track of file number

#this loop will go through all filenames and generate a list of proper final file names to be added to the outFolder
for f in fnames:    #loop through all filenames
    arcpy.AddMessage(f)
    fixedfn.append(outLocation + '\\' + name + str(count) + '.tif') #append the fixed file names to fixedfn[] list
    count += 1                                                      #increase the counter

#print of the fixedFn list to make sure these fixed filnames look correct
arcpy.AddMessage(fixedfn)
count = 0   #reset count for later use

#print out the fixedfn[] list to make sure these fixed filepaths and filenames look right 
arcpy.AddMessage(fixedfn)

for raster in rasters:
#fix file name problem before we get to clip_management
#require a new base filename structure that maxes out at 9 characters
#max file name is 9 characters max full path is 128 characters
    if not('dem' in raster):
        currentout = fixedfn[count]
        if replaceold == "true":    #if user selected to delete old rasters with same name then delete rasters
            arcpy.AddMessage(replaceold)
            if arcpy.Exists(currentout):
                arcpy.AddMessage("Deleting old raster(s)...")
                arcpy.Delete_management(currentout)

        arcpy.management.Clip(raster, "#", currentout, cFeature, "0", "ClippingGeometry")
        arcpy.AddMessage(currentout)
        arcpy.AddMessage(raster)
        count += 1

#print a message just to show script ran without crashing
arcpy.AddMessage("Finished without crashing.")
