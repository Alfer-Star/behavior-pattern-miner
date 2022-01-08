from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.objects.petri_net.obj import PetriNet

def getCostFunctionParameter(net: PetriNet):
    model_cost_function = dict()
    sync_cost_function = dict()
    for t in net.transitions:
        # if the label is not None, we have a visible transition
        if t.label is not None:
        # associate cost 1000 to each move-on-model associated to visible transitions
            model_cost_function[t] = 1000
            # associate cost 0 to each move-on-log
            sync_cost_function[t] = 0
        else:
        # associate cost 1 to each move-on-model associated to hidden transitions
            model_cost_function[t] = 1

    parameters = {}
    parameters[alignments.Variants.VERSION_STATE_EQUATION_A_STAR.value.Parameters.PARAM_MODEL_COST_FUNCTION] = model_cost_function
    parameters[alignments.Variants.VERSION_STATE_EQUATION_A_STAR.value.Parameters.PARAM_SYNC_COST_FUNCTION] = sync_cost_function
    return parameters