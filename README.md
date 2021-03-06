# Generation of stretched single qubit gates for Richardson error extrapolation
## Contents
* Abstract
* Description
* Reference
* Members

**_How to use ?_**

We wrote a function to modify the instruction schedule map (inst_map), which is a lookup table for translating "Quantum Gates" in the circuits to the pulse schedule used to drive qubits. 
The python function is put in "functions" folder and we demonstrate the 1-Qubit Randomized Benchmarking and checking the linearity of qubit dynamics. 
You can go through the following jupyter notebook in the repository.

The data of linearity and RB experiments are open, you can retrieve the data by using the "Job ID" shown in the notebook.
The calibration data of IBMQ_Armonk on Sep 28 (RB) and Sep 30 (Linearity) are also available in the folder "Backend_Calibration_data"
1. [1-Qubit Randomized Benchmarking with different stretch factors](Demo_RB_on_ibmq_armonk.ipynb)
2. [Checking linearity of the qubit dynamics](Demo_Linearity_on_ibmq_armonk.ipynb)
3. [Function for modifying instruction schedule map](functions/backend_modification.py)

## Abstract
With QiskitPulse we can create custom quantum gates that is not provided by a backend. One of easy and practical examples is single qubit gates. In this project, we generate u1, u2, u3 gates with different stretch factor using QiskitPulse and run randomized benchmarking algorithm to estimate systematic error.

## Description
In IBM Quantum backends u1, u2, u3, id, cx gates are provided as basis gates and any quantum circuit can be decomposed into this set. Two main sources of the error of those quantum gates are incoherent error due to limited T1 and T2 times and imperfection of pulse calibration.

Given T1 and T2 are time invariant, you can eliminate this noise with Richardson error extrapolation [1]:

![](https://user-images.githubusercontent.com/39517270/92420700-e31b2800-f1af-11ea-814f-d522e77df3e0.png)

Here we calibrate underlying quantum gates with different stretch factor c_i. In the case of circuit composed of single qubit gates, you need to calibrate u1, u2, u3 gates. Because these gates are generated from x90 or y90 pulse with virtual z rotation (pre-processing of pulse envelope), you just need to calibrate x90 and y90 pulses.

This is partially demonstrated by the joint work of U Chicago with IBM by using QiskitPulse [2]. In this paper they rescaled pulse amplitude with respect to the target rotation angle, but here we need to rescale both pulse duration and amplitude while the rotation angle remain unchanged, i.e. keeping the area under curve of your pulse envelope for different stretch factors.

### Workflow

Finally, we ran a single qubit randomized benchmarking algorithm with stretched x90 and y90 pulses. Below is our workflow.
1. Check the linearity

    We run the rabi oscillation for each pulses amplitude and fitting the data to get the rabi frequencies for each amplitude. After that, we can check the qubit dynamics is linear in the regime we did the experiments.
    * running the rabi oscillation on IBMQ_Armonk quantum computer
    ![Rabi Oscillation for each pulse amplitude](figures/Oscillation.jpg)
    
    * fitting the data and get the rabi frequency for each pulse amplitude.
    ![real device (ibmq_armonk) result](figures/linearity.jpg)
    
    The result is linear in the region that pulse amplitude between 0.3 and 1. Since the qubit dynamics is linear in this regime, we can easily modify the duration and the pulse to keep the pulse area.
2. Modify the instruction schedule map

    There's a look up table in device backend that qiskit transpile the quantum into microwave pulses implement in superconductor quantum computer through the mapping in this table. We change the mapping in the table so we can running the same quantum circuit in different stretch factor of pulse duration.
    
    * Example pulses for u2 gate, and u3 gate in the ibmq_armonk device, respectively.
    
    ![Pulse for u2/u3gate](figures/ex_gate_pulse.png)
    
    * Example for stretching the duration of the pulse and the pulse amplitude change to keep the area invariant.
    
    ![example of stretching the pu2/u3ulse](figures/ex_stretch_gate.png)
    
3. Randomized Benchmarking on different stretch factors
    We ran the RB for some different stretch factor c_i and used Richardson error extrapolation to calculate the noise free result.
    ![RB_result](figures/Richardson_RB.jpg)
    
    The blue line in the figure has stretch factor 1 (the origin result without changing). stretch factor is 2 for yellow line and 3 for green line. The red line is calculate by the first order Richardson Extrapolation and purple line is from second order. 
    
    The result is interesting that the error mitigated data is perfectly. 
    There's no decay or the decay rate is quite small that the population is remain in the ground state.
    IBMQ_Armonk Backend has only one qubit is a important reason, one qubit device means there's no correlation to other qubits in the device so we don't need to consider the noise come from them.
    Another reason is some noise on the Quantum Computer should independent of gate time. No matter what the stretch factor is, the strength of this kind of noise doesn't change. 
### Slides for presentation
[The slides for presentation in Qiskit Hackathon Taiwan by Bai-Siang](IBMQ_Hackathon_Oral_%2318_.pdf)

## Reference:
[1] [Error mitigation extends the computational reach of a noisy quantum processor](https://www.nature.com/articles/s41586-019-1040-7)

[2] [Optimized Quantum Compilation for Near-Term Algorithms with OpenPulse](https://arxiv.org/abs/2004.11205)

## Members (name in alphabetical order)
* Hsu,Ming-Chien @HuberyMing
* Lin,Tzu-Lu @supergravity
* Yeh,Bai-Siang @itsuka021
* Yang,tai-hsuan @xiaotai-yang

* Qiskit Coach: Naoki Kanazawa @nkanazawa1989 - Slack @Naoki Kanazawa Email knzwnao@jp.ibm.com
