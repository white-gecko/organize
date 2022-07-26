import sys
from typing import Union

import simplematch as sm

from organize.utils import flatten

from .filter import Filter, FilterResult


def parse_tag(s):
    """parse a tag definition and return a tuple (name, color)"""
    result = sm.match("{name} ({color})", s)
    if not result:
        return s, "none"
    return result["name"], result["color"].lower()


def list_tags(path):
    import macos_tags

    tags = macos_tags.get_all(path)
    return ["{} ({})".format(tag.name, tag.color.name.lower()) for tag in tags]


class MacOSTags(Filter):
    """Filter by macOS tags

    Args:
        *tags (list(str) or str):
            The tags to filter by
    """

    name = "macos_tags"
    schema_support_instance_without_args = True

    def __init__(self, *tags) -> None:
        self.filter_tags = list(flatten(list(tags)))

    def matches(self, tags: str) -> Union[bool, str]:
        if not self.filter_tags:
            return True
        if not tags:
            return False
        for tag in tags:
            if any(sm.test(filter_tag, tag) for filter_tag in self.filter_tags):
                return True
        return False

    def pipeline(self, args: dict) -> FilterResult:
        fs = args["fs"]  # type: FS
        fs_path = args["fs_path"]
        path = fs.getsyspath(fs_path)

        if sys.platform != "darwin":
            self.print("The macos_tags filter is only available on macOS")
            return

        tags = list_tags(path)

        return FilterResult(
            matches=bool(self.matches(tags)),
            updates={self.get_name(): tags},
        )

    def __str__(self):
        return "MacOSTags(tags=%s)" % ", ".join(self.filter_tags)
