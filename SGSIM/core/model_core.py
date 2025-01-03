import numpy as np
from . import filter_engine
from .model_config import ModelConfig
from ..motion import signal_analysis

class ModelCore(ModelConfig):
    """
    This class allows to
        calculate properties required in fitting to or simulating ground motions
        i.e., variances, FAS, CE, zero crossing, and local extrema of the stochastic model
    """
    def __init__(self, npts: int, dt: float,
                 mdl_type: str = 'beta_single',
                 wu_type: str = 'linear', zu_type: str = 'linear',
                 wl_type: str = 'linear', zl_type: str = 'linear'):
        super().__init__(npts, dt, mdl_type, wu_type, zu_type, wl_type, zl_type)

    def get_stats(self):
        """
        The evolutionary statistics of the stochastic model using Power Spectral Density (PSD)
        Ignoring the modulating function and the unit-variance White noise

        wu, zu: upper angular frequency and damping ratio
        wl, zl: lower angular frequency and damping ratio
        freq: angular frequency up to Nyq.

        statistics:
            variance :     variance
            variance_dot:  variance 1st derivative
            variance_2dot: variance 2nd derivative
            variance_bar:  variance 1st integral
            variance_2bar: variance 2nd integral
        """
        self.variance, self.variance_dot, self.variance_2dot, self.variance_bar, self.variance_2bar = filter_engine.get_stats(self.wu, self.zu, self.wl, self.zl, self.freq)
        return self

    def get_fas(self):
        """
        The Fourier amplitude spectrum (FAS) of the stochastic model using PSD
        """
        self.fas = filter_engine.get_fas(self.mdl, self.wu, self.zu, self.wl, self.zl, self.freq)
        return self.fas

    def get_ce(self):
        """
        The Cumulative energy of the stochastic model.
        """
        self.ce = signal_analysis.get_ce(self.dt, self.mdl)
        return self.ce

    def get_mle_ac(self):
        """
        The mean cumulative number of local extream (peaks and valleys)
        of the acceleration model
        without considering the modulation function
        """
        mle_rate_ac = (np.sqrt(self.variance_2dot / self.variance_dot) / (2 * np.pi))
        self.mle_ac = np.cumsum(mle_rate_ac) * self.dt
        return self.mle_ac

    def get_mle_vel(self):
        """
        The mean cumulative number of local extream (peaks and valleys)
        of the velocity model
        without considering the modulation function
        """
        mle_rate_vel = (np.sqrt(self.variance_dot / self.variance) / (2 * np.pi))
        self.mle_vel = np.cumsum(mle_rate_vel) * self.dt
        return self.mle_vel

    def get_mle_disp(self):
        """
        The mean cumulative number of local extream (peaks and valleys)
        of the displacement model
        without considering the modulation function
        """
        mle_rate_disp = (np.sqrt(self.variance / self.variance_bar) / (2 * np.pi))
        self.mle_disp = np.cumsum(mle_rate_disp) * self.dt
        return self.mle_disp

    def get_mzc_ac(self):
        """
        The mean cumulative number of zero crossing (up and down)
        of the acceleration model
        without considering the modulation function
        """
        mzc_rate_ac = (np.sqrt(self.variance_dot / self.variance) / (2 * np.pi))
        self.mzc_ac = np.cumsum(mzc_rate_ac) * self.dt
        return self.mzc_ac

    def get_mzc_vel(self):
        """
        The mean cumulative number of zero crossing (up and down)
        of the velocity model
        without considering the modulation function
        """
        mzc_rate_vel = (np.sqrt(self.variance / self.variance_bar) / (2 * np.pi))
        self.mzc_vel = np.cumsum(mzc_rate_vel) * self.dt
        return self.mzc_vel

    def get_mzc_disp(self):
        """
        The mean cumulative number of zero crossing (up and down)
        of the displacement model
        without considering the modulation function
        """
        mzc_rate_disp = (np.sqrt(self.variance_bar / self.variance_2bar) / (2 * np.pi))
        self.mzc_disp = np.cumsum(mzc_rate_disp) * self.dt
        return self.mzc_disp

    def get_pmnm_ac(self):
        """
        The mean cumulative number of positive-minima and negative maxima
        of the acceleration model without considering the modulation function.
        """
        pmnm_rate_ac = (np.sqrt(self.variance_2dot / self.variance_dot) -
                        np.sqrt(self.variance_dot / self.variance)) / (4 * np.pi)
        self.pmnm_ac = np.cumsum(pmnm_rate_ac) * self.dt
        return self.pmnm_ac

    def get_pmnm_vel(self):
        """
        The mean cumulative number of positive-minima and negative maxima
        of the velocity model without considering the modulation function.
        """
        pmnm_rate_vel = (np.sqrt(self.variance_dot / self.variance) -
                        np.sqrt(self.variance / self.variance_bar)) / (4 * np.pi)
        self.pmnm_vel = np.cumsum(pmnm_rate_vel) * self.dt
        return self.pmnm_vel

    def get_pmnm_disp(self):
        """
        The mean cumulative number of positive-minima and negative maxima
        of the displacement model without considering the modulation function.
        """
        pmnm_rate_disp = (np.sqrt(self.variance / self.variance_bar) -
                          np.sqrt(self.variance_bar / self.variance_2bar)) / (4 * np.pi)
        self.pmnm_disp = np.cumsum(pmnm_rate_disp) * self.dt
        return self.pmnm_disp

    def get_properties(self):
        """
        Calculate all properties of the stochastic model
        """
        self.get_stats()
        self.get_fas()
        self.get_ce()
        self.get_mle_ac()
        self.get_mle_vel()
        self.get_mle_disp()
        self.get_mzc_ac()
        self.get_mzc_vel()
        self.get_mzc_disp()
        self.get_pmnm_ac()
        self.get_pmnm_vel()
        self.get_pmnm_disp()
        return self
