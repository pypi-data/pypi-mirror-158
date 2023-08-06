from __future__ import annotations

import functools
import sys
from typing import Callable

from jax import lax
from jax import numpy as jnp
from jax import vmap
from pytreeclass import treeclass

from kernex.src.base import kernelOperation
from kernex.src.utils import ZIP, ix_, offset_to_padding, roll_view

property = functools.cached_property if sys.version_info.minor > 7 else property


@treeclass
class baseKernelMap(kernelOperation):

    def __post_init__(self):

        if len(self.funcs) == 1:
            self.__call__ = self.__single_call__

        else:
            self.__call__ = self.__multi_call__

    def reduce_map_func(self, func, *args, **kwargs) -> Callable:

        if self.relative:

            def reduce_map_func_callable(view, array):
                return func(roll_view(array[ix_(*view)]), *args, **kwargs)

        else:

            def reduce_map_func_callable(view, array):
                return func(array[ix_(*view)], *args, **kwargs)

        return reduce_map_func_callable

    def __single_call__(self, array, *args, **kwargs):

        padded_array = jnp.pad(array, self.pad_width)
        reduced_func = self.reduce_map_func(self.funcs[0], *args, **kwargs)
        result = vmap(lambda view: reduced_func(view, padded_array))(
            self.views)
        func_shape = result.shape[1:]
        return result.reshape(*self.output_shape, *func_shape)

    def __multi_call__(self, array, *args, **kwargs):

        padded_array = jnp.pad(array, self.pad_width)

        reduced_funcs = tuple(
            self.reduce_map_func(func, *args, **kwargs)
            for func in self.funcs[::-1])

        result = vmap(lambda view: lax.switch(self.func_index_from_view(
            view), reduced_funcs, view, padded_array))(self.views)

        func_shape = result.shape[1:]
        return result.reshape(*self.output_shape, *func_shape)


@treeclass
class kernelMap(baseKernelMap):

    def __init__(self, func_dict, shape, kernel_size, strides, padding,
                 relative):

        super().__init__(func_dict, shape, kernel_size, strides, padding,
                         relative)

    def __call__(self, array, *args, **kwargs):
        return self.__call__(array, *args, **kwargs)


@treeclass
class offsetKernelMap(kernelMap):

    def __init__(self, func_dict, shape, kernel_size, strides, offset,
                 relative):

        self.offset = offset

        super().__init__(func_dict, shape, kernel_size, strides,
                         offset_to_padding(offset, kernel_size), relative)

    @property
    def set_indices(self):
        return tuple(
            jnp.arange(x0, di - xf, si) for di, ki, si, (x0, xf) in ZIP(
                self.shape, self.kernel_size, self.strides, self.offset))

    def __call__(self, array, *args, **kwargs):
        result = self.__call__(array, *args, **kwargs)
        assert result.shape <= array.shape, f"kernel operation output must be scalar. Foud {result.shape}"
        return array.at[ix_(*self.set_indices)].set(result)
