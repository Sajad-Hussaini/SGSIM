import numpy as np
from .domain_config import DomainConfig

class ModelConfig(DomainConfig):
    """
    This class allows to configure time, frequency, and model parametric functions.
    """
    def __init__(self, npts: int, dt: float, modulating,
                 upper_frequency, upper_damping,
                 lower_frequency, lower_damping):
        super().__init__(npts, dt)
        self.mdl_func = modulating
        self.wu_func = upper_frequency
        self.zu_func = upper_damping
        self.wl_func = lower_frequency
        self.zl_func = lower_damping
        (self._mdl, self._wu, self._zu, self._wl, self._zl,
         self.variance, self.variance_dot, self.variance_2dot, self.variance_bar, self.variance_2bar,
         self._ce, self._mle_ac, self._mle_vel, self._mle_disp, self._mzc_ac, self._mzc_vel, self._mzc_disp,
         self._pmnm_ac, self._pmnm_vel, self._pmnm_disp) = np.zeros((20, self.npts))
        self._fas = np.zeros_like(self.freq)

    def _reset_attributes(self):
        """ Reset core model features upon parameters change. """
        self._fas.fill(0.0)
        self._ce.fill(0.0)
        self._mle_ac.fill(0.0)
        self._mle_vel.fill(0.0)
        self._mle_disp.fill(0.0)
        self._mzc_ac.fill(0.0)
        self._mzc_vel.fill(0.0)
        self._mzc_disp.fill(0.0)
        self._pmnm_ac.fill(0.0)
        self._pmnm_vel.fill(0.0)
        self._pmnm_disp.fill(0.0)
        self.variance.fill(0.0)
        self.variance_dot.fill(0.0)
        self.variance_2dot.fill(0.0)
        self.variance_bar.fill(0.0)
        self.variance_2bar.fill(0.0)

    @property
    def mdl(self):
        """ Modulating function """
        return self._mdl

    @mdl.setter
    def mdl(self, params):
        self._mdl[:] = self.mdl_func(self.t, *params)
        self.mdl_params = params
        self._reset_attributes()

    @property
    def wu(self):
        """ Upper dominant frequency """
        return self._wu

    @wu.setter
    def wu(self, params):
        self._wu[:] = self.wu_func(self.t, *params)
        self.wu_params = params
        self._wu *= 2 * np.pi  # Convert to angular frequency
        self._reset_attributes()

    @property
    def wl(self):
        """ Lower dominant frequency """
        return self._wl

    @wl.setter
    def wl(self, params):
        self._wl[:] = self.wl_func(self.t, *params)
        self.wl_params = params
        self._wl *= 2 * np.pi  # Convert to angular frequency
        self._reset_attributes()

    @property
    def zu(self):
        """ Upper damping ratio """
        return self._zu

    @zu.setter
    def zu(self, params):
        self._zu[:] = self.zu_func(self.t, *params)
        self.zu_params = params
        self._reset_attributes()

    @property
    def zl(self):
        """ Lower damping ratio """
        return self._zl

    @zl.setter
    def zl(self, params):
        self._zl[:] = self.zl_func(self.t, *params)
        self.zl_params = params
        self._reset_attributes()