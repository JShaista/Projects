import arcpy

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")

    PUNKTSKY_1km_6181_724_las = "C:\\temp\\Shaista\\RasterPythonProject\\Building_Extraction\\Building_Extraction\\Tuborg_Havn_data\\LAS_data\\PUNKTSKY_1km_6181_724.las"
    PUNKTSKY_1km_6181_725_las = "C:\\temp\\Shaista\\RasterPythonProject\\Building_Extraction\\Building_Extraction\\Tuborg_Havn_data\\LAS_data\\PUNKTSKY_1km_6181_725.las"
    Punktsky_GroundPnts_DEM_3_ = arcpy.Raster("C:\\temp\\Shaista\\RasterPythonProject\\FinalProject_SJ\\FinalProject_SJ.gdb\\Punktsky_GroundPnts_DEM")

    # Process: Create LAS Dataset (Create LAS Dataset) (management)
    PUNKTSKY_lasd = "C:\\temp\\Shaista\\RasterPythonProject\\FinalProject_SJ\\Outputs\\PUNKTSKY.lasd"
    arcpy.management.CreateLasDataset(input=[PUNKTSKY_1km_6181_724_las, PUNKTSKY_1km_6181_725_las], out_las_dataset=PUNKTSKY_lasd, folder_recursion="NO_RECURSION", in_surface_constraints=[], spatial_reference="PROJCS[\"ETRS_1989_UTM_Zone_32N\",GEOGCS[\"GCS_ETRS_1989\",DATUM[\"D_ETRS_1989\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",9.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]],VERTCS[\"DVR90 height\",VDATUM[\"Dansk Vertikal Reference 1990\"],PARAMETER[\"Vertical_Shift\",0.0],PARAMETER[\"Direction\",1.0],UNIT[\"metre\",1.0]]", compute_stats="COMPUTE_STATS", relative_paths="RELATIVE_PATHS", create_las_prj="NO_FILES")
    print ('LAS dataset created')
    
    # Process: Classify LAS Ground (Classify LAS Ground) (3d)
    Output_LAS_Dataset = arcpy.ddd.ClassifyLasGround(in_las_dataset=PUNKTSKY_lasd, method="STANDARD", reuse_ground="RECLASSIFY_GROUND", dem_resolution="", compute_stats="COMPUTE_STATS", extent="DEFAULT", boundary="", process_entire_files="PROCESS_EXTENT", update_pyramid="UPDATE_PYRAMID")[0]
    print ('Classifying ground points')

    
    # Process: Make LAS Dataset Layer (Make LAS Dataset Layer) (management)
    PUNKTSKY_LasDatasetLayer = "PUNKTSKY_LasDatasetLayer"
    arcpy.management.MakeLasDatasetLayer(in_las_dataset=Output_LAS_Dataset, out_layer=PUNKTSKY_LasDatasetLayer, class_code=["2"], return_values=["Last Return", "Single Return", "First of Many", "Last of Many", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], no_flag="INCLUDE_UNFLAGGED", synthetic="INCLUDE_SYNTHETIC", keypoint="INCLUDE_KEYPOINT", withheld="EXCLUDE_WITHHELD", surface_constraints=[], overlap="INCLUDE_OVERLAP")
    print('Filtering ground points after classifying')


    # Process: LAS Dataset To Raster (LAS Dataset To Raster) (conversion)
    Punktsky_GroundPnts_DEM = "C:\\temp\\Shaista\\RasterPythonProject\\FinalProject_SJ\\FinalProject_SJ.gdb\\Punktsky_GroundPnts_DEM"
    arcpy.conversion.LasDatasetToRaster(in_las_dataset=PUNKTSKY_LasDatasetLayer, out_raster=Punktsky_GroundPnts_DEM, value_field="ELEVATION", interpolation_type="", data_type="FLOAT", sampling_type="CELLSIZE", sampling_value=0.5, z_factor=1)
    Punktsky_GroundPnts_DEM = arcpy.Raster(Punktsky_GroundPnts_DEM)
    print ('Raster created from the filter ground points')
    
    # Process: Classify LAS Noise (Classify LAS Noise) (3d)
    Output_Noise_Points = ""
    PUNKTSKY_lasd_2_ = arcpy.ddd.ClassifyLasNoise(in_las_dataset=PUNKTSKY_lasd, method="RELATIVE_HEIGHT", edit_las="CLASSIFY", withheld="NO_WITHHELD", compute_stats="COMPUTE_STATS", ground=Punktsky_GroundPnts_DEM, low_z="-2 Meters", high_z="", max_neighbors=10, step_width="8 Meters", step_height="8 Meters", extent="DEFAULT", process_entire_files="PROCESS_EXTENT", out_feature_class=Output_Noise_Points, update_pyramid="UPDATE_PYRAMID")[0]
    print('classfiying noise for points which are at -2 meters and less' )

    
    # Process: Classify LAS Noise (2) (Classify LAS Noise) (3d)
    Output_Noise_Points_2_ = ""
    PUNKTSKYNremove_lasd = arcpy.ddd.ClassifyLasNoise(in_las_dataset=PUNKTSKY_lasd, method="ABSOLUTE_HEIGHT", edit_las="CLASSIFY", withheld="NO_WITHHELD", compute_stats="COMPUTE_STATS", ground="", low_z="", high_z="42 Meters", max_neighbors=10, step_width="8 Meters", step_height="8 Meters", extent="DEFAULT", process_entire_files="PROCESS_EXTENT", out_feature_class=Output_Noise_Points_2_, update_pyramid="UPDATE_PYRAMID")[0]
    print ('classifying noise for points which are at 42 meter and above')


    # Process: Make LAS Dataset Layer (2) (Make LAS Dataset Layer) (management)
    PUNKTSKY_LASD_HighLowNoise = "PUNKTSKY_LASD_HighLowNoise"
    arcpy.management.MakeLasDatasetLayer(in_las_dataset=PUNKTSKY_lasd, out_layer=PUNKTSKY_LASD_HighLowNoise, class_code=["1"], return_values=["Last Return", "Single Return", "First of Many", "Last of Many", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], no_flag="INCLUDE_UNFLAGGED", synthetic="INCLUDE_SYNTHETIC", keypoint="INCLUDE_KEYPOINT", withheld="EXCLUDE_WITHHELD", surface_constraints=[], overlap="INCLUDE_OVERLAP")
    print('Selecting unclassfied points for building classification')


    # Process: Classify LAS Building (Classify LAS Building) (3d)
    PUNKTSKY_LASD_HighLowNoise_2_ = arcpy.ddd.ClassifyLasBuilding(in_las_dataset=PUNKTSKY_LASD_HighLowNoise, min_height="2 Meters", min_area="10 SquareMeters", compute_stats="COMPUTE_STATS", extent="DEFAULT", boundary="", process_entire_files="PROCESS_EXTENT", point_spacing="", reuse_building="RECLASSIFY_BUILDING", photogrammetric_data="NOT_PHOTOGRAMMETRIC_DATA", method="AGGRESSIVE", classify_above_roof="NO_CLASSIFY_ABOVE_ROOF", above_roof_height="", above_roof_code=None, classify_below_roof="NO_CLASSIFY_BELOW_ROOF", below_roof_code=None, update_pyramid="UPDATE_PYRAMID")[0]
    print('Classifying lidar unassigned points for building data which has minimum height of 2 m and minimum area of 10 sq meters')


    # Process: Make LAS Dataset Layer (3) (Make LAS Dataset Layer) (management)
    PUNKTSKY_LASD_Buildings = "PUNKTSKY_LASD_Buildings"
    arcpy.management.MakeLasDatasetLayer(in_las_dataset=PUNKTSKY_LASD_HighLowNoise_2_, out_layer=PUNKTSKY_LASD_Buildings, class_code=["6"], return_values=["Last Return", "Single Return", "First of Many", "Last of Many", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], no_flag="INCLUDE_UNFLAGGED", synthetic="INCLUDE_SYNTHETIC", keypoint="INCLUDE_KEYPOINT", withheld="EXCLUDE_WITHHELD", surface_constraints=[], overlap="INCLUDE_OVERLAP")
    print('Classifying lidar unassigned points for building data which has minimum height of 2 m and minimum area of 10 sq meters')

    # Process: LAS Point Statistics As Raster (LAS Point Statistics As Raster) (management)
    Building_Raster = "C:\\temp\\Shaista\\RasterPythonProject\\FinalProject_SJ\\finalproject_sj.gdb\\Building_Raster"
    arcpy.management.LasPointStatsAsRaster(in_las_dataset=PUNKTSKY_LASD_Buildings, out_raster=Building_Raster, method="PREDOMINANT_CLASS", sampling_type="CELLSIZE", sampling_value=0.5)
    Building_Raster = arcpy.Raster(Building_Raster)
    print('Generating raster corresponding to the location of the LAS building points ')

    # Process: Raster to Polygon (Raster to Polygon) (conversion)
    Rstr2Poly_BuldingRaw = "C:\\temp\\Shaista\\RasterPythonProject\\FinalProject_SJ\\FinalProject_SJ.gdb\\Rstr2Poly_BuldingRaw"
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(in_raster=Building_Raster, out_polygon_features=Rstr2Poly_BuldingRaw, simplify="NO_SIMPLIFY", raster_field="Value", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)
    print('Converted raster to polygon')

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    Rstr2Poly_BuldingRaw_Layer, Count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Rstr2Poly_BuldingRaw, selection_type="NEW_SELECTION", where_clause="Shape_Area >= 70", invert_where_clause="")
    print('Selecting attribute and removing smaller polygins which are too small to correspond to buidling')

    # Process: Eliminate Polygon Part (Eliminate Polygon Part) (management)
    Rstr2Poly_BuldingRaw_Lyr_Clean = "C:\\temp\\Shaista\\RasterPythonProject\\FinalProject_SJ\\FinalProject_SJ.gdb\\Rstr2Poly_BuldingRaw_Lyr_Clean"
    arcpy.management.EliminatePolygonPart(in_features=Rstr2Poly_BuldingRaw_Layer, out_feature_class=Rstr2Poly_BuldingRaw_Lyr_Clean, condition="AREA", part_area="50 SquareMeters", part_area_percent=0, part_option="CONTAINED_ONLY")
    print('Eliminating polygons which has gap/holes i.e. more than 50 square meters')

    # Process: Regularize Building Footprint (Regularize Building Footprint) (3d)
    bldg_clean_footprint = "C:\\temp\\Shaista\\RasterPythonProject\\FinalProject_SJ\\FinalProject_SJ.gdb\\bldg_clean_footprint"
    arcpy.ddd.RegularizeBuildingFootprint(in_features=Rstr2Poly_BuldingRaw_Lyr_Clean, out_feature_class=bldg_clean_footprint, method="RIGHT_ANGLES", tolerance=1, densification=1, precision=0.15, diagonal_penalty=1.5, min_radius=0.1, max_radius=1000000, alignment_feature="", alignment_tolerance="", tolerance_type="DISTANCE")
    print('Regularizing building footprint which will help in cleaning up the jagged borders')

    # Process: LAS Building Multipatch (2) (LAS Building Multipatch) (3d)
    Multipatch3d_Building_3_ = "C:\\temp\\Shaista\\RasterPythonProject\\FinalProject_SJ\\FinalProject_SJ.gdb\\Multipatch3d_Building"
    arcpy.ddd.LasBuildingMultipatch(in_las_dataset=PUNKTSKY_LASD_Buildings, in_features=bldg_clean_footprint, ground=Punktsky_GroundPnts_DEM_3_, out_feature_class=Multipatch3d_Building_3_, point_selection="BUILDING_CLASSIFIED_POINTS", simplification="0.5 Meters")
    print('Create buildings multipatch file')
    
if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\temp\Shaista\RasterPythonProject\FinalProject_SJ\FinalProject_SJ.gdb", workspace=r"C:\temp\Shaista\RasterPythonProject\FinalProject_SJ\FinalProject_SJ.gdb"):
        modelbackup()
