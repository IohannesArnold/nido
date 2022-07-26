import pytest
from nido.models import Community, Residence, User, Group
from sqlalchemy.exc import IntegrityError


def test_disjoint_residence_community_and_user_community(db):
    c1 = Community(name="Com1", country="US")
    c2 = Community(name="Com2", country="US")
    u = User(personal_name="Lise", family_name="Wittering")
    r = Residence(
        street="235 Larry Trail", locality="El Paso", postcode="79934", region="TX"
    )

    db.add(c1)
    db.add(c2)
    c1.members.append(u)
    r.community = c2
    u.residences.append(r)

    db.add(u)
    with pytest.raises(IntegrityError):
        db.commit()


def test_position_max_size(session):
    g = session.get(Group, 1)
    u2 = session.get(User, 2)

    with pytest.raises(Exception):
        g.members.append(u2)


def test_position_min_size(session):
    g = session.get(Group, 1)
    u1 = session.get(User, 1)

    with pytest.raises(Exception):
        g.members.remove(u1)
