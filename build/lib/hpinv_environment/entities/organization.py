

def _find_dict_parent(d: dict, parent_key) -> dict | None:
    for k, v in d.items():
        if k == parent_key:
            return v
        if isinstance(v, dict):
            result = _find_dict_parent(v, parent_key)
            if result is not None:
                return result
    return None


class Organization:

    def __init__(self,
                 ultimate_parent_worksite_id: int,
                 additional_attributes: dict = None):
        self.ultimate_parent_worksite_id = ultimate_parent_worksite_id

        if additional_attributes:
            for k, v in additional_attributes.items():
                setattr(self, k, v)

        self.children_hierarchy = dict()
        self.all_worksite_ids = {ultimate_parent_worksite_id}

    def __hash__(self):
        return hash(self.ultimate_parent_worksite_id)

    @property
    def child_worksite_ids(self) -> set[int]:
        return {worksite_id for worksite_id in self.all_worksite_ids if worksite_id != self.ultimate_parent_worksite_id}

    def add_child(self, child_worksite_id: int, parent_worksite_id: int):
        parent_dict = _find_dict_parent(
            d=self.children_hierarchy,
            parent_key=parent_worksite_id
        )

        if not parent_dict:
            raise ValueError(
                f"Could not find parent WorksiteId {parent_worksite_id} to add child {child_worksite_id}."
                f"\nMust add the parent before adding its children.")

        parent_dict[child_worksite_id] = dict()
        self.all_worksite_ids.add(child_worksite_id)


