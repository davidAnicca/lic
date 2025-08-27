import pytest
from validator import validate

bounds = {
    "G_MIN": 10,
    "G_MAX": 20,
    "P_MIN": 30,
    "P_MAX": 40,
    "MU_MIN": 0.05,
    "MU_MAX": 0.5,
    "E_MIN": 1,
    "K_MIN": 2,
}


def test_G_outside_bounds():
    errs = validate(5, 35, 0.1, 3, 2, "HPH", bounds)
    assert "Generations number" in errs[0]


def test_P_outside_bounds():
    errs = validate(15, 100, 0.1, 3, 2, "HPH", bounds)
    assert any("Population size" in e for e in errs)


def test_M_not_between_0_and_1():
    errs = validate(15, 35, -0.2, 3, 2, "HPH", bounds)
    assert any("must be strictly between 0 and 1" in e for e in errs)


def test_M_outside_custom_bounds():
    errs = validate(15, 35, 0.9, 3, 2, "HPH", bounds)
    assert any("Mutation" in e and "outside" in e for e in errs)


def test_E_invalid_too_small():
    errs = validate(15, 35, 0.1, 3, 0, "HPH", bounds)
    assert any("Elitism" in e for e in errs)


def test_E_invalid_too_large():
    errs = validate(15, 35, 0.1, 3, 35, "HPH", bounds)
    assert any("Elitism" in e for e in errs)


def test_K_invalid_too_small():
    errs = validate(15, 35, 0.1, 1, 2, "HPH", bounds)
    assert any("Tournament size" in e for e in errs)


def test_K_invalid_too_large():
    errs = validate(15, 35, 0.1, 50, 2, "HPH", bounds)
    assert any("Tournament size" in e for e in errs)


def test_input_hp_not_string():
    errs = validate(15, 35, 0.1, 3, 2, 123, bounds)
    assert any("Input sequence" in e for e in errs)


def test_input_hp_invalid_chars():
    errs = validate(15, 35, 0.1, 3, 2, "ABX", bounds)
    assert any("Input sequence" in e for e in errs)


def test_valid_case_no_errors():
    errs = validate(15, 35, 0.1, 3, 2, "HPHPPH", bounds)
    assert errs == []
