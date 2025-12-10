from datetime import datetime
from typing import Iterable

import hpinv_enums
import pandas as pd

from hpinv_enums import WorksiteColumn, ActiveStatus


class Worksite:

    def __init__(self,
                 worksite_id: int,
                 parent_worksite_id: int,
                 additional_attributes: dict = None,
                 **kwargs):
        self.worksite_id = int(worksite_id)
        self.parent_worksite_id = int(parent_worksite_id)

        if additional_attributes or kwargs:
            additional_attributes = additional_attributes or dict()
            kwargs = kwargs or dict()
            d = additional_attributes | kwargs
            for k, v in d.items():
                setattr(self, k, v)

        self.provider_ids = set(kwargs['provider_ids']) if 'provider_ids' in kwargs else set()

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
        return self.worksite_id == self.parent_worksite_id

    @property
    def full_address(self) -> str:
        street_parts = [getattr(self, WorksiteColumn.ADDRESS_1.value),
                        getattr(self, WorksiteColumn.ADDRESS_2.value)]
        street = " ".join(str(part).strip() for part in street_parts if part and str(part).strip())

        city = getattr(self, WorksiteColumn.CITY.value, "")
        state = getattr(self, WorksiteColumn.STATE.value, "")
        zip_code = getattr(self, WorksiteColumn.ZIP.value, "")
        if zip_code and not pd.isna(zip_code):
            zip_code = int(zip_code)
        country = "USA"

        comma_parts = [city, state, zip_code, country]

        # Convert everything to string just in case
        full = ", ".join(str(part) for part in [street] + comma_parts if part and str(part).strip())
        return full

    def to_dict(self):
        d = self.__dict__
        for k, v in d.items():
            if isinstance(v, set):
                d[k] = list(v)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Worksite":
        return Worksite(**d)
