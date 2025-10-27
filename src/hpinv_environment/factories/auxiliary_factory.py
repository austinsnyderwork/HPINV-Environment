
import pandas as pd

from hpinv_enums import WorksiteColumn, AuxiliaryColumn


def _apply_create_auxiliary(row, worksites: dict):
    worksite_id = int(row[WorksiteColumn.WORKSITE_ID.value])
    worksite = worksites[worksite_id]

    work_hours = int(row[AuxiliaryColumn.HOURS.value])

    assistants = int(row[AuxiliaryColumn.ASSISTANTS.value])
    hygienists = int(row[AuxiliaryColumn.HYGIENISTS.value])
    training_assistants = int(row[AuxiliaryColumn.TRAINING_ASSISTANTS.value])

    worksite.auxiliary.add_auxiliary(
        auxiliary_type=AuxiliaryColumn.ASSISTANTS,
        count=assistants,
        hours=work_hours
    )

    worksite.auxiliary.add_auxiliary(
        auxiliary_type=AuxiliaryColumn.HYGIENISTS,
        count=hygienists,
        hours=work_hours
    )

    worksite.auxiliary.add_auxiliary(
        auxiliary_type=AuxiliaryColumn.TRAINING_ASSISTANTS,
        count=training_assistants,
        hours=work_hours
    )


def fill_worksites_with_auxiliary(auxiliary_df: pd.DataFrame, worksites: dict):
    auxiliary_df.apply(_apply_create_auxiliary, worksites=worksites, axis=1)


