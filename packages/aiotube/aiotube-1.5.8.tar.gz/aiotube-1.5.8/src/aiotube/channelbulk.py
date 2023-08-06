from ._threads import _Thread
from ._http import _get_channel_about
from ._rgxs import _ChannelPatterns as rgx
from typing import List, Optional, Dict, Any


class _ChannelBulk:

    __HEAD = 'https://www.youtube.com/channel/'

    def __init__(self, iterable: list):
        self._channel_ids = iterable
        self.__bulk_data = self.__fetch_all

    @property
    def __fetch_all(self):
        urls = [self.__HEAD + id for id in self._channel_ids]
        return _Thread.run(_get_channel_about, urls)

    def _gen_bulk(self):
        info_list = [self._gen_info(source) for source in self.__bulk_data]
        return {info.pop('id'): info for info in info_list}

    @staticmethod
    def _gen_info(source: str) -> Optional[Dict[str, Dict[str, Any]]]:
        info = {}

        def extract(pattern):
            d = pattern.findall(source)
            return d[0] if d else None

        patterns = [
            rgx.name, rgx.subscribers, rgx.views, rgx.creation,
            rgx.country, rgx.custom_url, rgx.avatar, rgx.banner, rgx.id,
            rgx.verified, rgx.description
        ]

        data = _Thread.run(extract, patterns)

        if data[2]:
            views = data[2].split(' ')[0]
        else:
            views = None

        if data[10]:
            description = data[10].replace('\\n', '\n')
        else:
            description = None

        curl = data[5] if data[5] and '/channel/' not in data[5] else None

        info['id'] = data[8]
        info['name'] = data[0]
        info['subscribers'] = data[1]
        info['views'] = views
        info['created_at'] = data[3]
        info['country'] = data[4]
        info['custom_url'] = curl
        info['avatar'] = data[6]
        info['banner'] = data[7]
        info['url'] = f'https://www.youtube.com/channel/{data[8]}'
        info['description'] = description.replace('\\n', '\n') if description else None
        info['verified'] = True if data[9] else False

        return info
