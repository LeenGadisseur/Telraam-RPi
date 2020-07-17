from distutils.core import setup, Extension
import numpy as np

module = Extension("backEstimation", sources = ["backEstimationModule.c"])

setup(	name="backgroundEstimation", 
	version = "1.0",
	description = "This packages is for the backEstimationModule.",
	include_dirs = [np.get_include()],
	ext_modules = [module])
