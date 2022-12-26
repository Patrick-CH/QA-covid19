[**English**](README.md) | [**中文说明**](README_ZH.md)

# QA-covid19

QA-covid19 是一个基于 KG (Knowledge Graph) 和 NLP (Natural Language Processing)的问答系统。



## 介绍

知识图谱，也称为语义网络，表示现实世界实体的网络——即对象、事件、情况或概念——并说明它们之间的关系。这些信息通常存储在图数据库中，并可视化为图结构，由此产生了术语知识“图”。

我们使用来自 openKG.cn 的 [covid19 知识图谱](http://openkg.cn/dataset/covid-19-baike) 来构建我们的系统。

与其他项目不同，我们使用 NER 模型和分类器来处理问题。

QIC(Query Intent Classification)数据集和NER数据集来自[CBLUE(Chinese Biomedical Language Understanding Evaluation)](https://tianchi.aliyun.com/cblue)



### 概要

项目结构

```文件树
│  classifier_model.py
│  question_classifier.py
│  README.md
│  wordIndexDict.json
│
├─app
│  │  app.py
│  │  forms.py
│  │  __init__.py
│  │
│  ├─static
│  │      style.css
│  │
│  ├─templates
│  │      base.html
│  │      chat.html
│  │      index.html
│  │      macros.html
│
├─data
│  │  diseases.json
│  │  NERtest.csv
│  │  qic_idx.json
│  │  tags_ner.json
│  │  test.csv
│  │  test.label.csv
│  │
│  ├─CMeEE
│  │      CMeEE_dev.json
│  │      CMeEE_test.json
│  │      CMeEE_train.json
│  │      example_gold.json
│  │      example_pred.json
│  │      README.txt
│  │
│  ├─KUAKE-QIC
│  │      example_gold.json
│  │      example_pred.json
│  │      KUAKE-QIC_dev.json
│  │      KUAKE-QIC_test.json
│  │      KUAKE-QIC_train.json
│  │      README.txt
│  │
│  └─model_data
│
├─MedicalNER
│  │  BiLSTMCRF.py
│  │  CRF.py
│  │  data_process.py
│  │  torch_ner.py
│  │  train_ner.py
│  │  w2idx.json
│  │  __init__.py
│
├─model
│  ├─bilstm_crf_ner_v0
│  │  └─assets
│  └─v1_test
│      └─assets
├─pretrained_model
│  ├─bert_zh_L-12_H-768_A-12_4
│  └─bert_zh_preprocess_3
│
├─QA_app
│  │  AnswerBuild.py
│  │  AnswerSearch.py
│  │  ChatBot.py
│  │  __init__.py
|  
├─Graph
│  │  build_graph.py
│  │  __init__.py
```



- app/ 提供我们系统的网络服务，包括网页和API服务。
- QA_app 提供了一个机器人，可以回答与 covid19 相关的医疗问题。
- classifier_model.py 训练问题意图(QIC)分类模型
- graph 在neo4j 数据库中构建知识图谱



### 特性

我们使用 NER 模型和分类器而不是预先设定的规则和关键字来设计 QA 系统，这将有助于我们的机器人回答更多相关的问题。



## 必要条件

我们的系统支持Windows 和 Linux 系统，但您必须满足以下要求：

- python 3.7 +
- tensorflow 2.5.0 +
- tensorflow-text 2.5.0 +
- py2neo 4.2.0 +
- neo4j 4.2.0 +

此外，我们建议您在运行我们的系统之前准备至少 4GB 显存的 GPU。



## 安装和使用

您可以按照以下步骤安装我们的系统：

下载：

`git clone git@github.com:Patrick-CH/QA-covid19.git`

建立KG：

`python ~/Graph/build_graph.py`

运行我们的系统：

`python ~/app.py`



## 开发

我们的系统提供网页和API服务。

网页：访问 localhost:80 即可看到网页。

接口定义：

| 方法 | 路径  | form-data            | response             |
| :--- | :---- | :------------------- | :------------------- |
| POST | /chat | {“问题”：“示例问题”} | {“答案”：“示例答案”} |



## 版本日志

V0：我们第一个验证系统框架的版本。

V1：首次发布功能比较丰富的版本。



## 分支

- Product (master ): 稳定版本
- Develop (dev branch): 最新版本
- Feature : 添加新的特性 (仍在开发中)
- Release : 公开发行版 (仍在开发中)



## 参考

[1] CBLUE: A Chinese Biomedical Language Understanding Evaluation Benchmark [[github](https://github.com/CBLUEbenchmark/CBLUE)] [[网站](https://tianchi.aliyun.com/cblue)]

[2] COVID-19 开放知识图谱.百科[[网站](http://openkg.cn/dataset/covid-19-baike)]



### 联系我们

如果您有任何问题或建议，请随时通过 chenyuke@whut.edu.cn 或 yukechen_patrick@foxmail.com 给我们发送电子邮件。



## 作者和致谢

作者：

- 来自武汉理工大学的 陈禹轲
- 来自武汉理工大学的 沈明轩
- 来自武汉理工大学的 余孜卓



我们要感谢武汉理工大学为我们提供了一个合作和合作的机会。

我们要感谢武汉理工大学的教授，刘钢老师，激发了我对创新技术发展的兴趣。
