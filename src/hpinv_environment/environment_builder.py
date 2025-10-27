from pathlib import Path

import pandas as pd

from .factories import create_organizations, create_providers, create_worksites
from .entities.organization import Organization
from .entities.provider import Provider
from .entities.worksite import Worksite
from .entities.worksite import WorksiteAuxiliary

import hpinv_sql
import hpinv_enums


class HpinvEnvironment:

    def __init__(self,
                 providers: dict[int: Provider],
                 worksites: dict[int: Worksite],
                 worksite_auxiliaries: dict[int: WorksiteAuxiliary],
                 organizations: dict[int: Organization]
                 ):
        self._providers = providers
        self._worksites = worksites
        self._worksite_auxiliaries = worksite_auxiliaries
        self._organizations = organizations

    @property
    def providers(self):
        return set(self._providers.values())

    @property
    def worksites(self):
        return set(self._worksites.values())

    @property
    def organizations(self):
        return set(self._organizations.values())

    def fetch_provider(self, hcp_id: int):
        return self._providers[hcp_id]

    def fetch_worksite(self, worksite_id: int):
        return self._worksites[worksite_id]

    def fetch_worksite_auxiliary(self, worksite_id: int):
        return self._worksite_auxiliaries[worksite_id]

    def fetch_organization(self, ultimate_parent_worksite_id: int):
        return self._organizations[ultimate_parent_worksite_id]

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
