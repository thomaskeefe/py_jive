import unittest
import numpy as np

from jive.jive.lin_alg_fun import *
from jive.jive.ajive_fig2 import *
from jive.jive.jive import *


class JiveDecomposition(unittest.TestCase):
    """
    Make sure all JIVE constraints work.
    """
    def setUp(self):
        """
        Sample data and compute JIVE estimates
        """

        # sample platonic data
        seed = 23423
        self.X_obs, self.X_joint, self.X_indiv, self.X_noise, \
        self.Y_obs, self.Y_joint, self.Y_indiv, self. Y_noise = generate_data_ajive_fig2(seed)

        self.blocks = [self.X_obs, self.Y_obs]
        wedin_bound = True
        show_scree_plot = False

        # compute JIVE decomposition
        jive = Jive(self.blocks, wedin_bound, show_scree_plot)
        jive.set_signal_ranks([2, 3])
        self.jive_estimates = jive.get_jive_estimates()

        self.K = len(self.blocks)
        self.dimensions = [self.blocks[k].shape[1] for k in range(self.K)]
        self.joint_rank = 1
        self.individual_ranks = [1, 2]

    def test_jive_decoposition(self):
        """
        Check that X = I + J + E for each block
        """
        for k in range(self.K):
            X = self.blocks[k]

            J = self.jive_estimates[k]["joint"]["full"]
            I = self.jive_estimates[k]["individual"]["full"]
            E = self.jive_estimates[k]["noise"]

            residual = X - (J + I + E)
            self.assertTrue(np.allclose(residual, 0))

    def test_joint_rank(self):
        """
        Check JIVE has the correct joint rank
        """
        # TODO: this might be a stochastic test -- maybe romeves
        rank_estimate = self.jive_estimates[0]['joint']['rank']

        self.assertTrue(self.joint_rank == rank_estimate)

    def test_individual_ranks(self):
        """
        Check JIVE has the correct individual rank
        """
        for k in range(self.K):
            rank_estimate = self.jive_estimates[k]['individual']['rank']
            rank_true = self.individual_ranks[k]

            self.assertTrue(rank_true == rank_estimate)

    def test_individual_space_SVD(self):
        """
        Check the SVD of the I matrix is correct
        """
        for k in range(self.K):
            I = self.jive_estimates[k]["individual"]["full"]
            U = self.jive_estimates[k]["individual"]["U"]
            D = self.jive_estimates[k]["individual"]["D"]
            V = self.jive_estimates[k]["individual"]["V"]

            # compare SVD reconstruction to I matrix
            svd_reconstruction = np.dot(U, np.dot(np.diag(D), V.T))
            residual = I - svd_reconstruction

            self.assertTrue(np.allclose(residual, 0))

    def test_joint_space_SVD(self):
        """
        Check the SVD of the J matrix is correct
        """
        for k in range(self.K):
            J = self.jive_estimates[k]["joint"]["full"]
            U = self.jive_estimates[k]["joint"]["U"]
            D = self.jive_estimates[k]["joint"]["D"]
            V = self.jive_estimates[k]["joint"]["V"]

            # compare SVD reconstruction to I matrix
            svd_reconstruction = np.dot(U, np.dot(np.diag(D), V.T))
            residual = J - svd_reconstruction

            self.assertTrue(np.allclose(residual, 0))



if __name__ == '__main__':
    unittest.main()