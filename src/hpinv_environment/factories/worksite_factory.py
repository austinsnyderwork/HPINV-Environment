
import pandas as pd

from ..entities import Worksite
from . import utils

from hpinv_enums import WorksiteColumn


class WorksiteFactory:

    def __init__(
            self,
            worksite_id_col_name: str = None,
            parent_worksite_id_col_name: str = None,
            additional_attribute_cols: list[str] = None
    ):
        self.worksite_id_col_name = worksite_id_col_name or WorksiteColumn.WORKSITE_ID.value
        self.parent_worksite_id_col_name = parent_worksite_id_col_name or WorksiteColumn.PARENT_WORKSITE_ID.value
        self.additional_attribute_cols = additional_attribute_cols or []

    def _apply_create_worksite(self, row, worksites: dict):
        worksite_id = row[WorksiteColumn.WORKSITE_ID.value]

        if worksite_id not in worksites:
            atts = utils.create_attributes_from_cols(
                row=row,
                cols=self.additional_attribute_cols
            )

            new_worksite = Worksite(
                worksite_id=row[WorksiteColumn.WORKSITE_ID.value],
                parent_worksite_id=row[WorksiteColumn.PARENT_WORKSITE_ID.value],
                transaction_id=row[WorksiteColumn.ACTIVE_STATUS.value],
                address_1=row[WorksiteColumn.ADDRESS_1.value],
                address_2=row[WorksiteColumn.ADDRESS_2.value],
                additional_attributes=atts
            )

            worksites[worksite_id] = new_worksite

    def create_worksites(self, worksites_df: pd.DataFrame) -> dict:
        worksites = dict()
        worksites_df.apply(self._apply_create_worksite, axis=1, args=(worksites,))

        worksites_with_nonexistent_parent = set(worksite for worksite in worksites.values()
                                                if getattr(worksite, WorksiteColumn.PARENT_WORKSITE_ID.value) not in worksites)
        for worksite in worksites_with_nonexistent_parent:
            worksites[worksite.parent_worksite_id] = (
                Worksite(
                    exists_in_hpinv=False,
                    worksite_id=worksite.parent_worksite_id,
                    parent_worksite_id=worksite.parent_worksite_id
                )
            )

        return worksites


