# Clixove Library

A Knowledge Induction Software for Academic Papers

![](https://img.shields.io/badge/dependencies-bootstrap%205.0.0%20beta2-blue)

![](https://img.shields.io/badge/dependencies-python%203.8-blue)

![](https://img.shields.io/badge/tests-Microsoft%20Edge%2089%20%E2%9C%94-brightgreen)

## Introduction

**Easy to use -- Click and solve all problems.**

Though many academic management software have the synchronization function, it sometimes causes problems. For example, according to the description of my professor, once all of his project folders in one of the software disappear, so he could not distinguish papers of different projects. And, it costs a lot of time of him to organize these papers again.

Most people just want to organize these papers without the need of complex functions, and the complex functions mentioned above will cause many problems but little benefits. Therefore, Clixove Library is suitable as a platform which is open-source and simple enough, and is fully based on the cloud storage to manage personal academic papers.

Next step:

- [ ] Connect open-source papers (eg. arXiv), and analyze them without saving to Clixove storage.

**Intelligence -- Use neural networks to conclude knowledge.**

The software is convenient to install extensions in fields of natural language processing. To be detailed, developers can add buttons in the library page in the paper management app, and imitate the "delete" function to create the new "analyze" function. The button will transmit the file path of selected academic papers to the main function of each advanced algorithm.

With this tool, everyone is able to link neural network models to customize new text analysis algorithms, since Clixove Library is made by Python, and is compatible to these models.

Next step:

- [ ] Text summary algorithm

## Installation

Make sure that all dependencies in the heading are satisfied.

```
pip install -r requirement.txt
python build_file_tree.py
python manage.py migrate
python manage.py runserver 0.0.0.0:[port]
```

Open your browser and visit `localhost:[port]`.

## Basic usage

Hold down “Control”, or “Command” on a Mac, to select more than one in a "select multiple widget".

The check mark (refer to [Emoji](http://www.unicode.org/emoji/charts/full-emoji-list.html#other-symbol), No.1450) means "select all", and the cross mark (refer to [Emoji](http://www.unicode.org/emoji/charts/full-emoji-list.html#other-symbol), No.1451) means "unselect all".

