import sys
import random
import math
from typing import Tuple
from collections import defaultdict

def calculate_euclideanDistance(vecotr_row_1: list, vector_row_2: list, num_dim: int) -> float:
    assert len(vecotr_row_1) == num_dim
    assert len(vector_row_2) == num_dim
    dist = 0
    for dim in range(num_dim):
        dist += (vecotr_row_1[dim] - vector_row_2[dim])**2
    
    return math.sqrt(dist)

def k_means_clustering(num_cluster: int,
                       img: list, bit_per_pixcel: int, 
                       height: int, width: int,
                       apply_dims: list, seed: int = None) -> list:
    if seed is not None:
        random.seed(seed)
    
    # initialize cluster cordinatates
    cordinates_cluster_in_colorspace = []
    for _ in range(num_cluster):
        cordinate_cluster = []
        for _ in range(len(apply_dims)):
            cordinate_cluster.append(int(random.uniform(0, 255)))
        cordinates_cluster_in_colorspace.append(cordinate_cluster)
    
    # k-means clustering
    img_cluster_idx = [ [ [-1] for _ in range(width)] for _ in range(height) ]
    couter_by_cluster = [0 for _ in range(num_cluster)]    
    sum_by_cluster = [ [0]*len(apply_dims) for _ in range(num_cluster)]
    
    while True:
        # cluster change flag
        clustering_unchanged = False
        # store cordinates of each class
        cordinates_memo = [[] for _ in range(num_cluster)]
        for y in range(height):
            for x in range(width):
                pixcel = []
                for dim in apply_dims:
                    pixcel.append(img[y][x][dim])
                
                idx_cluster_belong = -1
                # true max distance is sqrt( 255*255*len(apply_dims))
                # ex. (0,0,0), (255, 255, 255)
                distance_min = 255*255*len(apply_dims)
                for idx_cluster, cordinate_cluster in enumerate(cordinates_cluster_in_colorspace):
                    distance = calculate_euclideanDistance(pixcel, cordinate_cluster, len(apply_dims))
                    if distance_min > distance:
                        distance_min = distance
                        idx_cluster_belong = idx_cluster
                        
                if idx_cluster_belong != img_cluster_idx[y][x][0]:
                    clustering_unchanged = True
            
                img_cluster_idx[y][x][0] = idx_cluster_belong
                cordinates_memo[idx_cluster_belong].append((x, y))
                couter_by_cluster[idx_cluster_belong] += 1
                for idx, apply_dim in enumerate(apply_dims):
                    sum_by_cluster[idx_cluster_belong][idx] += img[y][x][apply_dim]
        
        # check continue
        if clustering_unchanged:
            break
        
        # update cluter cordinates
        for idx_cluster in range(cordinates_cluster_in_colorspace):
            for dim in range(len(cordinates_cluster_in_colorspace[0])):
                cordinates_cluster_in_colorspace[idx_cluster][dim] = sum_by_cluster[idx_cluster][dim] / couter_by_cluster[idx_cluster]
    
    return img_cluster_idx

def calc_center_cordinates_by_class(img: list, bit_per_pixcel: int, height: int, width: int, apply_dim: int) -> Tuple:
    sum_x_cordinate_by_cluster = defaultdict(int)
    sum_y_cordinate_by_cluster = defaultdict(int)
    couter_by_cluster = defaultdict(int)
    center_cordinates_by_cluster = defaultdict(tuple)
    for y in range(height):
        for x in range(width):
                idx_cluster = img[y][x][apply_dim]
                sum_x_cordinate_by_cluster[idx_cluster] += x
                sum_y_cordinate_by_cluster[idx_cluster] += y
                couter_by_cluster[idx_cluster] += 1
                
    for idx_cluster in couter_by_cluster.keys():
        x_center = sum_x_cordinate_by_cluster[idx_cluster] // couter_by_cluster[idx_cluster]
        y_center = sum_y_cordinate_by_cluster[idx_cluster] // couter_by_cluster[idx_cluster]
        center_cordinates_by_cluster[idx_cluster] = (x_center, y_center)
    
    return center_cordinates_by_cluster
        
    
                    
        
            
            
            
            
            
                
        
    
    
    