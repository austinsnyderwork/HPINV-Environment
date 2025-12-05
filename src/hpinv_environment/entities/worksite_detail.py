from hpinv_enums import HcpColumn, TypeId, ActiveStatus


class WorksiteDetail:

    def __init__(self,
                 worksite_id: int,
                 type_id: str,
                 additional_attributes: dict = None,
                 **kwargs):
        self.worksite_id = worksite_id
        self.type_id = TypeId(type_id)

        if additional_attributes or kwargs:
            additional_attributes = additional_attributes or dict()
            kwargs = kwargs or dict()
            d = additional_attributes | kwargs
            for k, v in d.items():
                setattr(self, k, v)

    def __key(self):
        return self.worksite_id, self.type_id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, WorksiteDetail):
            return False
        return self.__key() == other.__key()
