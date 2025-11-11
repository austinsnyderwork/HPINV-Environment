from pathlib import Path

import pandas as pd

from .factories import create_auxiliaries, create_organizations, ProviderFactory, WorksiteFactory
from .entities.organization import Organization
from .entities.provider import Provider
from .entities.worksite import Worksite
from .entities.worksite_auxiliary import WorksiteAuxiliary

import hpinv_sql
import hpinv_enums


class HpinvEnvironment:

    def __init__(self,
                 providers: dict[int: Provider] = None,
                 worksites: dict[int: Worksite] = None,
                 worksite_auxiliaries: dict[int: WorksiteAuxiliary] = None,
                 organizations: dict[int: Organization] = None
                 ):
        self._providers_dict = providers
        self._worksites_dict = worksites
        self._worksite_auxiliaries_dict = worksite_auxiliaries
        self._organizations_dict = organizations

    @property
    def providers(self) -> set:
        return set(self._providers_dict.values())

    @property
    def worksites(self) -> set:
        return set(self._worksites_dict.values())

    @property
    def worksite_auxiliaries(self) -> set:
        return set(self._worksite_auxiliaries_dict.values())

    @property
    def organizations(self) -> set:
        return set(self._organizations_dict.values())

    def fetch_provider(self, hcp_id: int):
        return self._providers_dict[hcp_id]

    def fetch_worksite(self, worksite_id: int):
        return self._worksites_dict[worksite_id]

    def fetch_worksite_auxiliary(self, worksite_id: int) -> WorksiteAuxiliary | None:
        if worksite_id not in self._worksite_auxiliaries_dict:
            return

        return self._worksite_auxiliaries_dict[worksite_id]

    def fetch_organization(self, ultimate_parent_worksite_id: int):
        return self._organizations_dict[ultimate_parent_worksite_id]


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


class AuxiliariesPullSpec(hpinv_sql.QueryPullSpec):

    def __init__(self):
        query_path = Path(__file__).parent / "queries" / "aux_data.sql"
        super().__init__(
            query_path=query_path
        )


class EnvironmentBuilder:

    @staticmethod
    def build_environment(
            worksite_additional_attribute_enums: list[hpinv_enums.WorksiteColumn],
            provider_additional_attribute_enums: list[hpinv_enums.HcpColumn],
            existing_hpinv_env: HpinvEnvironment = None,
            worksites_df: pd.DataFrame = None,
            hcps_df: pd.DataFrame = None,
            auxiliaries_df: pd.DataFrame = None
    ) -> HpinvEnvironment:
        sql_manager = hpinv_sql.SqlManager()

        if not worksites_df:
            worksites_df = sql_manager.pull(WorksitesPullSpec())
        worksites_df.columns = [col.lower() for col in worksites_df.columns]

        worksite_factory = WorksiteFactory(
            additional_attribute_enums=worksite_additional_attribute_enums
        )
        worksites = worksite_factory.create_worksites(worksites_df)

        organizations = create_organizations(worksites_df)

        if not hcps_df:
            hcps_df = sql_manager.pull(HcpsPullSpec())
        hcps_df.columns = [col.lower() for col in hcps_df.columns]
        provider_factory = ProviderFactory(additional_attribute_enums=provider_additional_attribute_enums)
        providers = provider_factory.create_providers(hcps_df)

        if not auxiliaries_df:
            auxiliaries_df = sql_manager.pull(AuxiliariesPullSpec())
        auxiliaries_df.columns = [col.lower() for col in auxiliaries_df.columns]
        auxiliaries = create_auxiliaries(auxiliaries_df)

        if existing_hpinv_env:
            existing_hpinv_env._worksites_dict = worksites
            existing_hpinv_env._worksite_auxiliaries_dict = auxiliaries
            existing_hpinv_env._providers_dict = providers
            existing_hpinv_env._organizations_dict = organizations

            return existing_hpinv_env

        return HpinvEnvironment(
            worksites=worksites,
            worksite_auxiliaries=auxiliaries,
            providers=providers,
            organizations=organizations
        )
