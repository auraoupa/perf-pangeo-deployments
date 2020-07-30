#!/usr/bin/env python

# ## The imports

import zarr
import xarray as xr
import time
import dask


# # The workers
nb_workers=8
from dask.distributed import Client, LocalCluster
cluster = LocalCluster(n_workers=nb_workers)
c = Client(cluster)

c

from dask.utils import ensure_dict, format_bytes
    
wk = c.scheduler_info()["workers"]

text="Workers= " + str(len(wk))
memory = [w["memory_limit"] for w in wk.values()]
cores = sum(w["nthreads"] for w in wk.values())
text += ", Cores=" + str(cores)
if all(memory):
    text += ", Memory=" + format_bytes(sum(memory))
print(text)


# # The data

%time ds=xr.open_zarr('/mnt/alberta/equipes/IGE/meom/workdir/albert/eNATL60/zarr/eNATL60-BLBT02-SSH-1h')
mean=ds.sossheig.mean(dim='time_counter')
%time mean.load()

cluster.close()
