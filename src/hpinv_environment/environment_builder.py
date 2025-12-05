from pathlib import Path

import pandas as pd
from hpinv_enums import WorksiteDetailColumn, TypeId
from typing import Iterable

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

    def fetch_worksite_detail(self, worksite_id: int, type_id: TypeId, missing_ok: bool = False) -> WorksiteDetail | None:
        if worksite_id not in self._worksite_details_dict:
            if missing_ok:
                return None
            else:
                raise ValueError(f"Could not find worksite {worksite_id} in worksite details.")

        details = self._worksite_details_dict[worksite_id]
        for detail in details:
            if detail.type_id == type_id:
                return detail

        if not missing_ok:
            raise ValueError(f"Found worksite {worksite_id}, but could not find worksite detail for {type_id}")

        return None

    def fetch_worksite_auxiliary(self, worksite_id: int) -> WorksiteAuxiliary | None:
        if worksite_id not in self._worksite_auxiliaries_dict:
            return

        return self._worksite_auxiliaries_dict[worksite_id]

    def fetch_organization(self, ultimate_parent_worksite_id: int) -> Organization | None:
        return self._organizations_dict[ultimate_parent_worksite_id]

    def load_environment_values(self,
                                providers: dict[int, Provider] = None,
                                worksites: dict[int, Worksite] = None,
                                worksite_details: dict[int, set[WorksiteDetail]] = None,
                                worksite_auxiliaries: dict[int, WorksiteAuxiliary] = None,
                                organizations: dict[int, Organization] = None
                                ):

        # Initialize internal dicts if they were None on __init__
        if self._providers_dict is None:
            self._providers_dict = {}
        if self._worksites_dict is None:
            self._worksites_dict = {}
        if self._worksite_details_dict is None:
            self._worksite_details_dict = {}
        if self._worksite_auxiliaries_dict is None:
            self._worksite_auxiliaries_dict = {}
        if self._organizations_dict is None:
            self._organizations_dict = {}

        # Update only what's provided
        if providers is not None:
            if not isinstance(providers, dict):
                raise TypeError("providers must be a dict[int, Provider]")
            self._providers_dict = providers

        if worksites is not None:
            if not isinstance(worksites, dict):
                raise TypeError("worksites must be a dict[int, Worksite]")
            self._worksites_dict = worksites

        if worksite_details is not None:
            if not isinstance(worksite_details, dict):
                raise TypeError("worksite_details must be a dict[int, set[WorksiteDetail]]")
            self._worksite_details_dict = worksite_details

        if worksite_auxiliaries is not None:
            if not isinstance(worksite_auxiliaries, dict):
                raise TypeError("worksite_auxiliaries must be a dict[int, WorksiteAuxiliary]")
            self._worksite_auxiliaries_dict = worksite_auxiliaries

        if organizations is not None:
            if not isinstance(organizations, dict):
                raise TypeError("organizations must be a dict[int, Organization]")
            self._organizations_dict = organizations


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

    def __init__(self):
        self._sql_manager = hpinv_sql.HpinvSqlManager()

    def create_worksites(self,
                         worksites_df: pd.DataFrame = None,
                         worksite_additional_attribute_enums: Iterable[hpinv_enums.WorksiteColumn] = None) -> dict:
        if not worksites_df:
            worksites_df = self._sql_manager.pull(WorksitesPullSpec())

        worksites_df.columns = [col.lower() for col in worksites_df.columns]

        worksite_factory = WorksiteFactory(
            additional_attribute_cols=[e.value for e in worksite_additional_attribute_enums] if worksite_additional_attribute_enums else None
        )
        worksites = worksite_factory.create_worksites(worksites_df)
        return worksites

    def create_worksite_details(self,
                                worksite_details_df: pd.DataFrame = None,
                                worksite_detail_additional_attribute_enums: list[hpinv_enums.WorksiteDetailColumn] = None)\
            -> dict:
        if not worksite_details_df:
            worksite_details_df = self._sql_manager.pull(WorksiteDetailsPullSpec())

        worksite_details_df.columns = [col.lower() for col in worksite_details_df.columns]

        worksite_detail_factory = WorksiteDetailFactory(
            additional_attribute_cols=worksite_detail_additional_attribute_enums
        )
        worksite_details = worksite_detail_factory.create_worksite_details(worksite_details_df)
        return worksite_details

    def create_organizations(self,
                             worksites_df: pd.DataFrame) -> dict:
        worksites_df.columns = [col.lower() for col in worksites_df.columns]

        organizations = OrganizationFactory(worksites_df).create_organizations()

        return organizations

    def create_providers(self,
                         hcps_df: pd.DataFrame = None,
                         provider_additional_attribute_enums: list[hpinv_enums.HcpColumn] = None) -> dict:
        if not hcps_df:
            hcps_df = self._sql_manager.pull(HcpsPullSpec())

        hcps_df.columns = [col.lower() for col in hcps_df.columns]

        provider_factory = ProviderFactory(
            additional_attribute_cols=[e.value for e in provider_additional_attribute_enums] if provider_additional_attribute_enums else None
        )
        providers = provider_factory.create_providers(hcps_df)

        return providers

    def create_auxiliaries(self,
                           auxiliaries_df: pd.DataFrame) -> dict:
        if not auxiliaries_df:
            auxiliaries_df = self._sql_manager.pull(AuxiliariesPullSpec())

        auxiliaries_df.columns = [col.lower() for col in auxiliaries_df.columns]
        auxiliaries = create_auxiliaries(auxiliaries_df)

        return auxiliaries

    def build_environment(
            self,
            fill_existing_env: HpinvEnvironment = None,
            worksite_additional_attribute_enums: Iterable[hpinv_enums.WorksiteColumn] = None,
            worksite_detail_additional_attribute_enums: Iterable[hpinv_enums.WorksiteDetailColumn] = None,
            provider_additional_attribute_enums: Iterable[hpinv_enums.HcpColumn] = None,
            worksites_df: pd.DataFrame = None,
            worksite_details_df: pd.DataFrame = None,
            hcps_df: pd.DataFrame = None,
            auxiliaries_df: pd.DataFrame = None
    ) -> HpinvEnvironment | None:
        worksites = self.create_worksites(worksite_additional_attribute_enums=worksite_additional_attribute_enums,
                                          worksites_df=worksites_df)
        worksite_details = self.create_worksite_details(worksite_detail_additional_attribute_enums=worksite_detail_additional_attribute_enums,
                                                        worksite_details_df=worksite_details_df)
        auxiliaries = self.create_auxiliaries(auxiliaries_df=auxiliaries_df)
        providers = self.create_providers(provider_additional_attribute_enums=provider_additional_attribute_enums,
                                          hcps_df=hcps_df)

        organizations = self.create_organizations(worksites_df=worksites_df)

        if fill_existing_env:
            fill_existing_env.load_environment_values(
                providers=providers,
                worksites=worksites,
                worksite_details=worksite_details,
                worksite_auxiliaries=auxiliaries,
                organizations=organizations
            )
            return

        return HpinvEnvironment(
            worksites=worksites,
            worksite_details=worksite_details,
            worksite_auxiliaries=auxiliaries,
            providers=providers,
            organizations=organizations
        )
