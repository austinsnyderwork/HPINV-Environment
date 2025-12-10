from datetime import date

from hpinv_enums import HcpColumn, HcpPositionColumn, WorksiteColumn, TypeId


class WorksitePosition:

    def __init__(self,
                 attributes: dict):
        for k, v in attributes.items():
            setattr(self, k, v)

    def __hash__(self):
        return hash(getattr(self, HcpPositionColumn.WORKSITE_HISTORY_ID.value))

    def __lt__(self, other):
        if not isinstance(other, WorksitePosition):
            return NotImplemented

        this_effect_date = getattr(self, HcpPositionColumn.EFFECT_DATE.value)
        other_effect_date = getattr(other, HcpPositionColumn.EFFECT_DATE.value)
        if this_effect_date < other_effect_date:
            return True
        elif this_effect_date == other_effect_date:
            this_worksite_history_id = getattr(self, HcpPositionColumn.WORKSITE_HISTORY_ID.value)
            other_worksite_history_id = getattr(other, HcpPositionColumn.WORKSITE_HISTORY_ID.value)
            return this_worksite_history_id < other_worksite_history_id

        return False

    def __gt__(self, other):
        if not isinstance(other, WorksitePosition):
            return NotImplemented

        this_effect_date = getattr(self, HcpPositionColumn.EFFECT_DATE.value)
        other_effect_date = getattr(other, HcpPositionColumn.EFFECT_DATE.value)
        if this_effect_date > other_effect_date:
            return True
        elif this_effect_date == other_effect_date:
            this_worksite_history_id = getattr(self, HcpPositionColumn.WORKSITE_HISTORY_ID.value)
            other_worksite_history_id = getattr(other, HcpPositionColumn.WORKSITE_HISTORY_ID.value)
            return this_worksite_history_id > other_worksite_history_id

        return False


class Provider:

    def __init__(self,
                 hcp_id: int,
                 type_id: TypeId,
                 additional_attributes: dict = None):
        self.hcp_id = hcp_id
        setattr(self, HcpColumn.HCP_ID.value, hcp_id)
        self.type_id = type_id
        setattr(self, HcpColumn.TYPE_ID.value, type_id)

        if additional_attributes:
            for k, v in additional_attributes.items():
                setattr(self, k, v)

    @property
    def full_name(self) -> str:
        return f"{getattr(self, HcpColumn.FIRST_NAME.value)} {getattr(self, HcpColumn.LAST_NAME.value)}"

    def to_dict(self) -> dict:
        return self.__dict__
