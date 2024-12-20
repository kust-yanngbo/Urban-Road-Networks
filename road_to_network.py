# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:04:04 2024

@author: Li Yuanbiao
"""

from osgeo import gdal
import re
import networkx as nx

def read_gdb_layer(gdb_dataset, layer_index):
    """
    读取GDB数据库中的指定图层，并提取要素的几何信息和属性字段。
    
    参数:
    gdb_dataset -- 打开的GDB数据集对象
    layer_index -- 图层索引
    
    返回值:
    data -- 包含几何信息和属性字段的列表
    """
    layer = gdb_dataset.GetLayer(layer_index)
    layer_data = []
    print(f"Layer Name: {layer.GetName()}")
    
    feature_count = layer.GetFeatureCount()
    for feature_index in range(feature_count):
        feature = layer.GetNextFeature()
        geom = feature.GetGeometryRef()
        layer_data.append(geom.ExportToWkt())
        
        for field_index in range(feature.GetFieldCount()):
            field_name = feature.GetFieldDefnRef(field_index).GetName()
            field_value = feature.GetField(field_index)
            # 打印或存储属性字段信息
            # print(f"{field_name}: {field_value}")
    
    return layer_data

def parse_geometries(data):
    """
    解析几何信息，区分节点和边。
    
    参数:
    data -- 包含几何信息的列表
    
    返回值:
    nodes -- 节点列表
    edges -- 边列表
    """
    nodes = []
    edges = []
    for geom in data:
        if geom[:5] != 'POINT':
            prefix = 'MULTILINESTRING '
            split_result = geom.split(prefix, 1)
            edges.append(split_result[1])
        else:
            match = re.search(r'\(([\d\.]+) ([\d\.]+)\)', geom)
            x = float(match.group(1))
            y = float(match.group(2))
            nodes.append((x, y))
    
    return nodes, edges

def convert_edges_to_networkx_format(nodes, edges):
    """
    将边转换为networkx所需的格式。
    
    参数:
    nodes -- 节点列表
    edges -- 边列表
    
    返回值:
    net_edges -- 转换后的边列表
    """
    net_edges = []
    for edge in edges:
        new_edge = []
        matches = re.findall(r'\(\((.*?)\)\)', edge)
        grouped_values = [match.split() for match in matches[0].split(',')]
        for group in grouped_values:
            node0 = float(group[0])
            node1 = float(group[1])
            if (node0, node1) in nodes or (node1, node0) in nodes:
                new_edge.append((node0, node1))
        if new_edge:
            net_edges.append(new_edge)
    return net_edges

def main(gdb_file):
    driver = gdal.GetDriverByName("OpenFileGDB")
    gdb_dataset = gdal.OpenEx(gdb_file, gdal.OF_VECTOR)
    
    if gdb_dataset is None:
        print("Could not open the database.")
    else:
        layer_count = gdb_dataset.GetLayerCount()
        data = []
        for i in range(layer_count):  
            layer_data = read_gdb_layer(gdb_dataset, i)
            data.extend(layer_data)
        
        nodes, edges = parse_geometries(data)
        net_edges = convert_edges_to_networkx_format(edges)
        
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(net_edges)
    
    #nx.write_graphml(G, 'data/chdu_4.graphml')

if __name__ == "__main__":
    gdb_file = "data/RoadNet/Kunming/昆明市内部道路路网.gdb"
    main(gdb_file)
                
