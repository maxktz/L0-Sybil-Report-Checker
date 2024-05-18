from typing import Literal, Optional, TypedDict

IssuesFilter = Literal["assigned", "created", "mentioned", "subscribed", "repos", "all"]


class PageNumbers(TypedDict):
    prev: Optional[int] = None
    next: Optional[int] = None
    first: Optional[int] = None
    last: Optional[int] = None


class Issue(TypedDict):
    id: int
    node_id: str
    url: str
    repository_url: str
    labels_url: str
    comments_url: str
    events_url: str
    html_url: str
    number: int
    state: str
    title: str
    body: str
    user: dict
    labels: list[dict]
    assignee: dict
    assignees: dict
    milestone: dict
    locked: bool
    active_lock_reason: str
    comments: int
    pull_request: dict
    closed_at: Optional[str]
    created_at: str
    updated_at: str
    repository: dict
    author_association: str
