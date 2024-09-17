from deepdiff import DeepDiff

class PrettyOrderedSet(set):
    def __repr__(self):
        return '[{}]'.format(", ".join(map(str, self)))

def compare_json(new_data, old_data):
    diff = DeepDiff(old_data, new_data, ignore_order=True, verbose_level=2).to_dict()
    return convert_diff_to_serializable(diff)

def convert_diff_to_serializable(diff):
    if isinstance(diff, dict):
        return {k: convert_diff_to_serializable(v) for k, v in diff.items()}
    elif isinstance(diff, list):
        return [convert_diff_to_serializable(i) for i in diff]
    elif isinstance(diff, (set, frozenset)):
        return list(diff)
    elif isinstance(diff, PrettyOrderedSet):
        return list(diff)
    else:
        return diff
