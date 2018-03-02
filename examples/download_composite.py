import openeo
import logging

#enable logging in requests library
logging.basicConfig(level=logging.DEBUG)

#connect with EURAC backend
session = openeo.session("nobody", "http://saocompute.eurac.edu/openEO_WCPS_Driver")

#create image collection
s2_fapar = session.imagecollection("S2_L2A_T32TPS_20M")

#specify process graph
job = s2_fapar \
    .date_range_filter("2016-01-01","2016-03-10") \
    .bbox_filter(left=652000,right=672000,top=5161000,bottom=5181000,srs="EPSG:32632") \
    .max_time() \
    .send_job()

#download result
job.download("/tmp/openeo-wcps.geotiff","netcdf")