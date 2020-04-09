import re
from typing import Optional, Dict

from apps.project.models import Task

path_regex = re.compile(r"(/?(?P<state>\w+))?(/(?P<file>.+))?")

prefixes = tuple(map(lambda x: x[0], Task.PREFIXES))
doctypes = tuple(map(lambda x: x[0], Task.TYPES))

pattern = r"((?P<prefix>(%s))_)?(?P<doctype>(%s))_(?P<doc_id>.+)\.(?P<extension>.+)" % (
    "|".join(prefixes),
    "|".join(doctypes),
)

file_regex = re.compile(pattern)


def parse_path(path: str) -> Optional[Dict]:
    if path is None:
        return

    matches = path_regex.search(path)

    if matches:
        return matches.groupdict()


def parse_file(filename: str) -> Optional[Dict]:
    if filename is None:
        return
    matches = file_regex.search(filename)

    if matches:
        return matches.groupdict()
