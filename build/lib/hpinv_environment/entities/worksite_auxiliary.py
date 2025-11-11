
from hpinv_enums import AuxiliaryColumn, WorksiteColumn


class HourSpecificAuxiliary:

    def __init__(self, hours: int):
        setattr(self, AuxiliaryColumn.HOURS.value, hours)
        setattr(self, AuxiliaryColumn.ASSISTANTS.value, 0)
        setattr(self, AuxiliaryColumn.HYGIENISTS.value, 0)
        setattr(self, AuxiliaryColumn.TRAINING_ASSISTANTS.value, 0)

    def __lt__(self, other):
        if not isinstance(other, HourSpecificAuxiliary):
            return NotImplemented

        this_hours = getattr(self, AuxiliaryColumn.HOURS.value)
        other_hours = getattr(other, AuxiliaryColumn.HOURS.value)

        return this_hours < other_hours

    def __eq__(self, other):
        if not isinstance(other, HourSpecificAuxiliary):
            return NotImplemented

        this_hours = getattr(self, AuxiliaryColumn.HOURS.value)
        other_hours = getattr(other, AuxiliaryColumn.HOURS.value)

        return this_hours == other_hours

    def __gt__(self, other):
        if not isinstance(other, HourSpecificAuxiliary):
            return NotImplemented

        this_hours = getattr(self, AuxiliaryColumn.HOURS.value)
        other_hours = getattr(other, AuxiliaryColumn.HOURS.value)

        return this_hours > other_hours


class WorksiteAuxiliary:

    def __init__(self, worksite_id: int):
        setattr(self, WorksiteColumn.WORKSITE_ID.value, worksite_id)
        setattr(self, AuxiliaryColumn.ASSISTANTS.value, dict())
        setattr(self, AuxiliaryColumn.HYGIENISTS.value, dict())
        setattr(self, AuxiliaryColumn.TRAINING_ASSISTANTS.value, dict())

        self._auxiliary_by_hours = dict()

    @property
    def hour_auxiliaries(self) -> list[HourSpecificAuxiliary]:
        return sorted(list(self._auxiliary_by_hours.values()))

    def add_auxiliary(self, auxiliary_type: AuxiliaryColumn, count: int, hours: int):

        if hours not in self._auxiliary_by_hours:
            self._auxiliary_by_hours[hours] = HourSpecificAuxiliary(hours=hours)

        aux_hours_object = self._auxiliary_by_hours[hours]
        current_count = getattr(aux_hours_object, auxiliary_type.value)
        setattr(self._auxiliary_by_hours[hours], auxiliary_type.value, current_count + count)

