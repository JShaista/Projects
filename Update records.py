                
                     
                     
import arcpy
airports_fc = r"C:\Assignments\world_airports.gdb\Airports"

arcpy.AddField_management(airports_fc, "flood_risk", "TEXT" field_length=10)

with arcpy.da.UpdateCursor(airport_fc, ["flood_risk", 'shape@Z']) as cursor:
     for row in cursor:
          elevation=row[1]
          if elevation > 50:
               row[0]="Safe"
          else:
               row[0]= "At Risk"
          cursor.updaterow[row]

print("All Done")
                    
