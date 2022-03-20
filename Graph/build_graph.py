from itertools import count
import py2neo
from py2neo import Graph, Node
import json
import os


class Covid19Graph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, "data/covid19.json")
        self.class_path = os.path.join(cur_dir, "data/class_name.json")
        self.p_path = os.path.join(cur_dir, "data/property_name.json")
        self.g = Graph(
            "http://localhost:7474",  # uri
            user="neo4j",
            password="112358")

    def read_file(self):
        # 读取json文件到python对象
        with open(self.data_path, encoding='UTF-8') as f:
            self.data = json.loads(f.read())
        with open(self.class_path, encoding='UTF-8') as f:
            self.class_name = json.loads(f.read())
        with open(self.p_path, encoding='UTF-8') as f:
            self.p_name = json.loads(f.read())
        print("read file done!")

    def build_nodes(self):
        # 创建节点Nodes, 保存关系rels
        rels = []
        cnt = 0
        for i in self.data['@graph']:
            attr = {}
            attr['id'] = i['@id'].split('/')[-1]
            attr['name'] = i['label']['@value']
            if attr['id'][0] == 'R':
                # 一般实体 Resource
                node_class = self.class_name[i['@type'].split('/')[-1]]
                for k in i.keys():
                    if k[0] == 'P':
                        if i[k].startswith('http'):
                            # 关系
                            rels.append((attr['id'], k, i[k].split('/')[-1]))
                        else:
                            # 属性
                            attr[self.p_name[k]] = i[k]
            elif attr['id'][0] == 'C':
                # 类别 Class
                node_class = "Class"
                if "subClassOf" in i.keys():
                    rels.append((attr['id'], "subClassOf", i["subClassOf"].split('/')[-1]))
            else:
                # 跳过 Property
                continue
            node = Node(node_class, **attr)
            self.g.create(node)
            cnt += 1
        self.rels = rels
        print(f"build {cnt} nodes done!")

    def build_rel(self):
        # 创建 关系 rels
        count = 0
        for rel in self.rels:
            id_a, r_id, id_b = rel
            r_type = self.p_name[r_id] if r_id[0] == 'P' else 'subClassOf'
            query = "match(p),(q) where p.id='%s'and q.id='%s' create (p)-[rel:%s {id:'%s'}]->(q)" % (
                id_a, id_b, r_type, r_id)
            try:
                self.g.run(query)
                count += 1
            except Exception as e:
                print(e)
        print(f"build {count} relations done!")

    def build(self):
        # neo4j中构建KG
        self.read_file()
        self.build_nodes()
        self.build_rel()


if __name__ == '__main__':
    kg = Covid19Graph()
    kg.build()
