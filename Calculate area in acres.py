import arcpy

Input_Data = arcpy.GetParameterAsText(0)
New_FieldName = arcpy.GetParameterAsText(1)
Field_DataType = arcpy.GetParameterAsText(2)
Output_FeatureClass = arcpy.GetParameterAsText(3)

#Add New Field
arcpy.AddField_management(Input_Data, New_FieldName,Field_DataType )


#get area in acres cursor
with arcpy.da.UpdateCursor(Input_Data, [New_FieldName]) as cursor:
    for row in cursor:
        arcpy.management.CalculateField(Input_Data, New_FieldName,"!Shape_Area!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
    arcpy.management.CalculateGeometryAttributes(Input_Data, [[New_FieldName, "AREA_GEODESIC"]], '', "ACRES", None, "SAME_AS_INPUT") 
            
arcpy.AddMessage("Calculate the area in Acres.")

