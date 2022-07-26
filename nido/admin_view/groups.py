#  Nido groups.py
#  Copyright (C) 2022 John Arnold
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import (
    Blueprint,
    abort,
    current_app,
    render_template,
    redirect,
    request,
    url_for,
)
from nido.auth import login_required, get_user_id, get_community_id, is_admin

from nido.models import Group

posit_bp = Blueprint("posit", __name__)


@posit_bp.route("/edit-groups")
@login_required
def edit_groups():
    community_id = get_community_id()
    if not is_admin(community_id, get_user_id()):
        return abort(403)
    groups = current_app.Session.query(Group).filter_by(community_id=community_id).all()
    return render_template("edit-groups.html", groups=groups)


@posit_bp.post("/edit-groups")
@login_required
def edit_groups_post():
    delete_id = request.form.get("delete_id")
    if delete_id:
        delend = current_app.Session.get(Group, int(delete_id))
        if delend.role.parent_id is None:
            pass
        else:
            current_app.Session.delete(delend)
            current_app.Session.commit()
    return redirect(url_for(".edit_groups"))
