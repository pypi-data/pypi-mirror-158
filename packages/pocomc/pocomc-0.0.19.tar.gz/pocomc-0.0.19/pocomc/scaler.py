from typing import Union, List

import numpy as np

from pocomc.input_validation import assert_array_float, assert_array_within_interval


class Reparameterise:
    def __init__(self,
                 ndim: int,
                 bounds: Union[np.ndarray, list] = None,
                 periodic: List[int] = None,
                 reflective: List[int] = None,
                 scale: bool = True,
                 diagonal: bool = True):
        """
        Function that reparameterises the model using change-of-variables parameter transformations.

        Parameters
        ----------
        ndim : int
            Dimensionality of sampling problem
        bounds : array or list or None
            Parameter bounds
        periodic : list
            List of indices corresponding to parameters with periodic boundary conditions
        reflective : list
            List of indices corresponding to parameters with periodic boundary conditions
        scale : bool
            Rescale parameters to zero mean and unit variance (default is true)
        diagonal : bool
            Use diagonal transformation (i.e. ignore covariance) (default is true)
        """
        self.ndim = ndim

        if bounds is None:
            bounds = np.full((self.ndim, 2), np.nan)
        elif len(bounds) == 2 and not np.shape(bounds) == (2, 2):
            bounds = np.tile(np.array(bounds, dtype=np.float32).reshape(2, 1), self.ndim).T
        assert_array_float(bounds)

        self.low = bounds.T[0]
        self.high = bounds.T[1]

        self.periodic = periodic
        self.reflective = reflective

        self.mu = None
        self.sigma = None
        self.cov = None
        self.L = None
        self.Linv = None
        self.logdetL = None
        self.scale = scale
        self.diagonal = diagonal

        self._create_masks()

    def apply_boundary_conditions(self, x: np.ndarray):
        """
        Apply boundary conditions (i.e. periodic or reflective) to input.
        TODO add short description.
        
        Parameters
        ----------
        x : np.ndarray
            Input array
        
        Returns
        -------
        Transformed input
        """
        if (self.periodic is None) and (self.reflective is None):
            return x
        elif self.periodic is None:
            return self._apply_reflective_boundary_conditions(x)
        elif self.reflective is None:
            return self._apply_periodic_boundary_conditions(x)
        else:
            return self._apply_reflective_boundary_conditions(self._apply_periodic_boundary_conditions(x))

    def _apply_periodic_boundary_conditions(self, x: np.ndarray):
        """
        Apply periodic boundary conditions to input.
        TODO add short description.
        
        Parameters
        ----------
        x : np.ndarray
            Input array
        
        Returns
        -------
        Transformed input.
        """
        if self.periodic is not None:
            x = x.copy()
            for i in self.periodic:
                for j in range(len(x)):
                    while x[j, i] > self.high[i]:
                        x[j, i] = self.low[i] + x[j, i] - self.high[i]
                    while x[j, i] < self.low[i]:
                        x[j, i] = self.high[i] + x[j, i] - self.low[i]
        return x

    def _apply_reflective_boundary_conditions(self, x: np.ndarray):
        """
        Apply reflective boundary conditions to input.
        TODO add short description.
        
        Parameters
        ----------
        x : np.ndarray
            Input array
        
        Returns
        -------
        Transformed input.
        """
        if self.reflective is not None:
            x = x.copy()
            for i in self.reflective:
                for j in range(len(x)):
                    while x[j, i] > self.high[i]:
                        x[j, i] = self.high[i] - x[j, i] + self.high[i]
                    while x[j, i] < self.low[i]:
                        x[j, i] = self.low[i] + self.low[i] - self.x[j, i]

        return x

    def fit(self, x: np.ndarray):
        """
        Learn mean and standard deviation using for rescaling.
        
        Parameters
        ----------
        x : np.ndarray
            Input data used for training.
        """
        assert_array_within_interval(x, self.low, self.high)

        u = self._forward(x)
        self.mu = np.mean(u, axis=0)
        if self.diagonal:
            self.sigma = np.std(u, axis=0)
        else:
            self.cov = np.cov(u.T)
            self.L = np.linalg.cholesky(self.cov)
            self.Linv = np.linalg.inv(self.L)
            self.logdetL = np.linalg.slogdet(self.L)[1]

    def forward(self, x: np.ndarray):
        """
        Forward transformation (both logit for bounds and affine for all parameters).

        Parameters
        ----------
        x : np.ndarray
            Input data
        Returns
        -------
        u : np.ndarray
            Transformed input data
        """
        assert_array_within_interval(x, self.low, self.high)

        u = self._forward(x)
        if self.scale:
            u = self._forward_affine(u)

        return u

    def inverse(self, u: np.ndarray):
        """
        Inverse transformation (both logit^-1 for bounds and affine for all parameters).

        Parameters
        ----------
        u : np.ndarray
            Input data
        Returns
        -------
        x : np.ndarray
            Transformed input data
        logdetJ : np.array
            Logarithm of determinant of Jacobian matrix transformation.
        """
        if self.scale:
            x, logdetJ = self._inverse_affine(u)
            x, logdetJ_prime = self._inverse(x)
            logdetJ += logdetJ_prime
        else:
            x, logdetJ = self._inverse(u)

        return x, logdetJ

    def _forward(self, x: np.ndarray):
        """
        Forward transformation (only logit for bounds).

        Parameters
        ----------
        x : np.ndarray
            Input data
        Returns
        -------
        u : np.ndarray
            Transformed input data
        """
        u = np.empty(x.shape)
        u[:, self.mask_none] = self._forward_none(x)
        u[:, self.mask_left] = self._forward_left(x)
        u[:, self.mask_right] = self._forward_right(x)
        u[:, self.mask_both] = self._forward_both(x)

        return u

    def _inverse(self, u: np.ndarray):
        """
        Inverse transformation (only logit^-1 for bounds).

        Parameters
        ----------
        u : np.ndarray
            Input data
        Returns
        -------
        x : np.ndarray
            Transformed input data
        logdetJ : np.array
            Logarithm of determinant of Jacobian matrix transformation.
        """
        x = np.empty(u.shape)
        J = np.empty(u.shape)

        x[:, self.mask_none], J[:, self.mask_none] = self._inverse_none(u)
        x[:, self.mask_left], J[:, self.mask_left] = self._inverse_left(u)
        x[:, self.mask_right], J[:, self.mask_right] = self._inverse_right(u)
        x[:, self.mask_both], J[:, self.mask_both] = self._inverse_both(u)

        logdetJ = np.array([np.linalg.slogdet(Ji * np.identity(len(Ji)))[1] for Ji in J])

        return x, logdetJ

    def _forward_affine(self, x: np.ndarray):
        """
        Forward affine transformation.

        Parameters
        ----------
        x : np.ndarray
            Input data
        Returns
        -------
        Transformed input data
        """
        if self.diagonal:
            return (x - self.mu) / self.sigma
        else:
            return np.array([np.dot(self.Linv, xi - self.mu) for xi in x])

    def _inverse_affine(self, u: np.ndarray):
        """
        Inverse affine transformation.

        Parameters
        ----------
        u : np.ndarray
            Input data
        Returns
        -------
        x : np.ndarray
            Transformed input data
        J : np.ndarray
            Diagonal of Jacobian matrix.
        """
        if self.diagonal:
            J = self.sigma
            logdetJ = np.linalg.slogdet(J * np.identity(len(J)))[1]
            return self.mu + self.sigma * u, logdetJ * np.ones(len(u))
        else:
            x = self.mu + np.array([np.dot(self.L, ui) for ui in u])
            return x, self.logdetL * np.ones(len(u))

    def _forward_left(self, x: np.ndarray):
        """
        Forward transformation for bounded parameters (only low).

        Parameters
        ----------
        x : np.ndarray
            Input data
        Returns
        -------
        Transformed input data
        """
        return np.log(x[:, self.mask_left] - self.low[self.mask_left])

    def _inverse_left(self, u: np.ndarray):
        """
        Inverse transformation for bounded parameters (only low).

        Parameters
        ----------
        u : np.ndarray
            Input data
        Returns
        -------
        x : np.ndarray
            Transformed input data
        J : np.array
            Diagonal of Jacobian matrix.
        """
        p = np.exp(u[:, self.mask_left])

        return p + self.low[self.mask_left], p

    def _forward_right(self, x: np.ndarray):
        """
        Forward transformation for bounded parameters (only high).

        Parameters
        ----------
        x : np.ndarray
            Input data
        Returns
        -------
        Transformed input data
        """
        return np.log(self.high[self.mask_right] - x[:, self.mask_right])

    def _inverse_right(self, u: np.ndarray):
        """
        Inverse transformation for bounded parameters (only high).

        Parameters
        ----------
        u : np.ndarray
            Input data
        Returns
        -------
        x : np.ndarray
            Transformed input data
        J : np.array
            Diagonal of Jacobian matrix.
        """
        p = np.exp(u[:, self.mask_right])

        return self.high[self.mask_right] - p, p

    def _forward_both(self, x: np.ndarray):
        """
        Forward transformation for bounded parameters (both low and high).

        Parameters
        ----------
        x : np.ndarray
            Input data
        Returns
        -------
        Transformed input data
        """
        p = (x[:, self.mask_both] - self.low[self.mask_both]) / (self.high[self.mask_both] - self.low[self.mask_both])

        return np.log(p / (1 - p))

    def _inverse_both(self, u: np.ndarray):
        """
        Inverse transformation for bounded parameters (both low and high).

        Parameters
        ----------
        u : np.ndarray
            Input data
        Returns
        -------
        x : np.ndarray
            Transformed input data
        J : np.array
            Diagonal of Jacobian matrix.
        """
        p = np.exp(-np.logaddexp(0, -u[:, self.mask_both]))
        x = p * (self.high[self.mask_both] - self.low[self.mask_both]) + self.low[self.mask_both]
        J = (self.high[self.mask_both] - self.low[self.mask_both]) * p * (1.0 - p)
        return x, J

    def _forward_none(self, x:np.ndarray):
        """
        Forward transformation for unbounded parameters (this does nothing).

        Parameters
        ----------
        x : np.ndarray
            Input data
        Returns
        -------
        u : np.ndarray
            Transformed input data
        """
        return x[:, self.mask_none]

    def _inverse_none(self, u:np.ndarray):
        """
        Inverse transformation for unbounded parameters (this does nothing).

        Parameters
        ----------
        u : np.ndarray
            Input data
        Returns
        -------
        x : np.ndarray
            Transformed input data
        logdetJ : np.array
            Logarithm of determinant of Jacobian matrix transformation.
        """
        return u[:, self.mask_none], np.ones(u.shape)[:, self.mask_none]

    def _create_masks(self):
        """
        Create parameter masks for bounded parameters
        """

        self.mask_left = np.zeros(self.ndim, dtype=bool)
        self.mask_right = np.zeros(self.ndim, dtype=bool)
        self.mask_both = np.zeros(self.ndim, dtype=bool)
        self.mask_none = np.zeros(self.ndim, dtype=bool)

        # TODO: Do this more elegantly, it's a shame
        for i in range(self.ndim):
            if np.isnan(self.low[i]) and np.isnan(self.high[i]):
                self.mask_none[i] = True
                self.mask_left[i] = False
                self.mask_right[i] = False
                self.mask_both[i] = False
            elif np.isnan(self.low[i]) and not np.isnan(self.high[i]):
                self.mask_none[i] = False
                self.mask_left[i] = False
                self.mask_right[i] = True
                self.mask_both[i] = False
            elif not np.isnan(self.low[i]) and np.isnan(self.high[i]):
                self.mask_none[i] = False
                self.mask_left[i] = True
                self.mask_right[i] = False
                self.mask_both[i] = False
            else:
                self.mask_none[i] = False
                self.mask_left[i] = False
                self.mask_right[i] = False
                self.mask_both[i] = True
