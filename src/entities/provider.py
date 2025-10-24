from datetime import date

from hpinv_enums import HcpColumn, HcpPositionColumn, WorksiteColumn, TypeId


class WorksitePosition:

    def __init__(self,
                 worksite_history_id: int,
                 effect_date: date,
                 worksite_id: int,
                 specialty: str,
                 fte: str,
                 work_hours: int,
                 work_weeks: int,
                 face_time: int,
                 percent_medicaid: int,
                 percent_sliding_fee: int
                 ):
        setattr(self, HcpPositionColumn.WORKSITE_HISTORY_ID.value, worksite_history_id)
        setattr(self, HcpPositionColumn.EFFECT_DATE.value, effect_date)
        setattr(self, WorksiteColumn.WORKSITE_ID.value, worksite_id)
        setattr(self, HcpPositionColumn.SPECIALTY_NAME.value, specialty)
        setattr(self, HcpPositionColumn.FTE.value, fte)
        setattr(self, HcpPositionColumn.WORK_HOURS.value, work_hours)
        setattr(self, HcpPositionColumn.WORK_WEEKS.value, work_weeks)
        setattr(self, HcpPositionColumn.FACE_TIME.value, face_time)
        setattr(self, HcpPositionColumn.PERCENT_MEDICAID.value, percent_medicaid)
        setattr(self, HcpPositionColumn.PERCENT_SLIDING_FEE.value, percent_sliding_fee)

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
                 first_name: str,
                 last_name: str):
        setattr(self, HcpColumn.HCP_ID.value, hcp_id)
        setattr(self, HcpColumn.TYPE_ID.value, type_id)
        setattr(self, HcpColumn.FIRST_NAME.value, first_name)
        setattr(self, HcpColumn.LAST_NAME.value, last_name)

