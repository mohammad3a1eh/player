from os import walk, path

def mp3finder(autoload):
    file_s = []
    with open(autoload , "r") as f:
        paths = f.readlines()
        # print(paths)

    for path in paths:
        for root, dirs, files in walk(path.replace("\n", "")):
            for file in files:
                if file.endswith(".mp3"):
                    file_s.append(fr"{root}{file}")

    print(file_s, file)
    return file_s, file
