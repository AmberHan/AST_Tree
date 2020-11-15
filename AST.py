# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2020/11/13 11:44
# !@Author : DongHan Yang
# !@File   : AST.py.py
import queue
import json
# result_dict结果真值表 key:真值表;value:[代价,node]
result_dict = {}


# father_node:父节点;children_list子节点;my_type:元电路对象;unitary矩阵,child=0减枝
class AstNode(object):
    def __init__(self, temp):
        # self.father_node = father_node
        self.type = int(temp["type"])
        self.label = temp.get("label")
        self.typeLabel = temp["typeLabel"]
        self.pos = int(temp["pos"])
        self.length = int(temp["length"])
        # self.children = children
        # self.id = temp["id"]
        # self.parent = None

    # 添加父亲的子节点,目的为了减枝
    def add_children(self, children):
        self.children_list.append(children)


# 广度优先,循环寻找最优解
# type_all:基本元情况； node:父节点
def com_circuit(plies_node, type_all):
    while not plies_node.empty():
        plies_node_list_size = plies_node.qsize()
        # 广度优先，每层遍历
        for i in range(plies_node_list_size):
            node = plies_node.get()
            if node.child == 0:  # 节点非最优
                continue
            for circuit_i in range(len(type_all)):
                if circuit_i == node.my_type:  # 相同的会抵消,不考虑
                    continue
                else:
                    # 优化后 自己算的矩阵
                    circuit_new_unitary = np.dot(type_all[circuit_i][2], node.unitary)
                    unitary_tuple_new = tuple(unitary_list(circuit_new_unitary))
                    node_cost = node.cost + type_all[circuit_i][1]
                    node_new = EveryNode(node, circuit_i, node_cost, circuit_new_unitary)
                    node.add_children(node_new)
                    if unitary_tuple_new not in result_dict:  # 新的解答
                        print('目前解数目：{}'.format(len(result_dict)))
                        plies_node.put(node_new)
                        result_dict[unitary_tuple_new] = [node_cost, node_new]
                    elif unitary_tuple_new in result_dict and result_dict[unitary_tuple_new][0] > node_cost:  # 更优解
                        plies_node.put(node_new)
                        node_get = result_dict[unitary_tuple_new][1]  # 找到非优解进行child=0,child_list置空操作
                        node_get.clear_children()
                        result_dict[unitary_tuple_new] = [node_cost, node_new]  # 更新真值字典
                    else:
                        node_new.clear_children()
                        continue


# 初始化
def init_truth():
    with open('AST.txt', 'r') as f:
        data = json.load(f)
    mm = data['root']['children']
    print(mm)
    for i in mm['children']:
        print(i, '\n')
        AstNode(i)
        # print(i['type'])
        # AstNode(i)
    #     for j in i['children']:
    #         print(j['type'])
    # print(data['root'])
    # circuit_unitary = np.identity(2 ** n)
    # node_0 = EveryNode(None, None, 0, circuit_unitary)
    # tree_queue = queue.Queue()
    # tree_queue.put(node_0)
    # com_circuit(tree_queue, type_all)
    # print('(数组列表):[代价，node标号]')
    # # print(result_dict)
    # print('真值表可表达的情况数目:{}'.format(len(result_dict)))


def main():
    init_truth()


if __name__ == '__main__':
    main()

