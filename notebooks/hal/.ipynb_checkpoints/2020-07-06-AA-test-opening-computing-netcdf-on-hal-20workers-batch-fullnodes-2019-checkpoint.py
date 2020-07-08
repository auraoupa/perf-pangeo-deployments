import zarr
import xarray as xr
import time
import dask
import glob

ask_workers=20
memory='180GB'

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

files=sorted(glob.glob('/work/ALT/odatis/eNATL60/BLBT02/gridT-2D/eNATL60*gridT-2D*.nc'))
drop_vars = ['nav_lat', 'nav_lon', 'somxl010', 'sosaline', 'sosstsst']
extra_coord_vars = []
chunks = dict(time_counter=240, y=240, x=480)
open_kwargs = dict(drop_variables=(drop_vars + extra_coord_vars),
                   chunks=chunks,decode_cf=True,decode_times=False,
                   concat_dim="time_counter",combine='nested')

%time ds = xr.open_mfdataset(files, parallel=True, **open_kwargs)

%time mean=ds.sossheig.mean(dim='time_counter')

%time mean.load()

cluster.close()