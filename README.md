# QA-covid19

QA-covid19 is a Question Answering System based on KG (Knowledge Graph) and NLP (Natural Language Processing).



## Introduction

A knowledge graph, also known as a semantic network, represents a network of real-world entities—i.e. objects, events, situations, or concepts—and illustrates the relationship between them. This information is usually stored in a graph database and visualized as a graph structure, prompting the term knowledge “graph.”

We used a [covid19 knowledge graph](http://openkg.cn/dataset/covid-19-baike) from openKG.cn to build our system.

Different from other projects, we use a NER model and classifier to process the question.

QIC (Query Intent Classification) dataset and NER dataset is from [CBLUE(Chinese Biomedical Language Understanding Evaluation)](https://tianchi.aliyun.com/cblue) 



### Summary 

Project structure

```file tree
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
|  |
├─Graph
│  │  build_graph.py
│  │  __init__.py
```



- app/  		 provides web service of our system, including web page and API service.
- QA_app 	provides a robot who can answer medical problems related to covid19.
-  classifier_model.py	 trains the QIC (Query Intent Classification) model
- graph  	  builds the KG in neo4j database



### Features 

We design the QA system with NER model and classifier instead of pre-set rules and keywords, which would help our robot answer much more related questions.



## Requirements 

Windows and Linux system are both supported, but you have to meet following requirements:

- python 3.7 +
- tensorflow 2.5.0 +
- tensorflow-text 2.5.0 +
- py2neo 4.2.0 +
- neo4j 4.2.0  +

Besides, we recommend that you prepare a GPU with at lest 4GB Graphics RAM before running our system.



## Installation & Usage 

You can install our system by following steps:

downloads:

`git clone git@github.com:Patrick-CH/QA-covid19.git`

build the KG:

`python ~/Graph/build_graph.py`

run our system:

`python ~/app.py `



## Development 

Our system provide both web page and API service.

web page:	visit localhost:80 and you can see the web page.

API definition:

| method | path  | form-data                        | response                  |
| :----- | :---- | :------------------------------- | :------------------------ |
| POST   | /chat | {"question": "example question"} | {"ans": "example answer"} |



## Changelog

V0: Our first version to validate the system framework.

V1: First publish version with relative abundant function.



## Branches

- Product (master ): stable version
- Develop (dev branch): latest version
- Feature : add new features (under development)
- Release : public release (under development)



## Reference

[1] CBLUE: A Chinese Biomedical Language Understanding Evaluation Benchmark [[github](https://github.com/CBLUEbenchmark/CBLUE)] [[website]([https://tianchi.aliyun.com/cblue)]

[2] COVID-19 Open Knowledge Graph. encyclopedia [[website](http://openkg.cn/dataset/covid-19-baike)]



### Contact 

Feel free to email us through chenyuke@whut.edu.cn or yukechen_patrick@foxmail.com, if you have any question or suggestion.



## Authors and acknowledgment

Authors:

- Yuke Chen 			from WHUT
- Mingxuan Shen    from WHUT
- Zizhuo Yu              from WHUT



We would like to thank WHUT for providing us an opportunity to team up and work together.

I would like to acknowledge Professor, Doc. Liu, for inspiring my interest in the development of innovative technologies.
