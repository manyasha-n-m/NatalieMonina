# from sentinelhub import SHConfig,AwsProductRequest
# INSTANCE_ID = 'fe2e93c1-1e9f-4e35-a8ac-093837c4f343'
#
# if INSTANCE_ID:
#     config = SHConfig()
#     config.instance_id = INSTANCE_ID
# else:
#     config = None
#
# product_id = ['S2A_MSIL2A_20190821T085601_N0213_R007_T36UUA_20190821T115206','S2A_MSIL2A_20190821T085601_N0213_R007_T36UUB_20190821T115206']
# data_folder = './AwsData'
# for product in product_id:
#      product_request = AwsProductRequest(product_id=product,
#                                      data_folder=data_folder, safe_format=True)
#      product_request.save_data()

import os
import glob
import gdal

gdal.UseExceptions()

os.chdir('AwsData')
os.system('mkdir a b Kyiv')

images = {
    'a': 'S2A_MSIL2A_20190821T085601_N0213_R007_T36UUA_20190821T115206.SAFE/GRANULE/L2A_T36UUA_A021740_20190821T085815/IMG_DATA/R{}m/',
    'b': 'S2A_MSIL2A_20190821T085601_N0213_R007_T36UUB_20190821T115206.SAFE/GRANULE/L2A_T36UUB_A021740_20190821T085815/IMG_DATA/R{}m/'}
for n, i in images.items():
    bands = {}
    for z in [10, 20, 60]:
        bands[z] = []
        ch = ['_B02_', '_B03_', '_B04_', '_B08_']
        a = i.format(z)
        if z==10:
            os.system("gdal_merge.py -o {}/{}_{}.tiff -separate -of Gtiff {}*_B02*.jp2 {}*_B03*.jp2 {}*_B04*.jp2 {}*_B08*.jp2".format(n,n,z,a,a,a,a))
        else:
            os.system("gdal_merge.py -o {}/{}_{}.tiff -separate -of Gtiff {}*_B02*.jp2 {}*_B03*.jp2 {}*_B04*.jp2".format(n,n,z,a,a,a))

VRT = gdal.BuildVRT("Kyiv/Kyiv_obl.vrt", ["a/a_10.tiff", "b/b_10.tiff"])
gdal.Translate("Kyiv/Kyiv_obl.tiff", VRT)

gdal.Warp('Kyiv/Kyiv_obl_4326.tiff',
          'Kyiv/Kyiv_obl.tiff',
          dstSRS='EPSG:4326')

gdal.Warp('Kyiv/Kyiv.tiff', 'Kyiv/Kyiv_obl_4326.tiff', cutlineDSName='border/Kyiv_regions.shp', cropToCutline=True)
