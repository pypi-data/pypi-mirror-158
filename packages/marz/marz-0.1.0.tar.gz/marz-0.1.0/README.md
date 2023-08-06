# marz

Marz is a **m**easurement **a**nd **r**eset simplification routine that collapses measure + reset pairs of operations on into a single measurement followed by a control-x gate.  This optimization is suitable for use on IBM Quantum systems, where the reset operation is performed by a measurement followed by a conditional x-gate: 

<img width="1180" alt="Screen Shot 2022-07-11 at 14 40 37" src="https://user-images.githubusercontent.com/1249193/178335187-a8d24aaa-935b-4931-b090-5f87ccb38a0f.png">

`marz` therefore saves one measurement per operation pair.  Because measurements are the operations with the largest error rates on IBM Quantum systems, and each measurement takes ~2 CNOT gates worth of time, this optimization reduces error rates and can reduce the duration of quantum circuits (dephasing) that impliment qubit reuse.  It can also eliminate the dreaded `BufferOverflow` error where measurement results are beinging generated faster than they can be stored.


## Usage

Marz is really easy to use as it has a single function:

```python

import marz

optim_circ = marz.collapse_meas_reset_pairs(input_circ)
```

One can also pass a list of circuits and get a list of optimized circuits back.

