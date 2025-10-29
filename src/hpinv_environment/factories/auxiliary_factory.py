
import pandas as pd

from ..entities import WorksiteAuxiliary

from hpinv_enums import WorksiteColumn, AuxiliaryColumn


def _apply_create_auxiliary(row, auxiliaries: dict):
    worksite_id = int(row[WorksiteColumn.WORKSITE_ID.value])

    if worksite_id not in auxiliaries:
        auxiliaries[worksite_id] = WorksiteAuxiliary(worksite_id=worksite_id)

    aux = auxiliaries[worksite_id]

    work_hours = int(row[AuxiliaryColumn.HOURS.value])

    assistants = int(row[AuxiliaryColumn.ASSISTANTS.value])
    hygienists = int(row[AuxiliaryColumn.HYGIENISTS.value])
    training_assistants = int(row[AuxiliaryColumn.TRAINING_ASSISTANTS.value])

    aux.add_auxiliary(
        auxiliary_type=AuxiliaryColumn.ASSISTANTS,
        count=assistants,
        hours=work_hours
    )

    aux.add_auxiliary(
        auxiliary_type=AuxiliaryColumn.HYGIENISTS,
        count=hygienists,
        hours=work_hours
    )

    aux.add_auxiliary(
        auxiliary_type=AuxiliaryColumn.TRAINING_ASSISTANTS,
        count=training_assistants,
        hours=work_hours
    )


def create_auxiliaries(auxiliary_df: pd.DataFrame) -> dict:
    auxiliaries = dict()
    auxiliary_df.apply(_apply_create_auxiliary, args=(auxiliaries,), axis=1)

    return auxiliaries


