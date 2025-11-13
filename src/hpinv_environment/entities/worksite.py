from datetime import datetime

import pandas as pd

from hpinv_enums import WorksiteColumn


class Worksite:

    def __init__(self,
                 worksite_id: int,
                 parent_worksite_id: int,
                 additional_attributes: dict = None):
        self.worksite_id = int(worksite_id) if worksite_id and not pd.isna(worksite_id) else None
        setattr(self, WorksiteColumn.WORKSITE_ID.value, worksite_id)
        self.parent_worksite_id = int(parent_worksite_id) if parent_worksite_id and not pd.isna(parent_worksite_id) else None
        setattr(self, WorksiteColumn.PARENT_WORKSITE_ID.value, parent_worksite_id)

        if additional_attributes:
            for k, v in additional_attributes.items():
                setattr(self, k, v)

        self.provider_ids = set()

    def __key(self):
        return self.worksite_id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, Worksite):
            return False

        return self.__key() == other.__key()

    @property
    def is_ultimate_parent(self):
        worksite_id = getattr(self, WorksiteColumn.WORKSITE_ID.value)
        parent_worksite_id = getattr(self, WorksiteColumn.PARENT_WORKSITE_ID.value)

        return worksite_id == parent_worksite_id

    @property
    def full_address(self):
        address_1 = getattr(self, WorksiteColumn.ADDRESS_1.value)
        address_2 = getattr(self, WorksiteColumn.ADDRESS_2.value)

        return f"{address_1} {address_2}"
