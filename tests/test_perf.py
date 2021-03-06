import pandas as pd
import numpy as np
from pyrsm.perf import calc, gains, lift

np.random.seed(1234)
nr = 100
df = pd.DataFrame()
df["x1"] = np.random.uniform(0, 1, nr)
df["x2"] = 1 - df["x1"]
df["response_prob"] = np.random.uniform(0, 1, nr)
df["response"] = np.where((df["x1"] > 0.5) & (df["response_prob"] > 0.5), "yes", "no")
# df["response"] = np.random.choice(["yes", "no"], nr)


def test_calc():
    ret = calc(df, "response", "yes", "x1", qnt=10)
    assert all(
        ret["cum_resp"] == np.array([6, 14, 20, 27, 29, 30, 30, 30, 30, 30])
    ), "Incorrect calculation of cum_resp with x1"


def test_calc_rev():
    ret = calc(df, "response", "yes", "x2", qnt=10)
    assert all(
        ret["cum_resp"] == np.array([6, 14, 20, 27, 29, 30, 30, 30, 30, 30])
    ), "Incorrect calculation of cum_resp with x2"


def test_gains():
    ret = gains(df, "response", "yes", "x1", qnt=10)
    assert all(
        ret["cum_gains"].values.round(3)
        == np.array([0.0, 0.2, 0.467, 0.667, 0.9, 0.967, 1.0, 1.0, 1.0, 1.0, 1.0])
    ), "Incorrect calculation of cum_gains"


def test_lift():
    ret = lift(df, "response", "yes", "x1", qnt=10)
    assert all(
        ret["cum_lift"].values.round(3)
        == np.array([2.0, 2.333, 2.222, 2.25, 1.933, 1.667, 1.429, 1.25, 1.111, 1.0])
    ), "Incorrect calculation of cum_lift"
