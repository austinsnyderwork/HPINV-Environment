
import logging

import pandas as pd

from ..entities import Organization
from hpinv_enums import WorksiteColumn


class OrganizationFactory:

    def __init__(self, worksites_df: pd.DataFrame):
        worksite_ids = list(worksites_df[WorksiteColumn.WORKSITE_ID.value])
        parent_worksite_ids = list(worksites_df[WorksiteColumn.PARENT_WORKSITE_ID.value])

        ultimate_parent_ids = set(
            worksites_df[
                worksites_df[WorksiteColumn.WORKSITE_ID.value] == worksites_df[WorksiteColumn.PARENT_WORKSITE_ID.value]
            ][WorksiteColumn.WORKSITE_ID.value]
        )

        self._parent_to_children_ids = {
            parent_worksite_id: set()
            for parent_worksite_id in parent_worksite_ids
        }
        for (worksite_id, parent_worksite_id) in zip(worksite_ids, parent_worksite_ids):
            self._parent_to_children_ids[parent_worksite_id].add(worksite_id)

        # Everything below changes during runtime
        self.loop_count = -1
        self._placed_worksites_by_loop = {
            -1: ultimate_parent_ids
        }

        self._worksite_id_to_organization = {
            ultimate_parent_id: Organization(ultimate_parent_id)
            for ultimate_parent_id in ultimate_parent_ids
        }

        self._all_worksites = set(worksite_ids) | set(parent_worksite_ids)

    @property
    def all_worksites_have_been_placed(self) -> bool:
        remaining_worksite_ids = self._all_worksites - self._placed_worksites
        return len(remaining_worksite_ids) == 0

    @property
    def _placed_worksites(self) -> set[int]:
        return {
            worksite_id
            for loop_count, placed_worksites in self._placed_worksites_by_loop.items()
            for worksite_id in placed_worksites
        }

    @property
    def unplaced_children(self) -> set[int]:
        return self._all_worksites - self._placed_worksites

    @property
    def organizations(self) -> set[Organization]:
        return set(self._worksite_id_to_organization.values())

    def fetch_newly_placed_worksites(self, loop_count: int):
        return self._placed_worksites_by_loop[loop_count]

    def _find_children_worksite_ids(self, parent_worksite_id: int) -> set[int]:
        if parent_worksite_id not in self._parent_to_children_ids:
            return {}

        return {
            child_worksite_id for child_worksite_id in self._parent_to_children_ids[parent_worksite_id]
            if child_worksite_id != parent_worksite_id
        }

    def _find_organization(self, worksite_id: int) -> Organization:
        if worksite_id not in self._worksite_id_to_organization:
            raise KeyError(f"Could not find an Organization that WorksiteId {worksite_id} belongs to.")

        return self._worksite_id_to_organization[worksite_id]

    def _add_child(
            self,
            child_worksite_id: int,
            parent_worksite_id: int
    ):
        organization = self._find_organization(parent_worksite_id)
        organization.add_child(
            child_worksite_id=child_worksite_id,
            parent_worksite_id=parent_worksite_id
        )

        self._placed_worksites_by_loop[self.loop_count].add(child_worksite_id)

        self._worksite_id_to_organization[child_worksite_id] = organization
        
    def create_organizations(self):
        while not self.all_worksites_have_been_placed:
            self.loop_count += 1
            self._placed_worksites_by_loop[self.loop_count] = set()

            new_parents = self.fetch_newly_placed_worksites(
                loop_count=self.loop_count - 1
            )
            if not new_parents:
                raise RuntimeError(f"Worksites {self.unplaced_children} are unable to be placed by loop {self.loop_count}.")

            print(f"Organization creation loop: {self.loop_count}")
            for parent_worksite_id in new_parents:
                child_worksite_ids = self._find_children_worksite_ids(parent_worksite_id)
                for child_worksite_id in child_worksite_ids:
                    self._add_child(
                        child_worksite_id=child_worksite_id,
                        parent_worksite_id=parent_worksite_id
                    )

        return {org.ultimate_parent_worksite_id: org for org in self.organizations}

