from hpinv_enums import HcpColumn, TypeId


class WorksiteDetail:

    def __init__(self,
                 worksite_id: int,
                 type_id: TypeId,
                 additional_attributes: dict = None):
        self.worksite_id = worksite_id
        self.type_id = type_id

        if additional_attributes:
            for k, v in additional_attributes.items():
                setattr(self, k, v)

    def __key(self):
        return self.worksite_id, self.type_id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, WorksiteDetail):
            return False
        return self.__key() == other.__key()
