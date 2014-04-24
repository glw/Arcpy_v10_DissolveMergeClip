# Author: Garret Wais garretwais@cookcountyil.gov
# Name: dissolve_merge.py
# Description: dissolves and merges all polygons for specified shpfiles. Then clips them based on another shps selected boundary.

import arcpy, os

arcpy.env.workspace = "path/to/workspace"
arcpy.env.overwriteOutput=True
md = "shapefile1.shp"
hf = "shapefile2.shp"
fpd = "shapefile3.shp"
out = "path/to/output" #process output folder

try:
	#dissolve shapefile3.shp polygons
	dissfield_fpd = ["dissolve"] # variable
	outputfpd = os.path.join(out, "dissolved_fpd.shp") # variable
	
	arcpy.Dissolve_management(fpd, outputfpd, dissfield_fpd,  "", "MULTI_PART", "DISSOLVE_LINES")
	print "FPD Dissolve Done..."

#===================================================================================================

	#dissolve shapefile2.shp
	dissfield_hf = ["site_no"] #variable
	outputhf = os.path.join(out, "dissolved_hf.shp") # variable

	arcpy.Dissolve_management(hf, outputhf, dissfield_hf, "", "MULTI_PART", "DISSOLVE_LINES")
	print "HF Dissolve Done..."

#=====================================================================================================
	
	#merge dissolved shpfiles
	dhf = os.path.join(out, "dissolved_hf.shp") # variable
	dfpd = os.path.join(out, "dissolved_fpd.shp") # variable
	
	#Merge_management (inputs, output, {field_mappings})
	arcpy.Merge_management([dhf, dfpd], os.path.join(out, "merged_hffpd.shp"), "")
	print "Merge of HF and FPD Done..."

#=======================================================================================================
	
	#dissolve merged polygons again this is needed b/c they were split for some reason by the merge operation
	input = os.path.join(out, "merged_hffpd.shp") # variable
	dissfield_diss = ["dissolve"] # variable
	output = os.path.join(out, "dissolved_finalfpd_hf.shp") # variable

	arcpy.Dissolve_management(input, output, dissfield_diss, "", "MULTI_PART", "DISSOLVE_LINES")
	print "Re-Dissolve of polygons Done..."

#=========================================================================================================
	
	#clip polygons from selected area
	mfpd = os.path.join(out, "dissolved_finalfpd_hf.shp") # variable

	rows = arcpy.SearchCursor(md)
	count = 0 # variable
	for row in rows:
		outpoly = os.path.join(out, "outpoly" + str(count)) # variable
		arcpy.Clip_analysis(mfpd, row.Shape, outpoly)
		count = count + 1
		
	print "clip and merge complete..."
	
except:
	print "An error occured..."
	print (arcpy.GetMessages(0))
	
del row	
del rows
