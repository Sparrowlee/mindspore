# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
""" test_tuple_slice """
import numpy as np

import mindspore.ops.operations as P
from mindspore import Tensor
from mindspore.nn import Cell
from ....mindspore_test_framework.mindspore_test import mindspore_test
from ....mindspore_test_framework.pipeline.forward.compile_forward \
    import pipeline_for_compile_forward_ge_graph_for_case_by_case_config
from ....mindspore_test_framework.pipeline.forward.verify_exception \
    import pipeline_for_verify_exception_for_case_by_case_config


class NetWork_1(Cell):
    """ NetWork_1 definition """

    def __init__(self):
        super(NetWork_1, self).__init__()
        self.addN = P.AddN()

    def construct(self, tensor_tuple):
        tensor_tuple_slice0 = tensor_tuple[:]
        tensor_tuple_slice1 = tensor_tuple[:3]
        tensor_tuple_slice2 = tensor_tuple[1:]
        tensor_tuple_slice3 = tensor_tuple[2:5:1]
        sum0 = self.addN(tensor_tuple_slice0)
        sum1 = self.addN(tensor_tuple_slice1)
        sum2 = self.addN(tensor_tuple_slice2)
        sum3 = self.addN(tensor_tuple_slice3)
        ret = sum0 + sum1 + sum2 + sum3
        return ret


class NetWork_2(Cell):
    """ NetWork_2 definition """

    def __init__(self):
        super(NetWork_2, self).__init__()
        self.addN = P.AddN()

    def construct(self, tensor_tuple):
        tensor_tuple_slice0 = tensor_tuple[::-1]
        tensor_tuple_slice1 = tensor_tuple[-1::-1]
        tensor_tuple_slice2 = tensor_tuple[:-4:-1]
        tensor_tuple_slice3 = tensor_tuple[-6:3]
        tensor_tuple_slice4 = tensor_tuple[-1:-6:-2]
        sum0 = self.addN(tensor_tuple_slice0)
        sum1 = self.addN(tensor_tuple_slice1)
        sum2 = self.addN(tensor_tuple_slice2)
        sum3 = self.addN(tensor_tuple_slice3)
        sum4 = self.addN(tensor_tuple_slice4)
        ret = sum0 + sum1 + sum2 + sum3 + sum4
        return ret


class NetWork_3(Cell):
    """ NetWork_3 definition """

    def __init__(self):
        super(NetWork_3, self).__init__()
        self.addN = P.AddN()

    def construct(self, tensor_tuple, start, stop, step=1):
        tensor_tuple_slice0 = tensor_tuple[start:stop:step]
        res = self.addN(tensor_tuple_slice0)
        return res


test_cases = [
    ('SlicePositive', {
        'block': NetWork_1(),
        'desc_inputs': [(Tensor(np.ones([2, 3, 4], np.int32)),
                         Tensor(np.zeros([2, 3, 4], np.int32)),
                         Tensor(np.ones([2, 3, 4], np.int32)),
                         Tensor(np.ones([2, 3, 4], np.int32)),
                         Tensor(np.zeros([2, 3, 4], np.int32)),
                         Tensor(np.ones([2, 3, 4], np.int32)))],
    }),
    ('SliceNegative', {
        'block': NetWork_2(),
        'desc_inputs': [(Tensor(np.ones([2, 3, 4], np.int32)),
                         Tensor(np.zeros([2, 3, 4], np.int32)),
                         Tensor(np.ones([2, 3, 4], np.int32)),
                         Tensor(np.ones([2, 3, 4], np.int32)),
                         Tensor(np.zeros([2, 3, 4], np.int32)),
                         Tensor(np.ones([2, 3, 4], np.int32)))],
    }),
]

test_cases_for_verify_exception = [
    ('SliceStartCross', {
        'block': (NetWork_3(), {'exception': RuntimeError}),
        'desc_inputs': [*(Tensor(np.ones([2, 3, 4], np.int32)),
                          Tensor(np.zeros([2, 3, 4], np.int32)),
                          Tensor(np.ones([2, 3, 4], np.int32)))],
    }),
    ('SliceStepZero', {
        'block': (NetWork_3(), {'exception': RuntimeError}),
        'desc_inputs': [*(Tensor(np.ones([2, 3, 4], np.int32)),
                          Tensor(np.zeros([2, 3, 4], np.int32)),
                          Tensor(np.ones([2, 3, 4], np.int32)))],
    }),
]


@mindspore_test(pipeline_for_compile_forward_ge_graph_for_case_by_case_config)
def test_compile():
    return test_cases


@mindspore_test(pipeline_for_verify_exception_for_case_by_case_config)
def test_check_exception():
    return test_cases_for_verify_exception
