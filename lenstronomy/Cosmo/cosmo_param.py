

class CosmoParam(object):
    """
    class that handles the cosmology relevant parameters
    """

    def __init__(self, cosmo_type=None, mass_scaling=False, kwargs_fixed={}, num_scale_factor=1):
        """


        :param sampling: bool, if True, activates time-delay parameters
        :param D_dt_init: initial guess of time-delay distance (Mpc)
        :param D_dt_sigma: initial uncertainty
        :param D_dt_lower: lower bound
        :param D_dt_upper: upper bound
        """
        if cosmo_type is None:
            self._Ddt_sampling = False
        elif cosmo_type == 'D_dt':
            self._Ddt_sampling = True
        else:
            raise ValueError("cosmo_type %s is not supported!" % cosmo_type)
        self._cosmo_type = cosmo_type
        self._mass_scaling = mass_scaling
        self._num_scale_factor = num_scale_factor
        self._kwargs_fixed = kwargs_fixed

    def getParams(self, args, i):
        """

        :param args:
        :param i:
        :return:
        """
        kwargs_cosmo = {}
        if self._Ddt_sampling is True:
            if self._cosmo_type == 'D_dt':
                if 'D_dt' not in self._kwargs_fixed:
                    kwargs_cosmo['D_dt'] = args[i]
                    i += 1
        if self._mass_scaling is True:
            if 'scale_factor' not in self._kwargs_fixed:
                kwargs_cosmo['scale_factor'] = args[i: i + self._num_scale_factor]
                i += self._num_scale_factor
        return kwargs_cosmo, i

    def setParams(self, kwargs_cosmo):
        """

        :param kwargs:
        :return:
        """
        args = []
        if self._Ddt_sampling is True:
            if self._cosmo_type == 'D_dt':
                if 'D_dt' not in self._kwargs_fixed:
                    args.append(kwargs_cosmo['D_dt'])
        if self._mass_scaling is True:
            if 'scale_factor' not in self._kwargs_fixed:
                for i in range(self._num_scale_factor):
                    args.append(kwargs_cosmo['scale_factor'][i])
        return args

    def param_init(self, kwargs_mean):
        """

        :param kwargs_mean:
        :return:
        """
        mean = []
        sigma = []
        if self._Ddt_sampling is True:
            if self._cosmo_type == 'D_dt':
                if 'D_dt' not in self._kwargs_fixed:
                    mean.append(kwargs_mean['D_dt'])
                    sigma.append(kwargs_mean['D_dt_sigma'])
        if self._mass_scaling is True:
            if 'scale_factor' not in self._kwargs_fixed:
                for i in range(self._num_scale_factor):
                    mean.append(kwargs_mean['scale_factor'][i])
                    sigma.append(kwargs_mean['scale_factor_sigma'][i])
        return mean, sigma

    def num_param(self):
        """

        :return:
        """
        num = 0
        list = []
        if self._Ddt_sampling is True:
            if self._cosmo_type == 'D_dt':
                if 'D_dt' not in self._kwargs_fixed:
                    num += 1
                    list.append('D_dt')
        if self._mass_scaling is True:
            if 'scale_factor' not in self._kwargs_fixed:
                num += self._num_scale_factor
                for i in range(self._num_scale_factor):
                    list.append('scale_factor')
        return num, list
