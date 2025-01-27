from dataclasses import dataclass
from typing import List, Optional, Union

from openeo.internal.jupyter import render_component
from openeo.rest.models.federation_extension import FederationExtension


@dataclass(frozen=True)
class Link:
    """
    Container for (web) link data, used throughout the openEO API,
    to point to alternate representations, a license, extra detailed information, and more.
    """

    rel: str
    href: str
    type: Optional[str] = None
    title: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(rel=data["rel"], href=data["href"], type=data.get("type"), title=data.get("title"))

    # TODO: add _html_repr_ for Jupyter integration


class CollectionListingResponse(list):
    """
    Container for collection metadata listing received from a ``GET /collections`` request.

    This object mimics a list of collection metadata dictionaries,
    which was the original return API of :py:meth:`~openeo.rest.connection.Connection.list_collections()`,
    but now also includes additional metadata like links and extensions.

    :param data: response data from a ``GET /collections`` request
    """

    __slots__ = ["_data"]

    def __init__(self, data: dict):
        self._data = data
        # Mimic original list of collection metadata dictionaries
        super().__init__(data["collections"])

    def _repr_html_(self):
        return render_component(component="collections", data=self)

    @property
    def links(self) -> List[Link]:
        """Get links from collections response."""
        return [Link.from_dict(d) for d in self._data.get("links", [])]

    @property
    def ext_federation(self) -> FederationExtension:
        """Accessor for federation extension data."""
        return FederationExtension(self._data)
