
import logging

import pandas as pd

from ..entities import Organization
from hpinv_enums import WorksiteColumn


class OrganizationLoopManager:

    def __init__(self, worksites_df: pd.DataFrame):
        worksite_ids = list(worksites_df[WorksiteColumn.WORKSITE_ID.value])
        parent_worksite_ids = list(worksites_df[WorksiteColumn.PARENT_WORKSITE_ID.value])

        ultimate_parent_ids = set(
            worksites_df[
                worksites_df[WorksiteColumn.WORKSITE_ID.value] == worksites_df[WorksiteColumn.PARENT_WORKSITE_ID.value]
                ][WorksiteColumn.WORKSITE_ID.value]
        )

        self._parent_to_children_ids = dict()
        for (worksite_id, parent_worksite_id) in zip(worksite_ids, parent_worksite_ids):
            if parent_worksite_id not in self._parent_to_children_ids:
                self._parent_to_children_ids[parent_worksite_id] = set()
            self._parent_to_children_ids[parent_worksite_id].add(worksite_id)

        # Below changes during runtime
        self._loop_count = 0
        self.newly_placed_worksites = ultimate_parent_ids

        self._worksite_id_to_organization = {
            ultimate_parent_id: Organization(ultimate_parent_id)
            for ultimate_parent_id in ultimate_parent_ids
        }

        self._placed_children = set(self._worksite_id_to_organization.keys())
        self._all_worksite_ids = set(worksite_ids) | set(parent_worksite_ids)

    @property
    def all_worksites_have_been_placed(self) -> bool:
        return bool(self._all_worksite_ids - self._placed_children)

    @property
    def unplaced_children(self):
        return self._all_worksite_ids - self._placed_children

    @property
    def organizations(self) -> set[Organization]:
        return set(self._worksite_id_to_organization.values())

    def find_children_worksite_ids(self, parent_worksite_id: int) -> set[int]:
        return self._parent_to_children_ids[parent_worksite_id]

    def find_organization(self, worksite_id: int) -> Organization:
        if worksite_id not in self._worksite_id_to_organization:
            raise KeyError(
                f"Could not find an Organization that WorksiteId {worksite_id} belongs to."
            )

        return self._worksite_id_to_organization[worksite_id]

    def preprocess_for_new_loop(self, new_loop_count: int):
        self._loop_count = new_loop_count
        self.newly_placed_worksites = set()

    def add_child(
            self,
            child_worksite_id: int,
            parent_worksite_id: int,
            organization: Organization
    ):
        organization.add_child(
            child_worksite_id=child_worksite_id,
            parent_worksite_id=parent_worksite_id
        )

        self._placed_children.add(child_worksite_id)
        self.newly_placed_worksites.add(child_worksite_id)
        self._worksite_id_to_organization[child_worksite_id] = organization


def create_organizations(worksites_df: pd.DataFrame) -> dict:
    loop_data = OrganizationLoopManager(worksites_df=worksites_df)

    loop = 0
    while not loop_data.all_worksites_have_been_placed:
        new_parents = loop_data.newly_placed_worksites
        if not new_parents:
            raise RuntimeError(f"Worksites {loop_data.unplaced_children} are unable to be placed by loop {loop}.")

        logging.info(f"Organization creation loop: {loop}")
        for parent_worksite_id in new_parents:
            child_worksite_ids = loop_data.find_children_worksite_ids(parent_worksite_id)
            organization = loop_data.find_organization(worksite_id=parent_worksite_id)
            for child_worksite_id in child_worksite_ids:
                loop_data.add_child(
                    child_worksite_id=child_worksite_id,
                    parent_worksite_id=parent_worksite_id,
                    organization=organization
                )

        loop += 1
        loop_data.preprocess_for_new_loop(loop)

    return {org.ultimate_parent_worksite_id: org for org in loop_data.organizations}
