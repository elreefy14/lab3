import networkx as nx
import matplotlib.pyplot as plt

def create_graph(filename):
    # Create a graph
    G = nx.Graph()

    with open(filename, 'r') as file:
        lines = file.readlines()
        # Read the file line by line starting from the second line
        for line in lines[1:]:
            G.add_edge(line.split(",")[0], line.split(",")[1], weight=int(line.split(",")[2]))

    return G


def dijkstra(G):
    D, D_temp, P = {}, {}, {}
    D_list, P_list = [], []

    # Get all nodes in the graph
    nodes = list(G.nodes())
    popped_list = [nodes[0]]

    # Get the adjacency dictionary
    adj = dict(G.adjacency())

    # Set of nodes whose least cost path is definitely known
    n_dash = [nodes[0]]

    # Loop through all the nodes
    for node in nodes:
        # If the node is a neighboring node, add its weight
        if node in adj[nodes[0]].keys(): 
            D[node], D_temp[node], P[node] = adj[nodes[0]][node]['weight'], adj[nodes[0]][node]['weight'], nodes[0]
        # Otherwise, add infinity
        else: 
            D[node], D_temp[node] = float("inf"), float("inf")

    D_list.append(D.copy())
    P_list.append(P.copy())
    n_dash.append(D_temp.pop(nodes[0]))

    # Continue until all nodes in N'
    while len(n_dash) <= len(nodes):
        # Get the node that has the minimum weight
        w = min(D_temp, key=lambda k: D_temp[k])

        # Update D(v) for all v adjacent to w and not in N'
        for v in adj[w].keys(): 
            if v in D_temp.keys() and w in D_temp.keys(): 
                if D[v] > D[w] + adj[w][v]['weight']:
                    D[v], D_temp[v] = D[w] + adj[w][v]['weight'], D[w] + adj[w][v]['weight']
                    P[v] = w

        D_list.append(D.copy())
        P_list.append(P.copy())
        popped_list.append(w)

        # Remove that node from D, and add it to N'
        n_dash.append(D_temp.pop(w))

    return D_list, P_list, popped_list


def construct_shortest_path(p, origin_node, node, path):
    if node != origin_node: 
        path.append(node)
        construct_shortest_path(p, origin_node, p[node], path)

    return path


def get_forwarding_table(p, nodes):
    dic = {}

    for node in nodes[1:]: 
        k = construct_shortest_path(p, nodes[0], node, [])
        dic[node] = k[-1]

    return dic


def draw_forwarding_table(nodes, dic):
    print(f"Destination\tLink")

    for node in nodes[1:]:
        print(f"{node}\t\t({nodes[0]}, {dic[node]})")


def print_lines(n):
    # This is the escape sequence for color blue
    for i in range(n): 
        print("\033[34m-", end="\033[0m")


def print_complete_line(nodes):
    # Lines for first steps
    print_lines(15)

    # Lines for each node
    for l in range(len(nodes)-1): 
        print_lines(15)

    print()


def print_first_row(nodes):
    print_complete_line(nodes)
    print(f"Step\tN'\t", end="")

    for node in nodes[1:]: 
        print(f"D({node}), P({node})", end="\t")

    print()
    print_complete_line(nodes)


def draw_info_table(nodes, D, P, popped_list):
    print_first_row(nodes)
    step = 0

    for (d, p) in zip(D[1:], P[1:]):
        print(f"{step}\t{''.join(map(str, popped_list[:step+1]))}", end="\t")
        step += 1

        for node in nodes[1:]: 
            try: 
                if node not in popped_list[:step]: 
                    print(f"   {d[node]}, {p[node]}", end="\t\t")
                else: 
                    print(end="\t\t")
            except KeyError: 
                print("    \u221e", end="\t\t")

        print()

    # Print last line
    print(f"{step}\t{''.join(map(str, popped_list[:step+1]))}", end="\n")
    print_complete_line(nodes)


# Main
G = create_graph("input.txt")

# Get the positions of the nodes
pos = nx.spring_layout(G)

# Draw the graph
nx.draw(G, pos, with_labels=True, font_weight='bold')

# Get the edges weights
edge_weight = nx.get_edge_attributes(G, 'weight')

# Draw the edges weights
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weight)
plt.show()

nodes = list(G.nodes())
D, P, popped_list = dijkstra(G)

# Draw the forwarding table
dic = get_forwarding_table(P[-1], nodes)
draw_forwarding_table(nodes, dic)

# Draw the info table
draw_info_table(nodes, D, P, popped_list)