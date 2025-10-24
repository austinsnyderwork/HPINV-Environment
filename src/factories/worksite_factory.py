
import pandas as pd

from src.entities import  Worksite

from hpinv_enums import ActiveStatusValue, WorksiteColumn


def _apply_create_worksite(row, worksites: dict):
    worksite_id = row[WorksiteColumn.WORKSITE_ID.value]

    if worksite_id not in worksites:
        new_worksite = Worksite(
            worksite_id=row[WorksiteColumn.WORKSITE_ID.value],
            worksite_name=row.get(WorksiteColumn.WORKSITE_NAME.value, None),
            parent_id=row[WorksiteColumn.PARENT_WORKSITE_ID.value],
            active_status=row[WorksiteColumn.ACTIVE_STATUS.value],
            call_date=row[WorksiteColumn.CALL_DATE.value],
            phone=row.get(WorksiteColumn.PHONE.value, None),
            city=row.get(WorksiteColumn.CITY.value, None),
            address_1=row.get(WorksiteColumn.ADDRESS_1.value, None),
            address_2=row.get(WorksiteColumn.ADDRESS_2.value, None),
            zip_code=row.get(WorksiteColumn.ZIP.value, None),
            state=row.get(WorksiteColumn.STATE.value, None),
            memo=row.get(WorksiteColumn.MEMO.value, None)
        )

        worksites[worksite_id] = new_worksite


def create_worksites(worksites_df: pd.DataFrame) -> dict:
    worksites = dict()
    worksites_df.apply(_apply_create_worksite, axis=1, args=(worksites,))

    worksites_without_parents = set(worksite for worksite in worksites.values() if worksite.parent_id not in worksites)
    for worksite in worksites_without_parents:
        worksites[worksite.parent_id] = Worksite(worksite_id=worksite.parent_id,
                                                 parent_id=worksite.parent_id,
                                                 active_status=ActiveStatusValue.INACTIVE.value)

    return worksites


