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
from flask import current_app
from flask import redirect
from flask import render_template
from flask import send_file
from flask_login import current_user
from flask_login import login_required

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.conversion import strip
from kadi.lib.db import escape_like
from kadi.lib.db import get_class_by_tablename
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.utils import get_user_roles
from kadi.lib.storage.misc import create_misc_storage
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import User
from kadi.modules.accounts.models import UserState


@bp.get("/users/<int:id>/image", v=None)
@login_required
@internal
def preview_user_image(id):
    """Preview a user's image thumbnail directly in the browser."""
    user = User.query.get_or_404(id)

    if user.is_merged:
        return redirect(
            url_for("api.preview_user_image", id=user.new_user_id), code=301
        )

    if user.image_name:
        storage = create_misc_storage()
        filepath = storage.create_filepath(str(user.image_name))

        if storage.exists(filepath):
            return send_file(
                filepath,
                mimetype="image/jpeg",
                download_name=f"{user.identity.username}.jpg",
            )

    return json_error_response(404)


@bp.get("/users/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=strip)
@qparam("exclude", multiple=True, parse=int)
@qparam("resource_type")
@qparam("resource_id", default=None, parse=int)
def select_users(qparams):
    """Search users in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Note that user
    identities are returned, not users. Therefore, users with multiple identities are
    technically included multiple times.
    """
    excluded_ids = qparams["exclude"]
    resource_type = qparams["resource_type"]
    resource_id = qparams["resource_id"]

    # If applicable, exclude users that already have any role in the specified resource.
    if (
        resource_type in ["record", "collection", "template", "group"]
        and resource_id is not None
    ):
        model = get_class_by_tablename(resource_type)
        resource = model.query.get_active(resource_id)

        if resource is not None and has_permission(
            current_user, "read", resource_type, resource_id
        ):
            user_ids_query = get_user_roles(
                resource_type, object_id=resource_id
            ).with_entities(User.id)
            excluded_ids += [u.id for u in user_ids_query]

    identity_queries = []

    for provider_config in current_app.config["AUTH_PROVIDERS"].values():
        model = provider_config["identity_class"]

        identities_query = (
            model.query.join(User, User.id == model.user_id)
            .filter(
                User.state == UserState.ACTIVE,
                User.id.notin_(excluded_ids),
                db.or_(
                    model.displayname.ilike(f"%{escape_like(qparams['term'])}%"),
                    model.username.ilike(f"%{escape_like(qparams['term'])}%"),
                ),
            )
            .with_entities(
                model.user_id,
                model.username,
                model.displayname.label("displayname"),
                db.literal(str(model.Meta.identity_type["name"])).label("type"),
            )
        )

        identity_queries.append(identities_query)

    paginated_identities = (
        identity_queries[0]
        .union(*identity_queries[1:])
        .order_by("displayname")
        .paginate(qparams["page"], 10, False)
    )

    data = {
        "results": [],
        "pagination": {"more": paginated_identities.has_next},
    }
    for identity in paginated_identities.items:
        data["results"].append(
            {
                "id": identity.user_id,
                "text": f"@{identity.username}",
                "body": render_template(
                    "accounts/snippets/select_user.html",
                    displayname=identity.displayname,
                    username=identity.username,
                    type=identity.type,
                ),
            }
        )

    return json_response(200, data)
