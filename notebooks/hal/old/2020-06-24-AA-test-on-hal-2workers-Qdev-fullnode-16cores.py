import zarr
import xarray as xr
import time
import dask

ask_workers=2
memory='60GB'
from dask_jobqueue import PBSCluster
from dask.distributed import Client
import dask.dataframe as dd

cluster = PBSCluster(cores=1, memory=memory, project='PerfTestPangeo', walltime='04:00:00')
cluster.scale(ask_workers)

c = Client(cluster)

c

from dask.utils import ensure_dict, format_bytes
    
wk = c.scheduler_info()["workers"]

text="Workers= " + str(len(wk))
memory = [w["memory_limit"] for w in wk.values()]
if all(memory):
    text += ", Memory=" + format_bytes(sum(memory))
print(text)
#Workers= 2, 2 cores,Memory=120.00 GB
%time ds=xr.open_zarr('/work/ALT/odatis/eNATL60/zarr/eNATL60-BLBT02-SSH-1h')
#Wall time: 124 ms
%time mean=ds.sossheig.mean(dim='time_counter')
#Wall time: 379 ms
%time mean.load()
#Wall time: 45min 19s
c.close()
cluster.close()
