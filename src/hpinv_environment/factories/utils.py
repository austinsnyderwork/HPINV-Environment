

def create_attributes_from_cols(row, cols: list[str]):
    atts = {
        col: row[col]
        for col in cols
    }
    return atts
