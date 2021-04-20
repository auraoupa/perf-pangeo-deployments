#!/usr/bin/env python

# # The imports
import xarray as xr
import time
import dask


# # The workers
ask_workers=4
from dask_jobqueue import SLURMCluster 
from dask.distributed import Client 
cluster = SLURMCluster(cores=1,processes=1,name='pangeo',walltime='02:30:00',
                       job_extra=['--constraint=HSW24','--exclusive',
                                  '--nodes=1'],memory='120GB',
                       interface='ib0') 
cluster.scale(ask_workers)
c= Client(cluster)
c

from dask.utils import ensure_dict, format_bytes
wk = c.scheduler_info()["workers"]
text="Workers= " + str(len(wk))
memory = [w["memory_limit"] for w in wk.values()]
if all(memory):
    text += ", Memory=" + format_bytes(sum(memory))
print(text)

# # The data
%time ds=xr.open_zarr('/store/albert7a/eNATL60/zarr/eNATL60-BLBT02-SSH-1h')
#=> 1.79s
%time mean=ds.sossheig.mean(dim='time_counter')
#=> 1.82s
%time mean.load()
#=> 28min31s
cluster.close()




