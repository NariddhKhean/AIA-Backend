import networkx as nx
import osmnx as ox
import geopandas as gpd
import fiona
fiona.drvsupport.supported_drivers['WFS'] = 'r'
import momepy
import shapely

LAYER_DIR = 'live/g3/Route Generator'


def call(input_args):
    # special_needs_visual:bool,
    # special_needs_physical:bool,
    # public_image:float,
    # origin = (48.19, 16.362),
    # destination = (48.20, 16.364),
    '''takes in user profile and preferences and returns either preferred poi or generated route

    args:
    special_needs_visual    : Get boolean from a check box
    special_needs_physical  : Get boolean from a check box
    public_image    : Slider with range of 0 to 1
    origin  : Starting location specified as a tuple of (lat, lon)
    destination  : target location specified as a tuple of (lat, lon)

    returns : returns shortest path geojson with Linestring geometry
    '''

    public_image = max(min(float(input_args['public_image']), 1), 0)
    special_needs_visual = bool(input_args['special_needs_visual'])
    special_needs_physical = bool(input_args['special_needs_physical'])
    origin = (input_args['origin']['lng'], input_args['origin']['lat'])
    destination = (input_args['destination']['lng'], input_args['destination']['lat'])


    #-----------------------------------CITY STREETS DATAFRAME---------------------------------------#
    #GET PUBLIC IMAGE DATA
    # urban_image_url = 'https://drive.google.com/file/d/1-KDBSknNJ04vhp1I1xHILhZ7pJeRQDuP/view?usp=sharing'
    # urban_image_url='https://drive.google.com/uc?id=' + urban_image_url.split('/')[-2]
    urban_image = gpd.read_file(f'{LAYER_DIR}/public_image2.geojson')

    #GET ACCESSIBILITY VISUAL DATA
    # acc_visual_url = 'https://drive.google.com/file/d/1-F8eNxXaHHoGORyHbJk8zT0BLsu_aZdx/view?usp=sharing'
    # acc_visual_url='https://drive.google.com/uc?id=' + acc_visual_url.split('/')[-2]
    acc_visual = gpd.read_file(f'{LAYER_DIR}/acc_visual_friendly.geojson')

    #GET ACCESSIBILITY WHEELCHAIR DATA
    # acc_wheelchair_url = 'https://drive.google.com/file/d/1-GOp9cvgg-j6Dn8kaThwsU1JzUDo64aj/view?usp=sharing'
    # acc_wheelchair_url='https://drive.google.com/uc?id=' + acc_wheelchair_url.split('/')[-2]
    acc_wheelchair = gpd.read_file(f'{LAYER_DIR}/acc_wheelchair_friendly.geojson')

    #GET CITY EDGES INFORMATION INTO ONE DATAFRAME
    city_edges = urban_image.loc[:, ['u', 'v', 'key', 'name', 'weighted_sum']]
    city_edges.weighted_sum = 1-city_edges.weighted_sum
    city_edges['blind_friendly'] = 1-acc_visual['visual_friendly_index']
    city_edges['wheelchair_friendly'] = 1-acc_wheelchair['wheelchair_friendly_index']
    city_edges['geometry'] = acc_wheelchair['geometry']
    city_edges = city_edges.rename(columns={'weighted_sum':'urban_image'})
    city_edges = city_edges.set_index(['u', 'v', 'key'])

    #GET CITY NODES INFORMATION INTO ONE DATAFRAME
    # city_nodes_url = 'https://drive.google.com/file/d/100i_xMPGcs2ouBeT0TlOxzNpywE0wsUU/view?usp=sharing'
    # city_nodes_url='https://drive.google.com/uc?id=' + city_nodes_url.split('/')[-2]
    city_nodes = gpd.read_file(f'{LAYER_DIR}/nodes.geojson')
    city_nodes = city_nodes.set_index('osmid')


    #-----------------------------------CITY STREETS DATAFRAME---------------------------------------#

    #-----------------------------------AFFECT STREET WEIGHTS WITH USER INPUT---------------------------------------#
    crs = 'epsg:4326'

    #create personalised dataframe
    routes_edges = city_edges.copy()

    #edit urban image
    routes_edges.urban_image = (1-public_image)*city_edges.urban_image

    #edit special_needs_visual
    if special_needs_visual:
        routes_edges.blind_friendly = city_edges.blind_friendly
    else:
        routes_edges.blind_friendly = 1.0

    #edit special_needs_physical
    if special_needs_physical:
        routes_edges.wheelchair_friendly = city_edges.wheelchair_friendly
    else:
        routes_edges.wheelchair_friendly = 1.0

    routes_edges['edge_weights'] = routes_edges.urban_image + routes_edges.blind_friendly + routes_edges.wheelchair_friendly

    new_cols = [col for col in routes_edges.columns.values if col != 'geometry'] + ['geometry']
    routes_edges = routes_edges.reindex(new_cols, axis=1)
    #-----------------------------------AFFECT STREET WEIGHTS WITH USER INPUT---------------------------------------#

    #-----------------------------------COMBINE GRAPH AND PLOT ROUTES---------------------------------------#
    graph_attrs = {'crs': 'epsg:4326', 'simplified': True}
    graph = ox.graph_from_gdfs(city_nodes, routes_edges, graph_attrs)

    #make a copy of the graph for reference
    gcopy = graph.copy()

    #Get source and target locations to nearast node
    source = ox.distance.nearest_nodes(graph, origin[1], origin[0])
    target = ox.distance.nearest_nodes(graph, destination[1], destination[0])

    #construct path. returns nodes that make up the path
    path = nx.dijkstra_path(graph, source, target, weight='edge_weights')

    #construct position for nodes
    pos = {i:[graph.nodes[i]['x'], graph.nodes[i]['y']]  for i in path }

    #construct edge for the path
    edge_path=[]
    for i in range(len(path)-1):
        edge=(path[i],path[i+1])
        edge_path.append(edge)

    #construct graph for path
    graph_path=nx.Graph()
    graph_path.add_nodes_from(path)
    graph_path.add_edges_from(edge_path)

    #construct geometry for path
    graph_path.edges(data=True)
    for u,v,data in graph_path.edges(data=True):
        data['geometry'] = shapely.geometry.LineString([pos[u], pos[v]])     

    #assign x,y to nodes 
    for u,data in graph_path.nodes(data=True):
        data['x'] = pos[u][0]
        data['y'] = pos[u][1]

    #convert edges into geodataframe
    route_edges = momepy.nx_to_gdf(graph_path, points=False)

    #convert geodataframe to geojson
    route_output = route_edges.to_json()

    return route_output

if __name__ == '__main__':
    test_input_args = {
        'special_needs_visual': True,
        'special_needs_physical': True,
        'public_image': 0.1,
        'origin': (48.19, 16.362),
        'destination': (48.20, 16.364),
    }
    call(test_input_args)

