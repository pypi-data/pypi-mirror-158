# coding=utf-8
# Copyright 2022 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for model."""

from typing import Any

from absl.testing import absltest
from absl.testing import parameterized
import jax
from jax import numpy as jnp
import numpy as np
from praxis import base_layer
from praxis import decoder_utils
from praxis import py_utils
from praxis import test_utils
from praxis.layers import models

NestedMap = py_utils.NestedMap
BaseHParams = base_layer.BaseLayer.HParams
instantiate = base_layer.instantiate

RANDOM = base_layer.RANDOM
DECODE_CACHE = base_layer.DECODE_CACHE


class MockLM(base_layer.BaseLayer):

  class HParams(BaseHParams):
    """Associated hyper-params for this layer class.

    Attributes:
      logits: results returned by extend_step(), of shape [max step, batch size,
        vocab size].
    """
    logits: Any = None

  def setup(self) -> None:
    p = self.hparams
    self.logits = jnp.array(p.logits, dtype=jnp.float32)

  def __call__(self, *args: Any, **kwargs: Any) -> None:
    self.put_variable(DECODE_CACHE, 'time_step', 0)

  def extend_step(
      self,
      inputs: Any,
      segment_pos: Any,
  ) -> Any:
    del inputs
    ret = NestedMap()
    time_step = self.get_variable(DECODE_CACHE, 'time_step')
    ret.logits = self.logits.at[time_step].get()
    self.put_variable(DECODE_CACHE, 'time_step', time_step + 1)
    return ret

  def transform_decode_state(self, transform_fn):
    """Transforms all decode state variables based on transform_fn."""
    batch_dim = -1
    time_dim = -1
    new_state = transform_fn(
        self.get_variable(DECODE_CACHE, 'time_step'), batch_dim, time_dim)
    self.update_decode_state('time_step', new_state)


