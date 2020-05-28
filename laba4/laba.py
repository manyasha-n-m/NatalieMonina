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
import rasterio

os.chdir('AwsData')
os.system('mkdir a b Kyiv')

images = {
    'a': 'S2A_MSIL2A_20190821T085601_N0213_R007_T36UUA_20190821T115206.SAFE/GRANULE/L2A_T36UUA_A021740_20190821T085815/IMG_DATA/R{}m/',
    'b': 'S2A_MSIL2A_20190821T085601_N0213_R007_T36UUB_20190821T115206.SAFE/GRANULE/L2A_T36UUB_A021740_20190821T085815/IMG_DATA/R{}m/'}
for n, i in images.items():
    bands = {}
    for z in [10, 20, 60]:
        bands[z] = {}
        ch = ['_B02_', '_B03_', '_B04_', '_B08_']
        for file in os.listdir(i.format(z)):
            for c in ch:
                if c in file:
                    os.system('echo '+file)
                    bands[z][c] = rasterio.open(i.format(z) + file, driver="JP2OpenJPEG")
                    break
        # merging
        merged = rasterio.open('{}/{}_{}.tiff'.format(n, n, z), 'w', driver='Gtiff',
                               width=bands[z]['_B02_'].width,
                               height=bands[z]['_B02_'].height,
                               count=4,
                               transform=bands[z]['_B02_'].transform,
                               dtype=bands[z]['_B02_'].dtypes[0])
        count = 0
        for c, b in bands[z].items():
            count += 1
            merged.write(b.read(1), count)
        merged.close()

        # reprojection
        gdal.Warp('{}/{}_{}_4326.tiff'.format(n, n, z),
                  '{}/{}_{}.tiff'.format(n, n, z),
                  dstSRS='EPSG:4326')

os.system('gdal_merge.py -o b/b.tiff -of Gtiff b/b*4326.tiff')
os.system('gdal_merge.py -o a/a.tiff -of Gtiff a/a*4326.tiff')

VRT = gdal.BuildVRT("Kyiv/Kyiv_obl.vrt", ["a/a.tiff", "b/b.tiff"])
gdal.Translate("Kyiv/Kyiv_obl.tiff", VRT)

os.system("gdalwarp -t_srs EPSG:4326 -q -cutline border/Kyiv_regions.shp -crop_to_cutline -of Gtiff Kyiv/Kyiv_obl.tiff Kyiv/Kyiv.tiff")
