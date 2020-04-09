from typing import Optional


class TypeMapperMixin(object):

    TYPE_MAP = {
        "ZAKAZ": "order",
        "VVOD_IMPORT": "input_import",
        "VVOD_REMAINS": "input_remains",
        "RMK_STORE": "receipt_receipt",
        "OTGRUZKA": "out_out",
    }

    @classmethod
    def map_type(cls, file_type: str) -> Optional[str]:
        return cls.TYPE_MAP.get(file_type)
