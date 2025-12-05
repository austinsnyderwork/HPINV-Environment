
import pandas as pd

from ..entities import Provider
from hpinv_enums import HcpColumn, TypeId


class ProviderFactory:

    def __init__(
            self,
            hcp_id_col_name: str = None,
            additional_attribute_cols: list[str] = None,
    ):
        self.hcp_id_col_name = hcp_id_col_name if hcp_id_col_name else HcpColumn.HCP_ID.value
        self.additional_attribute_cols = additional_attribute_cols or []

    def _apply_create_provider(self, row, providers: dict):
        provider_id = row[self.hcp_id_col_name]

        if provider_id not in providers:
            type_id = row[HcpColumn.TYPE_ID.value]
            new_provider = Provider(
                hcp_id=provider_id,
                type_id=TypeId(type_id) if type_id is not None else type_id,
                additional_attributes={col: row[col] for col in self.additional_attribute_cols}
            )

            providers[provider_id] = new_provider

    def create_providers(self, hcp_df: pd.DataFrame):
        providers = dict()

        hcp_df.apply(self._apply_create_provider, providers=providers, axis=1)

        return providers


