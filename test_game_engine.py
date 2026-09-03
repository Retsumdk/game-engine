from game_engine import Arena


def test_spawn_clamps_inside():
    a = Arena(100, 100, seed=1)
    e = a.spawn("player", 150, -20)
    assert e.x == 100 and e.y == 0


def test_move_respects_bounds():
    a = Arena(50, 50, seed=1)
    e = a.spawn("player", 48, 48)
    a.move(e, 10, 10)
    assert e.x == 50 and e.y == 50


def test_collision_detection():
    a = Arena(100, 100, seed=1)
    p = a.spawn("player", 50, 50)
    e = a.spawn("enemy", 52, 50)
    assert a.collides(p, e, 3.0) is True
    far = a.spawn("enemy", 90, 90)
    assert a.collides(p, far, 3.0) is False


def test_deterministic_seed():
    a1 = Arena(100, 100, seed=7)
    a2 = Arena(100, 100, seed=7)
    e1 = a1.random_entity("q")
    e2 = a2.random_entity("q")
    assert (e1.x, e1.y) == (e2.x, e2.y)
