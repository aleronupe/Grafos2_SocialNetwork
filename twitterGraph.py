import plotly.graph_objects as go
import random
import networkx as nx
import os
from collections import deque

from twitterRequests import *

def get_user_list(username):
    file_path = 'data/user_list/' + username + '.json'
    data = []
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
    else:
        data = get_list(username, 'friends')
        if len(data) > 0:
            with open(file_path, 'w') as outfile:
                json.dump(data, outfile)

    return data

def get_ids_list(username):
    file_path = 'data/ids/' + username + '.json'
    data = []
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
    else:
        data, rate_limit = get_ids(username, 'friends')
        print(rate_limit)
        if not rate_limit:
            with open(file_path, 'w') as outfile:
                json.dump(data, outfile)

    return data

def mount_graph():
    user = input('Whats your Twitter username? ')
    friends = get_user_list(user)
    verified = []
    for friend in friends:
        if friend['verified']:
            verified.append(friend)

    for famous in verified:
        friends.remove(famous)

    return create_di_graph(friends, user)

def create_di_graph(vec, user):

    # G = nx.DiGraph()
    G = nx.Graph()
    DiG = nx.MultiDiGraph()

    for i in range(0,len(vec)):
        G.add_node(i, name=vec[i]['name'], id=vec[i]['id'], username=vec[i]['screen_name'], visited=False)
        DiG.add_node(i, name=vec[i]['name'], id=vec[i]['id'], username=vec[i]['screen_name'], visited=False)

    nodes = DiG.nodes(data=True)
    for out_node in nodes:
        username = str(out_node[1]['username'])
        related_friends = get_ids_list(username)
        for node in nodes:
            for friend_id in related_friends:
                if(friend_id == node[1]['id']):
                    G.add_edge(out_node[0], node[0], layer=0, traveled=False)
                    DiG.add_edge(out_node[0], node[0], layer=0, traveled=False)
                

    title = 'Grafo de quem ' + user + ' segue no Twitter'
    return show_graph(G, DiG, title), G

