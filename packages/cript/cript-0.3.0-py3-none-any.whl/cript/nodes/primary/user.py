from logging import getLogger

from beartype import beartype

from cript.nodes import Base


logger = getLogger(__name__)


class User(Base):
    """
    Object representing a CRIPT user.

    Note: A user cannot be created or modified using the SDK.
          This object is for read-only purposes only.
    """

    node_type = "primary"
    node_name = "User"
    slug = "user"
    list_name = "users"

    @beartype
    def __init__(
        self,
        username: str = None,
        email: str = None,
        orcid_id: str = None,
        groups=None,
        public: bool = False,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.username = username
        self.email = email
        self.orcid_id = orcid_id
        self.groups = groups if groups else []
        self.public = public
        self.created_at = None
        self.updated_at = None
