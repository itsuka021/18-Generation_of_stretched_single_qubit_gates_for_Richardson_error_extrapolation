# Generation of stretched single qubit gates for Richardson error extrapolation
## Abstract
With QiskitPulse you can create custom quantum gates that is not provided by a backend. One of easy and practical examples is single qubit gates. In this project, you generate u1, u2, u3 gates with different stretch factor using QiskitPulse and run randomized benchmarking algorithm to estimate systematic error.

## Description
In IBM Quantum backends u1, u2, u3, id, cx gates are provided as basis gates and any quantum circuit can be decomposed into this set. Two main sources of the error of those quantum gates are incoherent error due to limited T1 and T2 times and imperfection of pulse calibration.

Given T1 and T2 are time invariant, you can eliminate this noise with Richardson error extrapolation [1]:

![https://user-images.githubusercontent.com/39517270/92420700-e31b2800-f1af-11ea-814f-d522e77df3e0.png]
e you need to calibrate underlying quantum gates with different stretch factor c_i. In the case of circuit composed of single qubit gates, you need to calibrate u1, u2, u3 gates. Because these gates are generated from x90 or y90 pulse with virtual z rotation (pre-processing of pulse envelope), you just need to calibrate x90 and y90 pulses.

This is partially demonstrated by the joint work of U Chicago with IBM by using QiskitPulse [2]. In this paper they rescaled pulse amplitude with respect to the target rotation angle, but here we need to rescale both pulse duration and amplitude while the rotation angle remain unchanged, i.e. keeping the area under curve of your pulse envelope for different stretch factors.

[goal1]

Finally you can run a single qubit randomized benchmarking algorithm with your stretched x90 and y90 pulses. If your pulses are well calibrated, you will observe a result like this.

image

[goal2]

What you can investigate (advanced):

As explained above this extrapolation eliminates a noise which is sensitive to the stretching of pulse. By calculating the error per gate from the curve fitting, you can plot gate error over different order n in the equation 2.
On the other hand, the lower bound of error caused by T1 and T2 can be theoretically calculated with utility tool in Qiskit Ignis.
Combining above results, you can infer the required n to eliminate incoherent error of your quantum computing system. Check if there is any difference of n among backends (if you have multiple backend access)?
## Reference:
[1] https://www.nature.com/articles/s41586-019-1040-7
[2] https://arxiv.org/abs/2004.11205

## Members
@supergravity
@itsuka021
@xiaotai-yang
@HuberyMing
Qiskit Coach: @nkanazawa1989 - Slack @Naoki Kanazawa emal knzwnao@jp.ibm.com
