
import pandas as pd

from ..entities import Worksite
from . import utils

from hpinv_enums import ActiveStatusValue, WorksiteColumn


class WorksiteFactory:

    def __init__(
            self,
            additional_attribute_enums: list[WorksiteColumn]
    ):
        self.additional_attribute_enums = additional_attribute_enums

    def _apply_create_worksite(self, row, worksites: dict):
        worksite_id = row[WorksiteColumn.WORKSITE_ID.value]

        if worksite_id not in worksites:
            atts = utils.create_attributes_from_enums(
                row=row,
                enums=self.additional_attribute_enums
            )

            new_worksite = Worksite(
                worksite_id=row[WorksiteColumn.WORKSITE_ID.value],
                parent_worksite_id=row[WorksiteColumn.PARENT_WORKSITE_ID.value],
                additional_attributes=atts
            )

            worksites[worksite_id] = new_worksite

    def create_worksites(self, worksites_df: pd.DataFrame) -> dict:
        worksites = dict()
        worksites_df.apply(self._apply_create_worksite, axis=1, args=(worksites,))

        worksites_without_parents = set(worksite for worksite in worksites.values()
                                        if getattr(worksite, WorksiteColumn.PARENT_WORKSITE_ID.value) not in worksites)
        for worksite in worksites_without_parents:
            worksites[worksite.parent_id] = Worksite(worksite_id=worksite.parent_id,
                                                     parent_worksite_id=worksite.parent_id)

        return worksites


