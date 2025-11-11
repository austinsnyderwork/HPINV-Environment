
import pandas as pd

from ..entities import Provider
from hpinv_enums import HcpColumn
from .utils import create_attributes_from_enums


class ProviderFactory:

    def __init__(
            self,
            additional_attribute_enums: list[HcpColumn]
    ):
        self.additional_attribute_enums = additional_attribute_enums

    def _apply_create_provider(self, row, providers: dict):
        provider_id = row[HcpColumn.HCP_ID.value]

        if provider_id not in providers:
            atts = create_attributes_from_enums(
                row=row,
                enums=self.additional_attribute_enums
            )
            new_provider = Provider(
                hcp_id=provider_id,
                type_id=row[HcpColumn.TYPE_ID.value],
                additional_attributes=atts
            )

            providers[provider_id] = new_provider

    def create_providers(self, hcp_df: pd.DataFrame):
        providers = dict()

        hcp_df.apply(self._apply_create_provider, providers=providers, axis=1)

        return providers


