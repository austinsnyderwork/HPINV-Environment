from pathlib import Path

import pandas as pd
from hpinv_enums import WorksiteDetailColumn, TypeId

from .entities.worksite_detail import WorksiteDetail
from .factories import create_auxiliaries, OrganizationFactory, ProviderFactory, WorksiteFactory, WorksiteDetailFactory
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
                 worksite_details: dict[int: set[WorksiteDetail]] = None,
                 worksite_auxiliaries: dict[int: WorksiteAuxiliary] = None,
                 organizations: dict[int: Organization] = None
                 ):
        self._providers_dict = providers
        self._worksites_dict = worksites
        self._worksite_details_dict = worksite_details
        self._worksite_auxiliaries_dict = worksite_auxiliaries
        self._organizations_dict = organizations

    @property
    def providers(self) -> set:
        return set(self._providers_dict.values())

    @property
    def worksites(self) -> set:
        return set(self._worksites_dict.values())

    @property
    def worksite_details(self) -> set[WorksiteDetail]:
        return {
            worksite_detail
            for worksite_id, worksite_details in self._worksite_details_dict
            for worksite_detail in worksite_details
        }

    @property
    def worksite_auxiliaries(self) -> set[WorksiteAuxiliary]:
        return set(self._worksite_auxiliaries_dict.values())

    @property
    def organizations(self) -> set[Organization]:
        return set(self._organizations_dict.values())

    def fetch_provider(self, hcp_id: int) -> Provider:
        return self._providers_dict[hcp_id]

    def fetch_worksite(self, worksite_id: int) -> Worksite:
        return self._worksites_dict[worksite_id]

    def fetch_worksite_detail(self, worksite_id: int, type_id: TypeId) -> WorksiteDetail | None:
        if worksite_id not in self._worksite_details_dict:
            return None

        details = self._worksite_details_dict[worksite_id]
        for detail in details:
            if detail.type_id == type_id:
                return detail

        return None

    def fetch_worksite_auxiliary(self, worksite_id: int) -> WorksiteAuxiliary | None:
        if worksite_id not in self._worksite_auxiliaries_dict:
            return

        return self._worksite_auxiliaries_dict[worksite_id]

    def fetch_organization(self, ultimate_parent_worksite_id: int) -> Organization | None:
        return self._organizations_dict[ultimate_parent_worksite_id]


class WorksitesPullSpec(hpinv_sql.QueryPullSpec):

    def __init__(self):
        query_path = Path(__file__).parent / "queries" / "worksite_data.sql"
        super().__init__(query_path=query_path)


class WorksiteDetailsPullSpec(hpinv_sql.QueryPullSpec):

    def __init__(self):
        query_path = Path(__file__).parent / "queries" / "worksite_detail_data.sql"
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
            worksite_additional_attribute_enums: list[hpinv_enums.WorksiteColumn] = None,
            worksite_detail_additional_attribute_enums: list[hpinv_enums.WorksiteDetailColumn] = None,
            provider_additional_attribute_enums: list[hpinv_enums.HcpColumn] = None,
            existing_hpinv_env: HpinvEnvironment = None,
            worksites_df: pd.DataFrame = None,
            worksite_details_df: pd.DataFrame = None,
            hcps_df: pd.DataFrame = None,
            auxiliaries_df: pd.DataFrame = None
    ) -> HpinvEnvironment:
        sql_manager = hpinv_sql.HpinvSqlManager()

        if not worksites_df:
            worksites_df = sql_manager.pull(WorksitesPullSpec())
        worksites_df.columns = [col.lower() for col in worksites_df.columns]

        worksite_factory = WorksiteFactory(
            additional_attribute_cols=[e.value for e in worksite_additional_attribute_enums] if worksite_additional_attribute_enums else None
        )
        worksites = worksite_factory.create_worksites(worksites_df)

        if not worksite_details_df:
            worksite_details_df = sql_manager.pull(WorksiteDetailsPullSpec())
        worksite_details_df.columns = [col.lower() for col in worksite_details_df.columns]
        worksite_detail_factory = WorksiteDetailFactory(
            additional_attribute_cols=[e.value for e in worksite_detail_additional_attribute_enums] if worksite_detail_additional_attribute_enums else None
        )
        worksite_details = worksite_detail_factory.create_worksite_details(worksite_details_df)

        organizations = OrganizationFactory(worksites_df).create_organizations()

        if not hcps_df:
            hcps_df = sql_manager.pull(HcpsPullSpec())
        hcps_df.columns = [col.lower() for col in hcps_df.columns]
        provider_factory = ProviderFactory(
            additional_attribute_cols=[e.value for e in provider_additional_attribute_enums] if provider_additional_attribute_enums else None
        )
        providers = provider_factory.create_providers(hcps_df)

        if not auxiliaries_df:
            auxiliaries_df = sql_manager.pull(AuxiliariesPullSpec())
        auxiliaries_df.columns = [col.lower() for col in auxiliaries_df.columns]
        auxiliaries = create_auxiliaries(auxiliaries_df)

        if existing_hpinv_env:
            existing_hpinv_env._worksites_dict = worksites
            existing_hpinv_env._worksite_details_dict = worksite_details
            existing_hpinv_env._worksite_auxiliaries_dict = auxiliaries
            existing_hpinv_env._providers_dict = providers
            existing_hpinv_env._organizations_dict = organizations

            return existing_hpinv_env

        return HpinvEnvironment(
            worksites=worksites,
            worksite_details=worksite_details,
            worksite_auxiliaries=auxiliaries,
            providers=providers,
            organizations=organizations
        )
