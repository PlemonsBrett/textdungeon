from project_two import __version__


# A sanity test to ensure poetry builder is working
def test_version():
    assert __version__ == "0.1.0"
