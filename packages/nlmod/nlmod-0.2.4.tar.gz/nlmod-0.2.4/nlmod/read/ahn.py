# -*- coding: utf-8 -*-
"""Created on Fri Jun 12 15:33:03 2020.

@author: ruben
"""

import datetime as dt
import logging
import tempfile

import numpy as np
import xarray as xr
from owslib.wcs import WebCoverageService
from rasterio import merge
from rasterio.io import MemoryFile
import rioxarray

from .. import cache, mdims, util

logger = logging.getLogger(__name__)


@cache.cache_netcdf
def get_ahn(model_ds, identifier="ahn3_5m_dtm"):
    """Get a model dataset with ahn variable.

    Parameters
    ----------
    model_ds : xr.Dataset
        dataset with the model information.
    identifier : str, optional
        Possible values for identifier are:
            'ahn2_05m_int'
            'ahn2_05m_non'
            'ahn2_05m_ruw'
            'ahn2_5m'
            'ahn3_05m_dsm'
            'ahn3_05m_dtm'
            'ahn3_5m_dsm'
            'ahn3_5m_dtm'

        The default is 'ahn3_5m_dtm'.

    Returns
    -------
    model_ds_out : xr.Dataset
        dataset with the ahn variable.
    """

    url = _infer_url(identifier)

    ahn_ds_raw = get_ahn_within_extent(
        extent=model_ds.extent, url=url, identifier=identifier
    )

    ahn_ds_raw = rioxarray.open_rasterio(ahn_ds_raw.open())
    ahn_ds_raw = ahn_ds_raw.rename({"band": "layer"})
    ahn_ds_raw = ahn_ds_raw.where(ahn_ds_raw != ahn_ds_raw.attrs["_FillValue"])

    if model_ds.gridtype == "structured":
        ahn_ds = mdims.resample_dataarray3d_to_structured_grid(
            ahn_ds_raw,
            extent=model_ds.extent,
            delr=model_ds.delr,
            delc=model_ds.delc,
            x=model_ds.x.data,
            y=model_ds.y.data,
        )
    elif model_ds.gridtype == "vertex":
        ahn_ds = mdims.resample_dataarray3d_to_vertex_grid(ahn_ds_raw, model_ds)

    model_ds_out = util.get_model_ds_empty(model_ds)
    model_ds_out["ahn"] = ahn_ds[0]

    for datavar in model_ds_out:
        model_ds_out[datavar].attrs["source"] = identifier
        model_ds_out[datavar].attrs["url"] = url
        model_ds_out[datavar].attrs["date"] = dt.datetime.now().strftime("%Y%m%d")
        if datavar == "ahn":
            model_ds_out[datavar].attrs["units"] = "mNAP"

    return model_ds_out


def split_ahn_extent(
    extent, res, x_segments, y_segments, maxsize, tmp_dir=None, **kwargs
):
    """There is a max height and width limit of 800 * res for the wcs server.
    This function splits your extent in chunks smaller than the limit. It
    returns a list of gdal Datasets.

    Parameters
    ----------
    extent : list, tuple or np.array
        extent
    res : float
        The resolution of the requested output-data
    x_segments : int
        number of tiles on the x axis
    y_segments : int
        number of tiles on the y axis
    maxsize : int or float
        maximum widht or height of ahn tile
    tmp_dir : str, optional
        Path-like to cache the downloads
    **kwargs :
        keyword arguments of the get_ahn_extent function.

    Returns
    -------
    MemoryFile
        Rasterio MemoryFile of the merged AHN

    Notes
    -----
    1. The resolution is used to obtain the ahn from the wcs server. Not sure
    what kind of interpolation is used to resample the original grid.
    """

    # needs a temporary folder to store the individual ahn tiffs before merge
    with tempfile.TemporaryDirectory() as tempfile_tmp_dir:
        if tmp_dir is None:
            logger.info(
                f"- Created temporary directory {tempfile_tmp_dir}. "
                "To store ahn tiffs of subextents"
            )
            tmp_dir_path = tempfile_tmp_dir
        else:
            logger.info(f"- Use {tmp_dir} to store ahn tiffs of subextents")
            tmp_dir_path = tmp_dir

        # write tiles
        datasets = []
        start_x = extent[0]
        for tx in range(x_segments):
            if (tx + 1) == x_segments:
                end_x = extent[1]
            else:
                end_x = start_x + maxsize * res
            start_y = extent[2]
            for ty in range(y_segments):
                if (ty + 1) == y_segments:
                    end_y = extent[3]
                else:
                    end_y = start_y + maxsize * res
                subextent = [start_x, end_x, start_y, end_y]
                logger.info(f"downloading subextent {subextent}")
                logger.info(f"x_segment-{tx}, y_segment-{ty}")

                datasets.append(
                    get_ahn_within_extent(
                        subextent, res=res, tmp_dir=tmp_dir_path, **kwargs
                    )
                )
                start_y = end_y

            start_x = end_x

        memfile = MemoryFile()
        merge.merge([b.open() for b in datasets], dst_path=memfile)

    return memfile


