
import pandas as pd

from hpinv_enums import WorksiteDetailColumn, TypeId
from ..entities.worksite_detail import WorksiteDetail


class WorksiteDetailFactory:

    def __init__(
            self,
            worksite_id_col_name: str = None,
            type_id_col_name: str = None,
            additional_attribute_cols: list[str] = None
    ):
        self._worksite_id_col_name = worksite_id_col_name or WorksiteDetailColumn.WORKSITE_ID.value
        self._type_id_col_name = type_id_col_name or WorksiteDetailColumn.TYPE_ID.value
        self._additional_attribute_cols = additional_attribute_cols or []

    def _apply_create_worksite_details(self, row, worksite_details: dict):
        ws_id = row[self._worksite_id_col_name]
        worksite_detail = WorksiteDetail(
            worksite_id=ws_id,
            type_id=TypeId(row[self._type_id_col_name]),
            additional_attributes={
                k: row[k] for k in self._additional_attribute_cols
            }
        )
        worksite_details[ws_id].add(worksite_detail)

    def create_worksite_details(self, worksite_details_df: pd.DataFrame) -> dict:
        worksite_details = {
            worksite_id: set()
            for worksite_id in set(worksite_details_df[self._worksite_id_col_name])
        }
        worksite_details_df.apply(self._apply_create_worksite_details, args=(worksite_details,), axis=1)
        return worksite_details

