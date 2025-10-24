
from hpinv_enums import AuxiliaryColumn


class AuxiliaryByHours:

    def __init__(self, hours: int):
        setattr(self, AuxiliaryColumn.HOURS.value, hours)
        setattr(self, AuxiliaryColumn.ASSISTANTS.value, 0)
        setattr(self, AuxiliaryColumn.HYGIENISTS.value, 0)
        setattr(self, AuxiliaryColumn.TRAINING_ASSISTANTS.value, 0)


class WorksiteAuxiliary:

    def __init__(self):
        setattr(self, AuxiliaryColumn.ASSISTANTS.value, dict())
        setattr(self, AuxiliaryColumn.HYGIENISTS.value, dict())
        setattr(self, AuxiliaryColumn.TRAINING_ASSISTANTS.value, dict())

        self.auxiliary_by_hours = dict()

    @property
    def all_hours(self) -> set:
        return set(self.auxiliary_by_hours.keys())

    def add_auxiliary(self, auxiliary_type: AuxiliaryColumn, count: int, hours: int):

        if hours not in self.auxiliary_by_hours:
            self.auxiliary_by_hours[hours] = AuxiliaryByHours(hours=hours)

        aux_hours_object = self.auxiliary_by_hours[hours]
        current_count = getattr(aux_hours_object, auxiliary_type.value)
        setattr(self.auxiliary_by_hours[hours], auxiliary_type.value, current_count + count)

    def fetch_auxiliary_staff(self):
        return self.auxiliary_by_hours

