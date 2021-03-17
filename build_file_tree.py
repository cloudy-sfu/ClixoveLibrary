import os

content = ["storage", "storage/papers", "storage/static"]
[os.mkdir(x) for x in content if not os.path.exists(x)]
