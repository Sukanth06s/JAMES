def merge_list(old, new):
    for item in new:
        if item not in old:
            old.append(item)


def merge_relationships(old, new):
    for rel in new:
        if not any(r.get("name") == rel.get("name") for r in old):
            old.append(rel)