class LanguageModelTest(test_utils.TestCase):

  def _run_decode(self, decoder_p, logits, input_batch):
    p = models.LanguageModel.HParams(
        name='mock_lm',
        decoder=decoder_p.clone(),
        lm=MockLM.HParams(logits=logits))
    lang_model = instantiate(p)
    theta = NestedMap(lm=NestedMap())
    # We fix seed to 9 to get the desired prefix lengths below.
    prng_key = jax.random.PRNGKey(seed=9)
    results, _ = lang_model.apply(
        theta,
        input_batch,
        rngs={RANDOM: prng_key},
        method=lang_model.decode,
        mutable=[DECODE_CACHE])
    _, results = results
    return results

  @parameterized.parameters([True, False])
  def test_base_case(self, fprop_for_prefix):
    p = models.LanguageModel.HParams().decoder
    p.seqlen = 3
    p.min_prefix_len = 1
    p.fprop_for_prefix = fprop_for_prefix
    if fprop_for_prefix:
      p.max_decode_steps = 2
    logits = [
        [
            [0, 1, 0, 0],
        ],
        [
            [0, 0, 0, 1],
        ],
    ]
    # We use full paddings to force prefix lengths to be 0 (since it is capped
    # at the lengths of input ids.
    input_batch = NestedMap(
        ids=jnp.array([[11, 12, 13, 14, 15]], dtype=jnp.int32),
        paddings=jnp.array([[0, 1, 1, 1, 1]], dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[1]], dtype=np.int32))
    # Decoding starts at 1 from input.ids, then each step uses argmax from the
    # provided logits, which are 1 and 3.
    if fprop_for_prefix:
      self.assertArraysEqual(
          results.output_ids,
          np.array([[[11, 1, 3, 0, 0, 0, 0]]], dtype=np.int32))
    else:
      self.assertArraysEqual(results.output_ids,
                             np.array([[[11, 1, 3]]], dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[3]], dtype=np.int32))

  def test_flat_beam_search_no_prefix(self):
    length_norm_alpha = 0.8
    p = models.FlatBeamSearchHParams(
        beam_size=4, eos_id=4, seqlen=4, length_norm_alpha=length_norm_alpha)
    logits = [
        [
            [2, 3, 1, 5, 0],  #  Top4: 3, 1, 0, 2
            [2, 3, 1, 5, 0],
            [2, 3, 1, 5, 0],
            [2, 3, 1, 5, 0],
        ],
        [
            [2, 3, 4, 1, 55],
            [25, 4, 3, 2, 1],
            [0, 0, 0, 0, 0],
            [1, 2, 26, 4, 5],
        ],
        # The last step doesn't matter as seqlen = 4 and flat beam search will
        # add EOS to the last step.
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[1, 0, 0, 0, 9]], dtype=jnp.int32),
        paddings=jnp.ones(shape=(1, 5), dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)
    # Decoding starts from the last element from input.ids, then each step uses
    # beam search from the provided logits.
    self.assertArraysEqual(
        results.output_ids,
        np.array([[[9, 3, 4, 0], [9, 1, 0, 4], [9, 2, 2, 4], [9, 3, 2, 4]]],
                 dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[3, 4, 4, 4]], dtype=np.int32))

    def length_norm(length):
      return decoder_utils.length_norm(np.array(length - 1), length_norm_alpha)

    # Get scores from output_ids sequence [3, 4], [1, 0], [2, 2] and [3, 2].
    self.assertArraysEqual(
        results.scores,
        np.array([[(5 + 55), (3 + 25), (1 + 26), (5 + 4)]], dtype=np.float32) /
        length_norm(results.decode_lengths))

  @parameterized.parameters([True, False])
  def test_prefix(self, fprop_for_prefix):
    p = models.LanguageModel.HParams().decoder
    p.seqlen = 5
    p.min_prefix_len = 2
    p.fprop_for_prefix = fprop_for_prefix
    if fprop_for_prefix:
      p.max_decode_steps = 3
    logits = [
        [
            [0, 1, 0, 0, 0, 0],  # argmax=1
        ],
        [
            [0, 0, 0, 1, 0, 0],  # argmax=3
        ],
        [
            [0, 0, 0, 0, 1, 0],  # argmax=4
        ],
        [
            [0, 0, 0, 0, 0, 1],  # argmax=5
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[11, 12, 13, 14, 15]], dtype=jnp.int32),
        paddings=jnp.array([[0., 0., 1., 1., 1.]], dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[2]], dtype=np.int32))
    # We copy prefix of length 2 from input.ids, so the first argmax
    # from logits is unused. Remaining 3 ids are from argmax.
    if fprop_for_prefix:
      self.assertArraysEqual(
          results.output_ids,
          np.array([[[11, 12, 1, 3, 4, 0, 0, 0]]], dtype=np.int32))
      self.assertArraysEqual(
          results.prefix_ids,
          np.array([[[11, 12, 0, 0, 0, 0, 0, 0]]], dtype=np.int32))
    else:
      self.assertArraysEqual(results.output_ids,
                             np.array([[[11, 12, 3, 4, 5]]], dtype=np.int32))
      self.assertArraysEqual(results.prefix_ids,
                             np.array([[[11, 12, 0, 0, 0]]], dtype=np.int32))

    self.assertArraysEqual(results.decode_lengths,
                           np.array([[5]], dtype=np.int32))

  def test_eos_terminate(self):
    p = models.LanguageModel.HParams().decoder
    p.seqlen = 6
    p.min_prefix_len = 0
    p.eos_id = 2
    logits = [
        [
            [0, 0, 0, 0, 1],  # argmax=4
        ],
        [
            [0, 0, 1, 0, 0],  # argmax=2
        ],
        [
            [0, 0, 0, 1, 0],  # argmax=3
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[11, 13]], dtype=jnp.int32),
        paddings=jnp.ones(shape=(1, 2), dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[0]], dtype=np.int32))
    # Decoding terminates after step 2 when eos_id=2 is encountered.
    self.assertArraysEqual(results.output_ids,
                           np.array([[[11, 4, 2, 0, 0, 0]]], dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[3]], dtype=np.int32))

  def test_eos_independent(self):
    p = models.LanguageModel.HParams().decoder
    p.seqlen = 5
    p.min_prefix_len = 0
    p.eos_id = 2
    logits = [
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],  # argmax=[4, 3]
        ],
        [
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1],  # argmax=[2, 4]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],  # argmax=[3, 2]
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[11, 13], [12, 14]], dtype=jnp.int32),
        paddings=jnp.ones(shape=(2, 2), dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[0], [0]], dtype=np.int32))
    # EOS termination are row independent: row 0 terminates at step 2 while
    # row 1 terminates at step 3.
    self.assertArraysEqual(
        results.output_ids,
        np.array([[[11, 4, 2, 0, 0]], [[12, 3, 4, 2, 0]]], dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[3], [4]], dtype=np.int32))

  def test_prefix_and_eos(self):
    p = models.LanguageModel.HParams().decoder
    p.seqlen = 5
    p.min_prefix_len = 0
    p.eos_id = 2
    logits = [
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],  # argmax=[4, 3, 3]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0],  # argmax=[3, 4, 2]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],  # argmax=[3, 2, 3]
        ],
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],  # argmax=[4, 4, 3]
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[11, 13, 15], [12, 14, 16], [20, 30, 40]],
                      dtype=jnp.int32),
        paddings=jnp.zeros(shape=(3, 3), dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)
    # This is fixed by the prng seed provided.
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[2], [1], [0]], dtype=np.int32))
    # Row 0 copies 2 ids from the input as prefix, and continues without
    # ever hitting EOS. Row 1 and 2 only copies the first id from the input,
    # and continues until EOS is found.
    self.assertArraysEqual(
        results.output_ids,
        np.array([[[11, 13, 3, 3, 4]], [[12, 3, 4, 2, 0]], [[20, 3, 2, 0, 0]]],
                 dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[5], [4], [3]], dtype=np.int32))

  def test_prefix_and_eos_fprop_for_prefix(self):
    p = models.LanguageModel.HParams().decoder
    p.seqlen = 7
    p.max_decode_steps = 4
    p.min_prefix_len = 0
    p.eos_id = 2
    p.fprop_for_prefix = True
    logits = [
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],  # argmax=[4, 3, 3]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0],  # argmax=[3, 4, 2]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],  # argmax=[3, 2, 3]
        ],
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],  # argmax=[4, 4, 3]
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[11, 13, 15], [12, 14, 16], [20, 30, 40]],
                      dtype=jnp.int32),
        paddings=jnp.array([[0, 0, 1], [0, 1, 1], [0, 1, 1]], dtype=jnp.int32),
        prefix_lengths=jnp.array([2, 1, 1], dtype=jnp.int32),
    )
    results = self._run_decode(p, logits, input_batch)
    # This is fixed by the prng seed provided.
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([2, 1, 1], dtype=np.int32))
    # Row 0 copies 2 ids from the input as prefix, and continues without
    # ever hitting EOS. Row 1 and 2 only copies the first id from the input,
    # and continues until EOS is found.
    # The prefix is right aligned to the generated sequence.
    self.assertArraysEqual(
        results.output_ids,
        np.array([[[11, 13, 4, 3, 3, 4, 0]], [[12, 3, 4, 2, 0, 0, 0]],
                  [[20, 3, 2, 0, 0, 0, 0]]],
                 dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[6], [4], [3]], dtype=np.int32))

  def test_prefix_has_eos(self):
    p = models.LanguageModel.HParams().decoder
    p.seqlen = 4
    p.min_prefix_len = 0
    p.eos_id = 2
    logits = [
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],  # argmax=3
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],  # argmax=4
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],  # argmax=[3, 2]
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[2, 2, 2], [2, 2, 2]], dtype=jnp.int32),
        paddings=jnp.zeros(shape=(2, 3), dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)
    # This is fixed by the prng seed provided.
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[3], [1]], dtype=np.int32))
    # Row 0 copies the first 3 ids, and does not terminate even though these
    # ids are EOS. Row 1 copies the first EOS from ids, and uses argmax for the
    # remaining 3.
    self.assertArraysEqual(
        results.output_ids,
        np.array([[[2, 2, 2, 3]], [[2, 3, 4, 2]]], dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[4], [4]], dtype=np.int32))

  def test_max_decode_steps(self):
    p = models.LanguageModel.HParams().decoder
    p.seqlen = 5
    p.min_prefix_len = 0
    p.eos_id = 2
    p.max_decode_steps = 2
    logits = [
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],  # argmax=[4, 3, 3]
        ],
        [
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],  # argmax=[2, 4, 4]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],  # argmax=[3, 4, 3]
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[11, 13, 15], [12, 14, 16], [20, 30, 40]],
                      dtype=jnp.int32),
        paddings=jnp.zeros(shape=(3, 3), dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)
    # This is fixed by the prng seed provided.
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[2], [1], [0]], dtype=np.int32))
    # Row 0 has prefix length 2, and hit EOS after decode for one step, so it
    # stops. Row 1 has prefix length 1, and hit max decode steps of 2, so it
    # stops at 3 decoded ids. Row 2 has prefix length 0, and stops after
    # hitting the max decode step of 2, ending with 2 decoded ids.
    # Note that logically prefix length 1 and 0 are equivalent, because
    # decoding always starts with the fixed first ids (BOS in practice), the
    # only difference is how they affect the counting of max_decode_steps.
    self.assertArraysEqual(
        results.output_ids,
        np.array([[[11, 13, 2, 0, 0]], [[12, 3, 4, 0, 0]], [[20, 3, 0, 0, 0]]],
                 dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[3], [3], [2]], dtype=np.int32))
    # softmax on logits of [0, 0, 0, 0, 1] reproduces:
    # [-1.904833   -1.904833   -1.904833   -1.904833   -0.90483296]
    self.assertAllClose(
        results.logprobs,
        np.array([[[1., -0.904832, -0.904832, 1., 1.]],
                  [[1., -0.904832, -0.904832, 1., 1.]],
                  [[1., -0.904832, 1., 1., 1.]]],
                 dtype=np.float32))

  @parameterized.parameters(
      (1),
      (2),
  )
  def test_sample_decoding_prefix_and_eos(self, k):
    p = models.SampleDecoderHParams(
        seqlen=5,
        min_prefix_len=0,
        eos_id=2,
        num_samples=2,
        k=k,
        temperature=0.5)
    logits = [
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],  # argmax=[4, 3, 3]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0],  # argmax=[3, 4, 2]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],  # argmax=[3, 2, 3]
        ],
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],  # argmax=[4, 4, 3]
        ],
    ]
    sample_logits = jnp.repeat(jnp.array(logits), axis=1, repeats=2)
    input_batch = NestedMap(
        ids=jnp.array([[11, 13, 15], [12, 14, 16], [20, 30, 40]],
                      dtype=jnp.int32),
        paddings=jnp.zeros(shape=(3, 3), dtype=jnp.float32),
    )
    results = self._run_decode(p, sample_logits, input_batch)

    # This is fixed by the prng seed provided.
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[2, 2], [1, 1], [0, 0]], dtype=np.int32))
    # Row 0 copies 2 ids from the input as prefix, and continues without
    # ever hitting EOS. Row 1 and 2 only copies the first id from the input,
    # and continues until EOS is found.
    if k == 1:
      self.assertArraysEqual(
          results.output_ids,
          np.array([[[11, 13, 3, 3, 4], [11, 13, 3, 3, 4]],
                    [[12, 3, 4, 2, 0], [12, 3, 4, 2, 0]],
                    [[20, 3, 2, 0, 0], [20, 3, 2, 0, 0]]],
                   dtype=np.int32))
    else:
      # Gumbel noise will make some difference between samples.
      self.assertArraysEqual(
          results.output_ids,
          np.array([[[11, 13, 3, 3, 4], [11, 13, 3, 3, 4]],
                    [[12, 3, 4, 2, 0], [12, 3, 0, 2, 0]],
                    [[20, 3, 2, 0, 0], [20, 3, 2, 0, 0]]],
                   dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[5, 5], [4, 4], [3, 3]], dtype=np.int32))

  @parameterized.parameters(
      (1),
      (2),
  )
  def test_sample_decoding_prefix_and_eos_fprop_for_prefix(self, k):
    p = models.SampleDecoderHParams(
        fprop_for_prefix=True,
        seqlen=7,
        max_decode_steps=4,
        min_prefix_len=0,
        eos_id=2,
        num_samples=2,
        k=k,
        temperature=0.5)
    logits = [
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],  # argmax=[4, 3, 3]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0],  # argmax=[3, 4, 2]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],  # argmax=[3, 2, 3]
        ],
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],  # argmax=[4, 4, 3]
        ],
    ]
    sample_logits = jnp.repeat(jnp.array(logits), axis=1, repeats=2)
    input_batch = NestedMap(
        ids=jnp.array([[11, 13, 15], [12, 14, 16], [20, 30, 40]],
                      dtype=jnp.int32),
        paddings=jnp.zeros(shape=(3, 3), dtype=jnp.float32),
        prefix_lengths=jnp.array([2, 1, 1], dtype=jnp.int32),
    )
    results = self._run_decode(p, sample_logits, input_batch)

    # This is fixed by the prng seed provided.
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([2, 1, 1], dtype=np.int32))
    # Row 0 copies 2 ids from the input as prefix, and continues without
    # ever hitting EOS. Row 1 and 2 only copies the first id from the input,
    # and continues until EOS is found.
    if k == 1:
      self.assertArraysEqual(
          results.output_ids,
          np.array([[[11, 13, 4, 3, 3, 4, 0], [11, 13, 4, 3, 3, 4, 0]],
                    [[12, 3, 4, 2, 0, 0, 0], [12, 3, 4, 2, 0, 0, 0]],
                    [[20, 3, 2, 0, 0, 0, 0], [20, 3, 2, 0, 0, 0, 0]]],
                   dtype=np.int32))
    else:
      # Gumbel noise will make some difference between samples.
      self.assertArraysEqual(
          results.output_ids,
          np.array([[[11, 13, 4, 3, 3, 4, 0], [11, 13, 0, 3, 3, 4, 0]],
                    [[12, 3, 4, 2, 0, 0, 0], [12, 3, 4, 2, 0, 0, 0]],
                    [[20, 3, 2, 0, 0, 0, 0], [20, 3, 2, 0, 0, 0, 0]]],
                   dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[6, 6], [4, 4], [3, 3]], dtype=np.int32))

  def test_sample_decoding_prefix_and_eos_sample_equal_one(self):
    p = models.SampleDecoderHParams(
        seqlen=5,
        min_prefix_len=0,
        eos_id=2,
        num_samples=1,
        k=2,
        temperature=0.5)
    logits = [
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],  # argmax=[4, 3, 3]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0],  # argmax=[3, 4, 2]
        ],
        [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],  # argmax=[3, 2, 3]
        ],
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],  # argmax=[4, 4, 3]
        ],
    ]
    input_batch = NestedMap(
        ids=jnp.array([[11, 13, 15], [12, 14, 16], [20, 30, 40]],
                      dtype=jnp.int32),
        paddings=jnp.zeros(shape=(3, 3), dtype=jnp.float32),
    )
    results = self._run_decode(p, logits, input_batch)

    # This is fixed by the prng seed provided.
    self.assertArraysEqual(results.prefix_lengths,
                           np.array([[2], [1], [0]], dtype=np.int32))
    # Row 0 copies 2 ids from the input as prefix, and continues without
    # ever hitting EOS. Row 1 and 2 only copies the first id from the input,
    # and continues until EOS is found.
    self.assertArraysEqual(
        results.output_ids,
        np.array([[[11, 13, 3, 3, 4]], [[12, 3, 4, 2, 0]], [[20, 3, 2, 0, 0]]],
                 dtype=np.int32))
    self.assertArraysEqual(results.decode_lengths,
                           np.array([[5], [4], [3]], dtype=np.int32))


if __name__ == '__main__':
  absltest.main()
