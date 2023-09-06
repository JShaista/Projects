import arcpy
import os

#To allow overwriting Output
arcpy.env.overwriteOutput = True

#Input Parameters
Input_Data = arcpy.GetParameterAsText(0)
Magnitude_field = arcpy.GetParameterAsText(1)

#Define workspace
arcpy.env.workspace = os.path.dirname(Input_Data)


#Make a copy of the Input Feature class
Input_Data_copy = os.path.join(os.path.dirname(Input_Data),"Input_Data_copy")
arcpy.CopyFeatures_management(Input_Data, Input_Data_copy)



#Add two New Fields for descriptive class and for average kms felt.
Class = "Desc_Class"
Dist = "Felt_Dist"
arcpy.AddField_management(Input_Data_copy, Class, "TEXT", field_alias="Descriptive Class")
arcpy.AddField_management(Input_Data_copy, Dist, "TEXT", field_alias="Distance Felt in km")
arcpy.AddMessage("Added Descriptice Class and Distance felt fields to the input data")

#Create function to categorize the magnitude of an earthquake into a descriptive class.
def Descriptive_Class(mag):
    if mag < 3.0: return "Micro"
    elif mag >= 3.0 and mag < 4.0: return "Minor"
    elif mag >= 4.0 and mag < 5.0: return "Light"
    elif mag >= 5.0 and mag < 6.0: return "Moderate"
    elif mag >= 6.0 and mag < 7.0: return "Strong"
    elif mag >= 7.0 and mag < 8.0: return "Major"
    elif mag >= 8.0: return "Great"
    

# Create function that returns the distance felt from the magnitude of an earthquake.
def Distance_Felt(mag):
    if mag < 3.0: return "5 Kilometers"
    elif mag >= 3.0 and mag < 4.0: return "25 Kilometers"
    elif mag >= 4.0 and mag < 5.0: return "75 Kilometers"
    elif mag >= 5.0 and mag < 6.0: return "125 Kilometers"
    elif mag >= 6.0 and mag < 7.0: return "250 Kilometers"
    elif mag >= 7.0 and mag < 8.0: return "400 Kilometers"
    elif mag >= 8.0: return "750 Kilometers"
    
#Create an update cursor to update the descriptive class and distance felt field.
cursor = arcpy.da.UpdateCursor(Input_Data,[Magnitude_field,Class,Dist])
arcpy.AddMessage("Created an Update Cursor")  

#Loop through each line and update the descriptive class and distance felt field.
for row in cursor:
    if row[0] == None: continue                     # This deals with Null values in the magnitude field.
    row[1] = Descriptive_Class(row[0])              # This asigns a value to the descriptive class field
    row[2] = Distance_Felt(row[0])                  # This assigns a value to the distance felt field
    cursor.updateRow(row)
arcpy.AddMessage("Descriptive class and distance felt fields updated.")


#Create Buffers as per the distance felt Field
Output_BufferFC = arcpy.GetParameterAsText(2)
arcpy.Buffer_analysis(Input_Data_copy, Output_BufferFC, 'Distance Felt in km', method = "GEODESIC")
arcpy.AddMessage("Buffer has been created")

#Create an output Statistics table
Summary_stats_tab = arcpy.GetParameterAsText(3)
arcpy.analysis.Statistics(Input_Data_copy,Summary_stats_tab, [['Magnitude_field', 'MEAN']])
arcpy.AddMessage("Statistics calculated")

#Final Tool completion message
arcpy.AddMessage("Tool executed successfully")
