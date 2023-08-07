import os
from typing import Any, Dict, Optional, Tuple

import xarray as xr

from . import sentinel1


class Sentinel1Backend(xr.backends.common.BackendEntrypoint):
    def open_dataset(  # type: ignore
        self,
        filename_or_obj: str,
        drop_variables: Optional[Tuple[str]] = None,
        group: Optional[str] = None,
        storage_options: Optional[Dict[str, Any]] = None,
        override_product_files: Optional[str] = None,
    ) -> xr.Dataset:
        ds = sentinel1.open_sentinel1_dataset(
            filename_or_obj,
            drop_variables=drop_variables,
            group=group,
            storage_options=storage_options,
            override_product_files=override_product_files,
        )
        return ds

    def guess_can_open(self, filename_or_obj: Any) -> bool:
        try:
            _, ext = os.path.splitext(filename_or_obj)
        except TypeError:
            return False
        return ext.lower() in {".safe", ".safe/"}
