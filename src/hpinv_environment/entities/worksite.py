from datetime import datetime

import pandas as pd
from .worksite_auxiliary import WorksiteAuxiliary

from hpinv_enums import WorksiteColumn


class Worksite:

    def __init__(self,
                 worksite_id: int,
                 parent_id: int,
                 active_status: str,
                 **additional_attributes):
        setattr(self, WorksiteColumn.WORKSITE_ID.value, int(worksite_id) if worksite_id and not pd.isna(worksite_id) else None)
        setattr(self, WorksiteColumn.ACTIVE_STATUS.value, active_status)
        setattr(self, WorksiteColumn.PARENT_WORKSITE_ID.value, int(parent_id) if parent_id and not pd.isna(parent_id) else None)

        for k, v in additional_attributes.items():
            setattr(self, k, v)

        self.provider_ids = set()

    def __hash__(self):
        return hash(getattr(self, WorksiteColumn.WORKSITE_ID.value))

    @property
    def worksite_id(self):
        return getattr(self, WorksiteColumn.WORKSITE_ID.value)

    @property
    def parent_id(self):
        return getattr(self, WorksiteColumn.PARENT_WORKSITE_ID.value)

