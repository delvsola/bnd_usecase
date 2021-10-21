import os

with open("submission.csv", "w") as f:
    f.write("Id,Expected\n")

    has_sign = list(map(
        lambda x: x.replace(".txt", ""),
        list(os.listdir("runs/detect/exp/labels")
             )))

    for file in os.listdir("datasets/images/test"):
        fn = file.replace(".tif", "")
        if fn in has_sign:
            out = f"{fn},1"
        else:
            out = f"{fn},0"
        f.write(out+"\n")
