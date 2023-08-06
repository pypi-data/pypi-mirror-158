import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
import spotpy

import definitions
from hydromodel.calibrate.calibrate_ga import calibrate_by_ga
from hydromodel.calibrate.calibrate_sceua import calibrate_by_sceua, SpotSetup
from hydromodel.models.xaj import xaj, uh_gamma, uh_conv
from hydromodel.visual.pyspot_plots import show_calibrate_result


@pytest.fixture()
def basin_area():
    # the area of basin 01013500, unit km2
    # basin_area = 2252.7
    return 1.783


@pytest.fixture()
def warmup_length():
    return 30


@pytest.fixture()
def the_data():
    root_dir = definitions.ROOT_DIR
    # test_data = pd.read_csv(os.path.join(root_dir, "hydromodel", "example", '01013500_lump_p_pe_q.txt'))
    return pd.read_csv(
        os.path.join(root_dir, "hydromodel", "example", "hymod_input.csv"), sep=";"
    )


@pytest.fixture()
def p_and_e(the_data):
    # p_and_e_df = test_data[['prcp(mm/day)', 'petfao56(mm/day)']]
    # three dims: sequence (time), batch (basin), feature (variable)
    # p_and_e = np.expand_dims(p_and_e_df.values, axis=1)
    p_and_e_df = the_data[["rainfall[mm]", "TURC [mm d-1]"]]
    return np.expand_dims(p_and_e_df.values, axis=1)


@pytest.fixture()
def qobs(basin_area, the_data):
    # 1 ft3 = 0.02831685 m3
    ft3tom3 = 2.831685e-2
    # 1 km2 = 10^6 m2
    km2tom2 = 1e6
    # 1 m = 1000 mm
    mtomm = 1000
    # 1 day = 24 * 3600 s
    daytos = 24 * 3600
    # qobs_ = np.expand_dims(test_data[['streamflow(ft3/s)']].values, axis=1)
    # trans ft3/s to mm/day
    # return qobs_ * ft3tom3 / (basin_area * km2tom2) * mtomm * daytos

    qobs_ = np.expand_dims(the_data[["Discharge[ls-1]"]].values, axis=1)
    # trans l/s to mm/day
    return qobs_ * 1e-3 / (basin_area * km2tom2) * mtomm * daytos


@pytest.fixture()
def params():
    # all parameters are in range [0,1]
    return np.tile([0.5], (1, 15))


def test_uh_gamma():
    # repeat for 20 periods and add one dim as feature: time_seq=20, batch=10, feature=1
    routa = np.tile(2.5, (20, 10, 1))
    routb = np.tile(3.5, (20, 10, 1))
    uh = uh_gamma(routa, routb, len_uh=15)
    np.testing.assert_almost_equal(
        uh[:, 0, :],
        np.array(
            [
                [0.0069],
                [0.0314],
                [0.0553],
                [0.0738],
                [0.0860],
                [0.0923],
                [0.0939],
                [0.0919],
                [0.0875],
                [0.0814],
                [0.0744],
                [0.0670],
                [0.0597],
                [0.0525],
                [0.0459],
            ]
        ),
        decimal=3,
    )


def test_uh():
    uh_from_gamma = np.tile(1, (5, 3, 1))
    rf = np.arange(30).reshape(10, 3, 1) / 100
    qs = uh_conv(rf, uh_from_gamma)
    np.testing.assert_almost_equal(
        np.array(
            [
                [0.0000, 0.0100, 0.0200],
                [0.0300, 0.0500, 0.0700],
                [0.0900, 0.1200, 0.1500],
                [0.1800, 0.2200, 0.2600],
                [0.3000, 0.3500, 0.4000],
                [0.4500, 0.5000, 0.5500],
                [0.6000, 0.6500, 0.7000],
                [0.7500, 0.8000, 0.8500],
                [0.9000, 0.9500, 1.0000],
                [1.0500, 1.1000, 1.1500],
            ]
        ),
        qs[:, :, 0],
        decimal=3,
    )


def test_xaj(p_and_e, params, warmup_length):
    qsim = xaj(p_and_e, params, warmup_length=warmup_length)
    np.testing.assert_array_equal(qsim.shape[0], p_and_e.shape[0] - warmup_length)


def test_xaj_mz(p_and_e, params, warmup_length):
    qsim = xaj(p_and_e, params, warmup_length=warmup_length, route_method="MZ")
    np.testing.assert_array_equal(qsim.shape[0], p_and_e.shape[0] - warmup_length)


def test_calibrate_xaj_sceua(p_and_e, qobs, warmup_length):
    calibrate_by_sceua(
        p_and_e,
        qobs,
        warmup_length,
        random_seed=2000,
        rep=5000,
        ngs=7,
        kstop=3,
        peps=0.1,
        pcento=0.1,
    )


def test_show_calibrate_sceua_result(p_and_e, qobs, warmup_length):
    spot_setup = SpotSetup(
        p_and_e, qobs, warmup_length, obj_func=spotpy.objectivefunctions.rmse
    )
    show_calibrate_result(spot_setup, "SCEUA_xaj")
    plt.show()


def test_calibrate_xaj_ga(p_and_e, qobs, warmup_length):
    calibrate_by_ga(
        p_and_e,
        qobs,
        warmup_length,
        run_counts=5,
        pop_num=50,
        cross_prob=0.5,
        mut_prob=0.5,
    )
