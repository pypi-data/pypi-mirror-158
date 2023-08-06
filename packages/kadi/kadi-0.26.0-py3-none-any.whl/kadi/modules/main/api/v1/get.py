# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask_login import current_user
from flask_login import login_required
from marshmallow.fields import DateTime

import kadi.lib.constants as const
from kadi import __version__
from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.api.utils import status
from kadi.lib.conversion import normalize
from kadi.lib.db import escape_like
from kadi.lib.licenses.schemas import LicenseSchema
from kadi.lib.permissions.utils import get_object_roles
from kadi.lib.tags.schemas import TagSchema
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.collections.models import Collection
from kadi.modules.groups.models import Group
from kadi.modules.main.utils import get_licenses as _get_licenses
from kadi.modules.main.utils import get_tags as _get_tags
from kadi.modules.records.models import Record
from kadi.modules.templates.models import Template


@bp.get("")
@login_required
@status(200, "Return the API endpoints.")
def index():
    """Get all base API endpoints."""
    endpoints = {
        "collections": url_for("api.get_collections"),
        "groups": url_for("api.get_groups"),
        "info": url_for("api.get_info"),
        "licenses": url_for("api.get_licenses"),
        "records": url_for("api.get_records"),
        "roles": url_for("api.get_resource_roles"),
        "tags": url_for("api.get_tags"),
        "templates": url_for("api.get_templates"),
        "trash": url_for("api.get_trash"),
        "users": url_for("api.get_users"),
    }
    return json_response(200, endpoints)


@bp.get("/info")
@login_required
@status(200, "Return the information about the Kadi instance.")
def get_info():
    """Get information about the Kadi instance."""
    info = {"version": __version__}
    return json_response(200, info)


@bp.get("/roles")
@login_required
@status(200, "Return the resource roles and permissions.")
def get_resource_roles():
    """Get all possible roles and corresponding permissions of all resources."""
    roles = {}

    for model in [Record, Collection, Template, Group]:
        object_name = model.__tablename__
        roles[object_name] = get_object_roles(object_name)

    return json_response(200, roles)


@bp.get("/tags")
@login_required
@paginated
@qparam(
    "filter", parse=normalize, description="A query to filter the tags by their name."
)
@qparam(
    "type",
    default=None,
    description="A resource type to limit the tags to. One of ``record`` or"
    " ``collection``.",
)
@status(200, "Return a paginated list of tags, sorted by name in ascending order.")
def get_tags(page, per_page, qparams):
    """Get all tags of resources the current user can access."""
    paginated_tags = _get_tags(
        filter_term=qparams["filter"], resource_type=qparams["type"]
    ).paginate(page, per_page, False)

    data = {
        "items": TagSchema(many=True).dump(paginated_tags.items),
        **create_pagination_data(
            paginated_tags.total, page, per_page, "api.get_tags", **qparams
        ),
    }

    return json_response(200, data)


@bp.get("/licenses")
@login_required
@paginated
@qparam(
    "filter",
    parse=normalize,
    description="A query to filter the licenses by their title or name.",
)
@status(200, "Return a paginated list of licenses, sorted by name in ascending order.")
def get_licenses(page, per_page, qparams):
    """Get all licenses."""
    paginated_licenses = _get_licenses(filter_term=qparams["filter"]).paginate(
        page, per_page, False
    )

    data = {
        "items": LicenseSchema(many=True).dump(paginated_licenses.items),
        **create_pagination_data(
            paginated_licenses.total, page, per_page, "api.get_licenses", **qparams
        ),
    }

    return json_response(200, data)


@bp.get("/trash")
@login_required
@scopes_required("misc.manage_trash")
@paginated
@qparam(
    "filter",
    parse=normalize,
    description="A query to filter the deleted resources by their identifier.",
)
@status(
    200,
    "Return a paginated list of deleted resources, sorted by deletion date in"
    " descending order.",
)
def get_trash(page, per_page, qparams):
    """Get all deleted resources the current user created.

    Only the ``id`` and ``identifier`` of the resources are returned. Additionally, each
    resource contains its resource type (``type``), its deletion date (``deleted_at``)
    as well as endpoints to restore (``_actions.restore``) or purge (``_actions.purge``)
    the resource.
    """
    queries = []

    for model in [Record, Collection, Template, Group]:
        resources_query = model.query.filter(
            model.identifier.ilike(f"%{escape_like(qparams['filter'])}%"),
            model.user_id == current_user.id,
            model.state == const.MODEL_STATE_DELETED,
        ).with_entities(
            model.id,
            model.identifier,
            model.last_modified.label("deleted_at"),
            db.literal(model.__tablename__).label("type"),
            db.literal(str(model.Meta.pretty_name)).label("pretty_type"),
        )
        queries.append(resources_query)

    paginated_resources = (
        queries[0]
        .union(*queries[1:])
        .order_by(db.desc("deleted_at"))
        .paginate(page, per_page, False)
    )

    items = []
    for resource in paginated_resources.items:
        item = {
            "id": resource.id,
            "identifier": resource.identifier,
            "type": resource.type,
            "pretty_type": resource.pretty_type,
            "deleted_at": DateTime().serialize("deleted_at", resource),
            "_actions": {
                "restore": url_for(f"api.restore_{resource.type}", id=resource.id),
                "purge": url_for(f"api.purge_{resource.type}", id=resource.id),
            },
        }

        items.append(item)

    data = {
        "items": items,
        **create_pagination_data(
            paginated_resources.total, page, per_page, "api.get_trash"
        ),
    }

    return json_response(200, data)
