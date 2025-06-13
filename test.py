with open("files.json", "rb") as fp:
    file_name=fp.name.split(".")[0]+".txt"
    print(file_name)
