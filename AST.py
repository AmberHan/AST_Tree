# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2020/11/13 11:44
# !@Author : DongHan Yang
# !@File   : AST.py.py
import queue
import json
# result_dict结果真值表 key:every_id;value:node
result_dict = {}
every_id = 1
result_dict1 = {}
every_id1 = 1


# father_node:父节点;children_list子节点;my_type:元电路对象;unitary矩阵,child=0减枝
class AstNode(object):
    def __init__(self, father_node, node_id, temp):
        self.father_node = father_node
        self.id = node_id
        self.type = int(temp["type"])
        self.label = temp.get("label")
        self.typeLabel = temp["typeLabel"]
        self.pos = int(temp["pos"])
        self.length = int(temp["length"])
        self.children = []

    def add_children(self, child):
        self.children.append(child)

# 初始化
def init_truth():
    with open('AST.txt', 'r') as f:
        data = json.load(f)
    # print(data)
    re_dist = data['root']
    root_node = AstNode(None, every_id, re_dist)
    result_dict[every_id] = root_node
    result_dict1[every_id1] = root_node
    re_list = data['root']['children']
    # 法一 广度优先
    node_queue = queue.Queue()
    node_queue.put(root_node)
    list_queue = queue.Queue()
    list_queue.put(re_list)
    gd_root(node_queue, list_queue)
    # 法二 深度优先
    sd_root(root_node, re_list)


# 深度优先
def sd_root(father_node, re_list):
    global every_id
    for children in re_list:
        every_id += 1
        new_node = AstNode(father_node, every_id, children)
        father_node.add_children(new_node)
        result_dict[every_id] = new_node
        re_list = children['children']
        sd_root(new_node, re_list)


# 广度优先
def gd_root(node_queue, list_queue):
    global every_id1
    while not node_queue.empty():
        node_queue_size = node_queue.qsize()
        for i in range(node_queue_size):
            father_node = node_queue.get()
            re_list = list_queue.get()
            for children in re_list:
                every_id1 += 1
                new_node = AstNode(father_node, every_id, children)
                father_node.add_children(new_node)
                result_dict1[every_id1] = new_node
                node_queue.put(new_node)
                list_queue.put(children['children'])


def main():
    init_truth()
    print("深度节点数目", every_id)
    print("广度节点数目", every_id1)
    # print(result_dict)
    # print(result_dict1)


if __name__ == '__main__':
    main()

