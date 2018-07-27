#import tensorflow as tf
import math

from .node import Node, RealValuedNode

class UnknownMutationException(Exception):
    pass

def map_to_np_phenotype(genes, params, real_valued=False):

    nodes = []
    for _ in range(params.n_inputs):
        nodes.append(Node(None, [], is_input=True))

    chunk_size = params.function_set.max_arity + 1

    for i in range(params.n_nodes):
        node_genes = genes[i * chunk_size : (i * chunk_size) + chunk_size]

        function, arity = params.function_set[node_genes[0]]

        if real_valued:
            nodes.append(RealValuedNode(node_genes[0], node_genes[1:], arity))
        else:
            nodes.append(Node(function, node_genes[1:], arity))

    for gene in genes[-params.n_outputs:]:
        nodes.append(Node(None, [gene], is_output=True))

    return nodes

def map_to_tf_phenotype(genes, params):
    nodes = []
    for _ in range(params.n_inputs):
        nodes.append(Node(tf.constant, [], is_input=True))

    chunk_size = params.function_set.max_arity + 1

    for i in range(params.n_nodes):
        node_genes = genes[i * chunk_size : (i * chunk_size) + chunk_size]

        function, arity = params.function_set[node_genes[0]]

        nodes.append(Node(function, node_genes[1:], arity))

    for gene in genes[-params.n_outputs:]:
        nodes.append(Node(tf.Variable, [gene], is_output=True))

    return nodes

def active_paths(nodes, real_valued=False):
    stack = []
    paths = []
    path = []

    # get all the output nodes
    index = len(nodes) - 1

    for node in reversed(nodes):
        if node.is_output:
            stack.append((index, node))
            index -= 1
        else: # output nodes should be only at the end of nodes list
            break

    while len(stack) > 0:
        index, current_node = stack.pop()

        not_first_output_node = len(path) != 0

        if current_node.is_output and not_first_output_node:
            paths.append(list(reversed(path)))
            path = []

        path.append(index)

        if not current_node.is_output and not current_node.is_input:
            if real_valued:
                nested = [[math.floor(i), math.ceil(i)] for i in current_node.inputs[:current_node.arity]]
                inputs = [x for y in nested for x in y]
            else:
                inputs = current_node.inputs[:current_node.arity]
        else:
            inputs = current_node.inputs

        for input_index in reversed(inputs):
            stack.append((input_index, nodes[input_index]))

    if len(path) != 0:
        paths.append(list(reversed(path)))

    return paths


def join_lists(x, y):
    # this abhorent method is used in individual comparison, so the
    # reduce would run few ms faster
    return x + y

def round_cma_vector(cma_vector, bounds):
    """ convert float vector from CMA-ES to valid genes vector """
    processed_genes = []
    for number, bound in zip(cma_vector, bounds):
        gene = int(round(number))
        if gene > bound:
            gene = bound
        if gene < 0:
            gene = 0
        processed_genes.append(gene)
    return processed_genes

def handle_invalid_decorator(fun):
    """ Decorates the inner cost_function, so it returns fitness_of_invalid value
    defined in parameters in case of ValueError """
    def wrapper(*args, **kwargs):
        new_args = list(args)
        cost_function = args[2]
        params = args[3]
        def wrapped_cost_function(*args, **kwargs):
            try:
                return cost_function(*args, **kwargs)
            except ValueError as e:
                return params.fitness_of_invalid
        new_args[2] = wrapped_cost_function
        return fun(*new_args, **kwargs)
    return wrapper
