"""
The MIT License (MIT)

Copyright (c) 2022-present ShomyKohai

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from .images import Image


class Character:
    """Represents a :class:`Character` istance

    .. versionadded:: 0.2.0

    Attributes
    -----------
    media_id: :class:`int`
        ID of the character's origin media
    id: :class:`int`
        ID of the character
    name: :class:`str`
        Return characters canonical name
    slug: :class:`str`
        String identifier. Work as id to fetch data
    description: :class:`str`
        The character's description
    role: Literal[:class:`str`]
        Role of the character ("main" or "supporting")
    mal_id: :class:`int`
        Character ID on My Anime List
    image: :class:`str`
        Return character's image
    """

    __slots__ = (
        "id",
        "type",
        "media_id",
        "name",
        "slug",
        "description",
        "role",
        "slug",
        "mal_id",
        "_attributes",
    )

    def __init__(
        self, attributes: dict, *, role: str = None, entry_id: int = None, **kwargs
    ):
        data = attributes["attributes"]
        self._attributes = attributes
        self.media_id = entry_id
        self.id: int = int(attributes["id"])
        self.type: str = "characters"
        self.name: str = data["canonicalName"]
        self.description: str = data["description"]
        self.role: Optional[str] = role
        self.slug: str = data["slug"]
        self.mal_id: int = int(data["malId"])

    @property
    def image(self) -> Image:
        return Image(self._attributes["image"])

    @property
    def created_at(self) -> Optional[datetime]:
        """When a character got added in Kitu DB"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        """Last time a character got updated"""
        try:
            return datetime.strptime(
                self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None
