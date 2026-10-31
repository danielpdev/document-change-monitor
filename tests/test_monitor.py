from app.core import Monitor


def test_atomic_replacement_retirement_and_history(tmp_path):
    m = Monitor("sqlite:///" + str(tmp_path / "m.sqlite"))
    m.update("policy", "Old thirty day refund")
    assert not m.update("policy", "Old thirty day refund")["changed"]
    assert m.update("policy", "New seven day refund")["version"] == 2
    assert not m.search("thirty") and m.search("seven")[0]["version"] == 2
    m.retire("policy")
    assert not m.search("refund") and len(m.history("policy")) == 2
    assert m.update("policy", "New seven day refund")["version"] == 3
