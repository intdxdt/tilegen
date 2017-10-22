import math
from common import MAXZOOMLEVEL

class GlobalGeodetic(object):
    """
    TMS Global Geodetic Profile
    ---------------------------

    Functions necessary for generation of global tiles in Plate Carre projection,
    EPSG:4326, "unprojected profile".

    Such tiles are compatible with Google Earth (as any other EPSG:4326 rasters)
    and you can overlay the tiles on top of OpenLayers base map.

    Pixel and tile coordinates are in TMS notation (origin [0,0] in bottom-left).

    What coordinate conversions do we need for TMS Global Geodetic tiles?

      Global Geodetic tiles are using geodetic coordinates (latitude,longitude)
      directly as planar coordinates XY (it is also called Unprojected or Plate
      Carre). We need only scaling to pixel pyramid and cutting to tiles.
      Pyramid has on top level two tiles, so it is not square but rectangle.
      Area [-180,-90,180,90] is scaled to 512x256 pixels.
      TMS has coordinate origin (for pixels and tiles) in bottom-left corner.
      Rasters are in EPSG:4326 and therefore are compatible with Google Earth.

         LatLon      <->      Pixels      <->     Tiles

     WGS84 coordinates   Pixels in pyramid  Tiles in pyramid
         lat/lon         XY pixels Z zoom      XYZ from TMS
        EPSG:4326
         .----.                ----
        /      \     <->    /--------/    <->      TMS
        \      /         /--------------/
         -----        /--------------------/
       WMS, KML    Web Clients, Google Earth  TileMapService
    """
    def __init__(self, tileSize=256):
        self.tileSize = tileSize

    def LatLonToPixels(self, lat, lon, zoom):
        """Converts lat/lon to pixel coordinates in given zoom of the EPSG:4326 pyramid"""
        res = 180.0 / self.tileSize / 2 ** zoom
        px = (180 + lat) / res
        py = (90 + lon) / res
        return px, py

    def PixelsToTile(self, px, py):
        """Returns coordinates of the tile covering region in pixel coordinates"""
        tx = int(math.ceil(px / float(self.tileSize)) - 1)
        ty = int(math.ceil(py / float(self.tileSize)) - 1)
        return tx, ty

    def LatLonToTile(self, lat, lon, zoom):
        """Returns the tile for zoom which covers given lat/lon coordinates"""
        px, py = self.LatLonToPixels(lat, lon, zoom)
        return self.PixelsToTile(px, py)

    def Resolution(self, zoom):
        """Resolution (arc/pixel) for given zoom level (measured at Equator)"""
        return 180.0 / self.tileSize / 2 ** zoom
        # return 180 / float( 1 << (8+zoom) )

    def ZoomForPixelSize(self, pixelSize):
        """Maximal scaledown zoom of the pyramid closest to the pixelSize."""
        for i in range(MAXZOOMLEVEL):
            if pixelSize > self.Resolution(i):
                if i != 0:
                    return i - 1
                else:
                    return 0  # We don't want to scale up

    def TileBounds(self, tx, ty, zoom):
        """Returns bounds of the given tile"""
        res = 180.0 / self.tileSize / 2 ** zoom
        return (
            tx * self.tileSize * res - 180,
            ty * self.tileSize * res - 90,
            (tx + 1) * self.tileSize * res - 180,
            (ty + 1) * self.tileSize * res - 90
        )

    def TileLatLonBounds(self, tx, ty, zoom):
        """Returns bounds of the given tile in the SWNE form"""
        b = self.TileBounds(tx, ty, zoom)
        return b[1], b[0], b[3], b[2]
