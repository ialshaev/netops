from optparse import Values
import yaml
import graphviz as gv


styles = {
    "graph": {
        "label": "Network Map",
        "fontsize": "16",
        "fontcolor": "white",
        "bgcolor": "#3F3F3F",
        "rankdir": "BT",
    },
    "nodes": {
        "fontname": "Helvetica",
        "shape": "box",
        "fontcolor": "white",
        "color": "#006699",
        "style": "filled",
        "fillcolor": "#006699",
        "margin": "0.4",
    },
    "edges": {
        "style": "dashed",
        "color": "green",
        "arrowhead": "open",
        "fontname": "Courier",
        "fontsize": "14",
        "fontcolor": "white",
    },
}


def apply_styles(graph, styles):
    graph.graph_attr.update(("graph" in styles and styles["graph"]) or {})
    graph.node_attr.update(("nodes" in styles and styles["nodes"]) or {})
    graph.edge_attr.update(("edges" in styles and styles["edges"]) or {})
    return graph


def draw_topology(topology_dict, out_filename="img/topology", style_dict=styles):

    node_list_main = []
    for node in list(topology_dict.keys()):
        node_list_main.append(node)
    print(node_list_main)

    intf_list_main = []
    for node in list(topology_dict.values()):
        intf_list = list(node.keys())
        intf_list_main.append(intf_list)
    print(intf_list_main)

    second_part = []
    for net_node in list(topology_dict.values()):
        for net_node_nested in list(net_node.values()):
            second_part.append(net_node_nested)

    second_part_1half = []
    second_part_2half = []   
    for i in second_part:
        half_one = list(i.keys())
        half_two = list(i.values())
        second_part_1half.append(half_one)
        second_part_2half.append(half_two)

    print(second_part_1half)
    print(second_part_2half)

    
 
    # print(intf_list_main)

    # for dev, int_list in zip(node_list_main, intf_list_main):
    #     for intrf in int_list:
    #         print(f'{dev} --> {intrf}')

    # for i in node_list():
    #     print(f'')

    # for i in intf:
    #     print(f'{node01} -> {intf}')
    # nodes = set([item[0] for item in list(topology_dict.keys()) + list(topology_dict.values())])
    # graph = gv.Graph(format="svg")

    # for node in nodes:
    #     graph.node(node)

    # for key, value in topology_dict.items():
    #     head, t_label = key
    #     tail, h_label = value
    #     graph.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" " * 12)

    # graph = apply_styles(graph, style_dict)
    # filename = graph.render(filename=out_filename)
    # print("Topology saved in", filename)

if __name__ == "__main__":
    with open("./topology.yaml") as topo:
        topology_dict = yaml.safe_load(topo)
        # print(topology_dict)
        draw_topology(topology_dict)

    # topo1 = {('R5', 'Eth0/5'): ('R6', 'Eth0/5'),('R4', 'Eth0/1'): ('R5', 'Eth0/1'),('R4', 'Eth0/2'): ('R6', 'Eth0/0')}
    # draw_topology(topo1)


# def draw_topology(topology_dict, out_filename="img/topology", style_dict=styles):
#     """
#     topology_dict - словарь с описанием топологии
#     Пример словаря topology_dict:
#         {('R4', 'Eth0/1'): ('R5', 'Eth0/1'),
#          ('R4', 'Eth0/2'): ('R6', 'Eth0/0')}
#     соответствует топологии:
#     [ R5 ]-Eth0/1 --- Eth0/1-[ R4 ]-Eth0/2---Eth0/0-[ R6 ]
#     Функция генерирует топологию, в формате svg.
#     И записывает файл topology.svg в каталог img.
#     """
#     nodes = set(
#         [item[0] for item in list(topology_dict.keys()) + list(topology_dict.values())]
#     )
#     graph = gv.Graph(format="svg")

#     for node in nodes:
#         graph.node(node)

#     for k, v in topology_dict.items():
#         print(v)

#     dev_int_list = []
#     for key, value in topology_dict.items():
#         dev_int_list.append(key)
#         dev_int_list.append(value)
#     dev_int_set = set(dev_int_list)
#     new_dev_int_list = list(dev_int_set)
#     print(new_dev_int_list)

#     for item in new_dev_int_list:
#         # print(f'{item[0]} --> {item[1]}')
#         head = t_label  = item[0]
#         tail = h_label = item[1]
#         graph.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" " * 12)

#         # head, t_label = key
#         # tail, h_label = value
#         # graph.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" " * 12)

#     graph = apply_styles(graph, style_dict)
#     filename = graph.render(filename=out_filename)
#     print("Topology saved in", filename)