def show_graph(G, DiG, text, colors = [], path = []):

    pos = nx.fruchterman_reingold_layout(G)

    # G = G.to_directed()
    edge_x = []
    edge_y = []
    for e in DiG.edges():
        if e[0] not in path and e[1] not in path:
            edge_x.extend([pos[e[0]][0], pos[e[1]][0], None])
            edge_y.extend([pos[e[0]][1], pos[e[1]][1], None])

    p_edge_x = []
    p_edge_y = []
    for i in range(0, len(path) - 1):
        edge = (path[i], path[i+1])
        p_edge_x.extend([pos[edge[0]][0], pos[edge[1]][0], None])
        p_edge_y.extend([pos[edge[0]][1], pos[edge[1]][1], None])

    edge_trace1 = go.Scatter(
        x=p_edge_x, y=p_edge_y,
        line=dict(width=1, color='#0F0'),
        hoverinfo='none',
        mode='lines')

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x =[pos[k][0] for k in range(len(pos))]
    node_y=[pos[k][1] for k in range(len(pos))]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=colors,
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(DiG.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(DiG.nodes[node]['name'] + ' \n@' + DiG.nodes[node]['username'])

    if len(colors) > 0:
        node_trace.marker.color = colors
    else:
        node_trace.marker.color = node_adjacencies

    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, edge_trace1, node_trace],
                    layout=go.Layout(
                title='<b>'+text+'</b>',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="Feito por Alexandre Miguel e Gabriela Guedes",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False,
                            showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # print('\033[1m' + 'Wictão' + '\033[0m')
    # for i in range(0, len(DiG)):
    #     if DiG.nodes[i]['username'] == 'GirardiWictor':
    #         iterator = DiG.neighbors(i)
    #         for item in iterator:
    #             print(DiG.nodes[item]['username'])
    # print(' ')

    # print('\033[1m' + 'Ganda' + '\033[0m')
    # for i in range(0, len(DiG)):
    #     if DiG.nodes[i]['username'] == 'ganda_lc':
    #         iterator = DiG.neighbors(i)
    #         for item in iterator:
    #             print(DiG.nodes[item]['username'])

    # print(' ')
            
    # print('\033[1m' + 'Andrézin' + '\033[0m')
    # for i in range(0, len(DiG)):
    #     if DiG.nodes[i]['username'] == 'AGameplayz':
    #         iterator = DiG.neighbors(i)
    #         for item in iterator:
    #             print(DiG.nodes[item]['username'])

    # print('\033[1m' + 'Leandro' + '\033[0m')
    # for i in range(0, len(DiG)):
    #     if DiG.nodes[i]['username'] == 'Leandro_gpaiva':
    #         iterator = DiG.neighbors(i)
    #         for item in iterator:
    #             other = DiG.neighbors(item)
    #             print(DiG.nodes[item]['username'])
    #             for bitch in other:
    #                 if bitch == i:
    #                 print('Segue de volta')
                

    # print('\n' + 'REVERSE' + '\n')

    # Rev = DiG.reverse()

    # print('\033[1m' + 'Wictão' + '\033[0m')
    # for i in range(0, len(Rev)):
    #     if Rev.nodes[i]['username'] == 'GirardiWictor':
    #         iterator = Rev.neighbors(i)
    #         for item in iterator:
    #             print(Rev.nodes[item]['username'])
    # print(' ')

    # print('\033[1m' + 'Ganda' + '\033[0m')
    # for i in range(0, len(Rev)):
    #     if Rev.nodes[i]['username'] == 'ganda_lc':
    #         iterator = Rev.neighbors(i)
    #         for item in iterator:
    #             print(Rev.nodes[item]['username'])

    # print(' ')
            
    # print('\033[1m' + 'Andrézin' + '\033[0m')
    # for i in range(0, len(Rev)):
    #     if Rev.nodes[i]['username'] == 'AGameplayz':
    #         iterator = Rev.neighbors(i)
    #         for item in iterator:
    #             print(Rev.nodes[item]['username'])



    # fig.show()
    return DiG

def search_path(from_user, to_user, G):
    return nx.shortest_path(G, from_user, to_user)

def get_user_graph_id(username, G):
    for i in range(0, len(G)):
        if G.nodes[i]['username'] == username:
            return i
    return -1

def breadth_first_search(G, username):
    nodes = G.nodes(data=True)
    origin = get_user_graph_id(username, G)
    size = len(nodes)
    path = []
    if (origin != -1):
        nodes[origin]['visited'] = True
        path = list(G.adj[origin])
        for init_pos in path:
            nodes[init_pos]['visited'] = True
            G.edges[origin, init_pos]['traveled'] = True
            G.edges[origin, init_pos]['layer'] = 1
        for pos in path:
            neighbours = list(G.adj[pos])
            for n_pos in neighbours:
                if(nodes[n_pos]['visited']):
                    if(G.edges[origin, init_pos]['layer'] == 0):
                        G.edges[origin, init_pos]['layer'] = 2
                else:
                    path.append(n_pos)
                    nodes[n_pos]['visited'] = True
                    G.edges[pos, n_pos]['traveled'] = True
                    G.edges[pos, n_pos]['layer'] = 1
    node_colors = []
    for n in range(size):
        if(n == origin):
            node_colors.append("blue")
        elif(nodes[n]['visited'] == True):
            node_colors.append("red")
        else:
            node_colors.append("green")
    
    return node_colors

def depth_first_search(G, username, stack):
    nodes = G.nodes(data=True)
    origin = get_user_graph_id(username, G)
    size = len(nodes)

    if (origin == -1):
        return stack

    nodes[origin]['visited'] = True
    adjacents = list(G.adj[origin])
    stack.append(origin)
    
    for elmnt in adjacents:
        if nodes[elmnt]['visited'] == False:
            G.edges[origin, elmnt, 0]['traveled'] = True
            G.edges[origin, elmnt, 0]['layer'] = 1
            stack = depth_first_search(G, nodes[elmnt]['username'], stack)
        else:
            G.edges[origin, elmnt, 0]['traveled'] = True
            G.edges[origin, elmnt, 0]['layer'] = 2
    return stack

def prepare_dfs(G, username):
    nodes = G.nodes(data=True)
    origin = get_user_graph_id(username, G)
    node_colors = []
    size = len(nodes)
    stack = []
    stack = depth_first_search(G, username, stack)
    for n in range(size):
        if(n == origin):
            node_colors.append("blue")
        elif(nodes[n]['visited'] == True):
            node_colors.append("red")
        else:
            node_colors.append("green")
    return node_colors, stack

def create_multidi_graph(vec, username):
    print(vec)
    DiG = nx.MultiDiGraph()
    G = nx.Graph()
    size = len(vec)
    

    for i in range(0,size):
        DiG.add_node(i, id=vec[i][0])
        G.add_node(i, id=vec[i][0])
        

    nodes = DiG.nodes(data=True)
    print(nodes)
    for i in range(0,size):
        adj_set = vec[i][1]
        for j in range(0, size):
            if nodes[j]['id'] in adj_set:
                G.add_edge(nodes[i][0], nodes[j][0], weight=1)
                DiG.add_edge(nodes[i][0], nodes[j][0], weight=1)
                    
    title = 'Inner circle de' + username
    return show_graph(G, DiG, title)

# def djikstra(G, origin):



def inner_circle(G, username):
    node_colors, stack = prepare_dfs(G, username)
    origin = get_user_graph_id(username, G)
    adjacents = set(G.adj[origin])

    containers = []
    removals = []

    for elmnt in adjacents:
        in_adjacents = set(G.adj[elmnt]) #Usuários que o amigos do Origem seguem
        if not(origin in in_adjacents): #Constrói lista de usuários que o Origem segue que não o seguem de volta
            removals.append(elmnt) 

    for out in removals: # Remove usuários que não o seguem de volta
        print('removing: ' + G.nodes[out]['username'] )
        adjacents.remove(out)


    #Elementos que o nó de origem segue
    for elmnt in adjacents:
        in_adjacents = set(G.adj[elmnt]) #Usuários que o amigos do Origem seguem
        print(str(elmnt) + ': ' + G.nodes[elmnt]['username'])
        print(in_adjacents)
        elmnt_following = in_adjacents.intersection(adjacents) # Interseção entre quem Origem segue e quem o amigo de origem segue
        containers.append((elmnt, elmnt_following))

    
    what = create_multidi_graph(containers, username)

    return


    

        



if __name__ == "__main__":
    create_barear_token()
    DiG, G = mount_graph()
    usr = input('Perform Depth First Search from user (use name without @): ')
    node_colors, stack = prepare_dfs(DiG, usr)
    title = 'Busca por Profundidade começando em ' + usr
    # for element in stack:
    #     print(G.nodes[element]['username'])
    # show_graph(G, DiG, title, node_colors)
    inner_circle(DiG, usr)
    

#4062018375