def _infer_url(identifier=None):
    """infer the url from the identifier.

    Parameters
    ----------
    identifier : TYPE, optional
        DESCRIPTION. The default is None.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    url : TYPE
        DESCRIPTION.
    """

    # infer url from identifier
    if "ahn2" in identifier:
        url = (
            "https://geodata.nationaalgeoregister.nl/ahn2/wcs?"
            "request=GetCapabilities&service=WCS"
        )
    elif "ahn3" in identifier:
        url = (
            "https://geodata.nationaalgeoregister.nl/ahn3/wcs?"
            "request=GetCapabilities&service=WCS"
        )
    else:
        ValueError(f"unknown identifier -> {identifier}")

    return url


def get_ahn_within_extent(
    extent=None,
    identifier="ahn3_5m_dtm",
    url=None,
    res=None,
    version="1.0.0",
    fmt="GEOTIFF_FLOAT32",
    crs="EPSG:28992",
    maxsize=800,
    tmp_dir=None,
):
    """

    Parameters
    ----------
    extent : list, tuple or np.array, optional
        extent. The default is None.
    identifier : str, optional
        Possible values for identifier are:
            'ahn2_05m_int'
            'ahn2_05m_non'
            'ahn2_05m_ruw'
            'ahn2_5m'
            'ahn3_05m_dsm'
            'ahn3_05m_dtm'
            'ahn3_5m_dsm'
            'ahn3_5m_dtm'

        The default is 'ahn3_5m_dtm'.

        the identifier also contains resolution and type info:
        - 5m or 05m is a resolution of 5x5 or 0.5x0.5 meter.
        - 'dtm' is only surface level (maaiveld), 'dsm' has other surfaces
        such as building.
    url : str or None, optional
        possible values None, 'ahn2' and 'ahn3'. If None the url is inferred
        from the identifier. The default is None.
    res : float, optional
        resolution of ahn raster. If None the resolution is inferred from the
        identifier. The default is None.
    version : str, optional
        version of wcs service, options are '1.0.0' and '2.0.1'.
        The default is '1.0.0'.
    fmt : str, optional
        geotif format . The default is 'GEOTIFF_FLOAT32'.
    crs : str, optional
        coördinate reference system. The default is 'EPSG:28992'.
    tmp_dir : str
        Path-like to temporairly store the downloads before merge.
    maxsize : float, optional
        maximum number of cells in x or y direction. The default is
        800.

    Returns
    -------
    MemoryFile
        Rasterio MemoryFile of the AHN

    """

    if isinstance(extent, xr.DataArray):
        extent = tuple(extent.values)

    # get url
    if url is None:
        url = _infer_url(identifier)
    elif url == "ahn2":
        url = (
            "https://geodata.nationaalgeoregister.nl/ahn2/wcs?"
            "request=GetCapabilities&service=WCS"
        )
    elif url == "ahn3":
        url = (
            "https://geodata.nationaalgeoregister.nl/ahn3/wcs?"
            "request=GetCapabilities&service=WCS"
        )
    elif not url.startswith("https://geodata.nationaalgeoregister.nl"):
        raise ValueError(f"unknown url -> {url}")

    # check resolution
    if res is None:
        if "05m" in identifier.split("_")[1]:
            res = 0.5
        elif "5m" in identifier.split("_")[1]:
            res = 5.0
        else:
            raise ValueError("could not infer resolution from identifier")

    # check if ahn is within limits
    dx = extent[1] - extent[0]
    dy = extent[3] - extent[2]

    # check if size exceeds maxsize
    if (dx / res) > maxsize:
        x_segments = int(np.ceil((dx / res) / maxsize))
    else:
        x_segments = 1

    if (dy / res) > maxsize:
        y_segments = int(np.ceil((dy / res) / maxsize))
    else:
        y_segments = 1

    if (x_segments * y_segments) > 1:
        st = f"""requested ahn raster width or height bigger than {maxsize*res}
            -> splitting extent into {x_segments} * {y_segments} tiles"""
        logger.info(st)
        return split_ahn_extent(
            extent,
            res,
            x_segments,
            y_segments,
            maxsize,
            identifier=identifier,
            version=version,
            fmt=fmt,
            crs=crs,
            tmp_dir=tmp_dir,
        )

    # download file
    logger.info(
        f"- download ahn between: x ({str(extent[0])}, {str(extent[1])}); "
        f"y ({str(extent[2])}, {str(extent[3])})"
    )
    wcs = WebCoverageService(url, version=version)
    if version == "1.0.0":
        bbox = (extent[0], extent[2], extent[1], extent[3])
        output = wcs.getCoverage(
            identifier=identifier, bbox=bbox, format=fmt, crs=crs, resx=res, resy=res
        )
    elif version == "2.0.1":
        # bbox, resx and resy do nothing in version 2.0.1
        subsets = [("x", extent[0], extent[1]), ("y", extent[2], extent[3])]
        output = wcs.getCoverage(
            identifier=[identifier], subsets=subsets, format=fmt, crs=crs
        )
    else:
        raise Exception(f"Version {version} not yet supported")

    return MemoryFile(output.read())
