import zarr
import xarray as xr
import time
import dask

ask_workers=8
memory='4GB'
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
cores = sum(w["nthreads"] for w in wk.values())
text += ", Cores=" + str(cores)
if all(memory):
    text += ", Memory=" + format_bytes(sum(memory))
print(text)
#Workers= 8, Cores=8, Memory=32.00 GB

%time ds=xr.open_zarr('/work/ALT/odatis/eNATL60/zarr/eNATL60-BLBT02-SSH-1h')
#41.6 ms
%time mean=ds.sossheig.mean(dim='time_counter')
#209 ms
%time mean.load()

c.close()
cluster.close()
