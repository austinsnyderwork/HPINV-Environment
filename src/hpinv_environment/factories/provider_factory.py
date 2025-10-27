
import pandas as pd

from src.entities import Provider
from hpinv_enums import WorksiteColumn, HcpColumn, HcpPositionColumn


def _apply_create_provider(row, providers: dict):
    provider_id = row[HcpColumn.HCP_ID.value]

    if provider_id not in providers:

        new_provider = Provider(
            hcp_id=provider_id,
            type_id=row[HcpColumn.TYPE_ID.value],
            first_name=row[HcpColumn.FIRST_NAME.value],
            last_name=row[HcpColumn.LAST_NAME.value]
        )

        providers[provider_id] = new_provider


def create_providers(hcp_df: pd.DataFrame):
    providers = dict()

    hcp_df.apply(_apply_create_provider, providers=providers, axis=1)

    return providers


