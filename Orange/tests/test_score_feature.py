import unittest

import numpy as np

from Orange.data import Table, Domain
from Orange.preprocess import score
from Orange import preprocess


class FeatureScoringTest(unittest.TestCase):

    def setUp(self):
        self.zoo = Table("zoo")  # disc. features, disc. class
        self.housing = Table("housing")  # cont. features, cont. class

    def test_info_gain(self):
        scorer = score.InfoGain()
        correct = [0.79067, 0.71795, 0.83014, 0.97432, 0.46970]
        np.testing.assert_almost_equal([scorer(a, self.zoo) for a in range(5)],
                                       correct, decimal=5)

    def test_gain_ratio(self):
        scorer = score.GainRatio()
        correct = [0.80351, 1.00000, 0.84754, 1.00000, 0.59376]
        np.testing.assert_almost_equal([scorer(a, self.zoo) for a in range(5)],
                                       correct, decimal=5)

    def test_gini(self):
        scorer = score.Gini()
        correct = [0.11893, 0.10427, 0.13117, 0.14650, 0.05973]
        np.testing.assert_almost_equal([scorer(a, self.zoo) for a in range(5)],
                                       correct, decimal=5)

    def test_classless(self):
        classless = Table(Domain(self.zoo.domain.attributes),
                          self.zoo[:, 0:-1])
        scorers = [score.Gini(), score.InfoGain(), score.GainRatio()]
        for scorer in scorers:
            with self.assertRaises(ValueError):
                scorer(0, classless)

    def test_wrong_class_type(self):
        scorers = [score.Gini(), score.InfoGain(), score.GainRatio()]
        for scorer in scorers:
            with self.assertRaises(ValueError):
                scorer(0, self.housing)

        with self.assertRaises(ValueError):
            score.Chi2(2, self.housing)
        with self.assertRaises(ValueError):
            score.ANOVA(2, self.housing)
        score.UnivariateLinearRegression(2, self.housing)

    def test_chi2(self):
        nrows, ncols = 500, 5
        X = np.random.randint(4, size=(nrows, ncols))
        y = 10 + (-3*X[:, 1] + X[:, 3]) // 2
        data = preprocess.Discretize()(Table(X, y))
        scorer = score.Chi2()
        sc = [scorer(a, data) for a in range(ncols)]
        self.assertTrue(np.argmax(sc) == 1)

    def test_anova(self):
        nrows, ncols = 500, 5
        X = np.random.rand(nrows, ncols)
        y = 4 + (-3*X[:, 1] + X[:, 3]) // 2
        data = Table(X, y)
        scorer = score.ANOVA()
        sc = [scorer(a, data) for a in range(ncols)]
        self.assertTrue(np.argmax(sc) == 1)

    def test_regression(self):
        nrows, ncols = 500, 5
        X = np.random.rand(nrows, ncols)
        y = (-3*X[:, 1] + X[:, 3]) / 2
        data = Table(X, y)
        scorer = score.UnivariateLinearRegression()
        sc = [scorer(a, data) for a in range(ncols)]
        self.assertTrue(np.argmax(sc) == 1)
