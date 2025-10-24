from datetime import datetime

import pandas as pd
from .worksite_auxiliary import WorksiteAuxiliary

from hpinv_enums import WorksiteColumn


class Worksite:

    def __init__(self,
                 worksite_id: int,
                 parent_id: int,
                 active_status: str,
                 call_date: datetime = None,
                 worksite_name: str = None,
                 phone: str = None,
                 city: str = None,
                 address_1: str = None,
                 address_2: str = None,
                 zip_code: int = None,
                 state: str = None,
                 memo: str = None):
        setattr(self, WorksiteColumn.WORKSITE_ID.value, int(worksite_id) if worksite_id and not pd.isna(worksite_id) else None)
        setattr(self, WorksiteColumn.WORKSITE_NAME.value, worksite_name)
        setattr(self, WorksiteColumn.ACTIVE_STATUS.value, active_status)
        setattr(self, WorksiteColumn.PARENT_WORKSITE_ID.value, int(parent_id) if parent_id and not pd.isna(parent_id) else None)
        setattr(self, WorksiteColumn.PHONE.value, phone)
        setattr(self, WorksiteColumn.CITY.value, city)
        setattr(self, WorksiteColumn.ADDRESS_1.value, address_1)
        setattr(self, WorksiteColumn.ADDRESS_2.value, address_2)
        setattr(self, WorksiteColumn.ZIP.value, int(zip_code) if zip_code and not pd.isna(zip_code) else None)
        setattr(self, WorksiteColumn.STATE.value, state)
        setattr(self, WorksiteColumn.CALL_DATE.value, call_date)
        setattr(self, WorksiteColumn.MEMO.value, memo)

        self.provider_ids = set()

        self.auxiliary = WorksiteAuxiliary()

    def __hash__(self):
        return hash(getattr(self, WorksiteColumn.WORKSITE_ID.value))

    @property
    def worksite_id(self):
        return getattr(self, WorksiteColumn.WORKSITE_ID.value)

    @property
    def parent_id(self):
        return getattr(self, WorksiteColumn.PARENT_WORKSITE_ID.value)

    @property
    def is_ultimate_parent(self):
        return getattr(self, WorksiteColumn.WORKSITE_ID.value) == getattr(self, WorksiteColumn.PARENT_WORKSITE_ID.value)

