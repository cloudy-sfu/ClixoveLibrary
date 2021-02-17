# ClixoveLibrary
A Team Knowledge Base for Academic Paper

![](https://img.shields.io/badge/dependencies-Django%203.1.6-blue)
![](https://img.shields.io/badge/dependencies-bootstrap%205.0-blue)

## Introduction
Paper management systems, such as Mendeley(R), usually associate folders via a configuration file, and read the attributes of PDF files to indicate authors, the title, and keywords. Sometimes we need to share papers in teams, or between several computers at home & work, and local paper management systems don't satisfy our demands. However, if we use Google Drive(R) to share files, we cannot see authors, the title, and keywords at ONE glance. In other words, the filename doesn't include all information that we identify a paper. Additionally, we can't conclude abstract information such as the subject of the article, thus hard to name the paper until carefully read it.

As for searching for papers in the computer, we can write in the filename neither scene features (i.e. the paper that my teacher requires me to read before this Thursday), nor abstract of knowledges (i.e. the paper that introduces block chain).

Therefore, our program includes:
- Manage papers classified by research projects
- Manage research projects
- Manage a team
- Sharing papers in a team

These features are comming soon:
- Searching papers
- Mark scene features (i.e. bradge "read before Thursday")

These features are planned to be developed:
- Automatically generate abstract and key words of papers
- PDF to text
- Automatically generate knowledge graphs in paragraph & document & project levels
- Automatically find knowledges in papers <br>
(i.e. {"Machine learning": "Machine learning is the study of computer algorithms that improve automatically through experience. It is seen as a part of artificial intelligence."})

## Usage
1. Download the code 
2. Install Python>=3.7 
3. Set the project root folder as the current folder
4. Run:
```
pip install -r requirement
python build_file_tree.py
python manage.py migrate
python manage.py runserver localhost:8000
```
5. Visit `localhost:8000/home` via web browser.
