from datetime import datetime
from typing import Iterable

import hpinv_enums
import pandas as pd

from hpinv_enums import WorksiteColumn


class Worksite:

    def __init__(self,
                 worksite_id: int,
                 parent_worksite_id: int,
                 exists_in_hpinv: bool = True,
                 transaction_id: hpinv_enums.TransactionId = None,
                 address_1: str = None,
                 address_2: str = None,
                 additional_attributes: dict = None,
                 **kwargs):
        self.exists_in_hpinv = exists_in_hpinv

        self.worksite_id = int(worksite_id) if worksite_id and not pd.isna(worksite_id) else None
        self.parent_worksite_id = int(parent_worksite_id) if parent_worksite_id and not pd.isna(parent_worksite_id) else None

        self.transaction_id = transaction_id

        self.address_1 = address_1
        self.address_2 = address_2

        if additional_attributes or kwargs:
            additional_attributes = additional_attributes or dict()
            kwargs = kwargs or dict()
            d = additional_attributes | kwargs
            for k, v in d.items():
                setattr(self, k, v)

        self.provider_ids = set(kwargs['provider_ids']) or set()

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
    def full_address(self) -> str:
        street_parts = [self.address_1, self.address_2]
        street = " ".join(str(part).strip() for part in street_parts if part and str(part).strip())

        city = getattr(self, WorksiteColumn.CITY.value, "")
        state = getattr(self, WorksiteColumn.STATE.value, "")
        zip_code = getattr(self, WorksiteColumn.ZIP.value, "")
        country = "USA"

        comma_parts = [city, state, zip_code, country]

        # Convert everything to string just in case
        full = ", ".join(str(part) for part in [street] + comma_parts if part and str(part).strip())
        return full

    def to_dict(self):
        d = self.__dict__
        for k, v in d.items():
            if isinstance(v, Iterable) and not isinstance(v, list):
                d[k] = list(v)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Worksite":
        return Worksite(**d)
