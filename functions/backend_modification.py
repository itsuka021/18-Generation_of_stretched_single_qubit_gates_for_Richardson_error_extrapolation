from qiskit.ignis.characterization import update_u_gates, get_single_q_pulse
from qiskit.pulse import Drag, Schedule, Play


def mod_inst_map(inst_map_, c_factor, qubits, dri_channel):
    """
    Modify the instruction_schedule_map of the given backend.

    Args:
        inst_map_ (InstMap) : original inst_map you want to modify
        c_factor (float) : stretched factor for pulse duration
        qubits (List) : the qubits you want to modify its pulse
        dri_channel (List) : the list of channel corresponding to the inst)map
    Returns:
        InstMap : modified inst_map
    Notes:
        All of the modifications will directly take effect on your backend unless you get the backend from IBMQ again.
    """

    # you need to check the index of u2_pulse.
    # index [1][1] is for the case that the backend have only one qubit.
    # for other device the index may become [2][1] or something else.
    origin_params_ = []
    for q in qubits:
        q_list = [q]
        u3_pulse = inst_map_.get('u3', q_list, P0=1, P1=1, P2=1).instructions[1][1].pulse
        is_param = getattr(u3_pulse, 'parameters', None)
        if is_param is None:
            origin_params_.append(get_single_q_pulse(inst_map_, q_list)[0])
        else:
            origin_params_.append(u3_pulse.parameters)
    print('Original Parameters')
    print(origin_params_)

    # modify the parameters
    mod_params = []
    for q_i in range(len(qubits)):
        mod_params.append(_tune_param(origin_params_[q_i], c_factor))
    print('Modified Parameters')
    print(mod_params)

    pulses_list = []
    for q_index in qubits:
        x90_sched = Schedule(name='pi2_pulse_qubit_%.d' % q_index)
        x90_sched += Play(Drag(**mod_params[q_index]), dri_channel[qubits.index(q_index)]).shift(0)
        pulses_list.append(x90_sched)
    update_u_gates(mod_params, pulses_list, qubits, inst_map_, dri_channel)

    return mod_params


def _tune_param(params, c1):
    """
    Args:
          params (dict) : Pulse parameters to be modified
          c1 (float) : stretch factor
    Returns:
        dict : parameters after modify

    Examples:
         C1 = 2 = ratio to extend duration

         sigma X pulse
            inst.pulse = Drag(duration=640, amp=(0.647275375+0j), sigma=160, beta=-4.6318738)

            inst.pulse.parameters  = {'duration': 640, 'amp': (0.647275375+0j), 'sigma': 160, 'beta': -4.6318738}
    """
    params['sigma'] = params['sigma'] * c1
    params['amp'] = params['amp'] / c1
    params['duration'] = params['duration'] * c1
    # print(params)
    return params
