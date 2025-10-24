
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .factories import create_organizations, create_providers, create_worksites
from .entities.organization import Organization
from .entities.provider import Provider
from .entities.worksite import Worksite

import hpinv_sql
import hpinv_enums


@dataclass
class HpinvEnvironment:
    providers: set[Provider]
    worksites: set[Worksite]
    organizations: set[Organization]


class WorksitesPullSpec(hpinv_sql.QueryPullSpec):

    def __init__(self):
        query_path = Path(__file__).parent / "queries" / "worksite_data.sql"
        super().__init__(query_path=query_path)


class HcpsPullSpec(hpinv_sql.QueryPullSpec):

    def __init__(self):
        query_path = Path(__file__).parent / "queries" / "hcp_data.sql"
        super().__init__(
            query_path=query_path
        )


class EnvironmentBuilder:

    @staticmethod
    def build_environment(
            worksites_df: pd.DataFrame = None,
            hcps_df: pd.DataFrame = None
    ) -> HpinvEnvironment:
        sql_manager = hpinv_sql.SqlManager()

        if not worksites_df:
            worksites_df = sql_manager.pull(WorksitesPullSpec())
        worksites_df.columns = [col.lower() for col in worksites_df.columns]

        worksites = create_worksites(worksites_df)
        worksites = set(worksites.values())

        organizations = create_organizations(worksites_df)
        organizations = set(organizations.values())

        if not hcps_df:
            hcps_df = sql_manager.pull(HcpsPullSpec())
        hcps_df.columns = [col.lower() for col in hcps_df.columns]
        providers = create_providers(hcps_df)
        providers = set(providers.values())

        return HpinvEnvironment(
            worksites=worksites,
            providers=providers,
            organizations=organizations
        )


