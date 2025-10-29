

def create_attributes_from_enums(row, enums: list):
    atts = {
        enum.value: row[enum.value]
        for enum in enums
    }
    return atts