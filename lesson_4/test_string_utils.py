import pytest
from string_utils import StringUtils

@pytest.fixture
def utils():
    return StringUtils()

def test_capitalize(utils):
    assert utils.capitilize("skypro") == "Skypro"
    assert utils.capitilize("Skypro") == "Skypro"
    assert utils.capitilize("s") == "S"
    assert utils.capitilize("") == ""

def test_trim(utils):
    assert utils.trim("   skypro") == "skypro"
    assert utils.trim("skypro") == "skypro"
    assert utils.trim("   ") == ""
    assert utils.trim("") == ""

def test_to_list(utils):
    assert utils.to_list("a,b,c,d") == ["a", "b", "c", "d"]
    assert utils.to_list("1:2:3", ":") == ["1", "2", "3"]
    assert utils.to_list("") == []
    assert utils.to_list(" ") == [" "]

def test_contains(utils):
    assert utils.contains("SkyPro", "S") == True
    assert utils.contains("SkyPro", "U") == False
    assert utils.contains("", "S") == False

def test_delete_symbol(utils):
    assert utils.delete_symbol("SkyPro", "k") == "SyPro"
    assert utils.delete_symbol("SkyPro", "Pro") == "Sky"
    assert utils.delete_symbol("SkyPro", "Z") == "SkyPro"
    assert utils.delete_symbol("", "Z") == ""

def test_starts_with(utils):
    assert utils.starts_with("SkyPro", "S") == True
    assert utils.starts_with("SkyPro", "P") == False
    assert utils.starts_with("", "S") == False

def test_end_with(utils):
    assert utils.end_with("SkyPro", "o") == True
    assert utils.end_with("SkyPro", "y") == False
    assert utils.end_with("", "o") == False

def test_is_empty(utils):
    assert utils.is_empty("") == True
    assert utils.is_empty(" ") == True
    assert utils.is_empty("SkyPro") == False

def test_list_to_string(utils):
    assert utils.list_to_string([1, 2, 3, 4]) == "1, 2, 3, 4"
    assert utils.list_to_string(["Sky", "Pro"]) == "Sky, Pro"
    assert utils.list_to_string(["Sky", "Pro"], "-") == "Sky-Pro"
    assert utils.list_to_string([]) == ""