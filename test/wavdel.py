# /tmp内にある.wavを全部削除する

import os

for file in os.listdir("/tmp"):
    if file.endswith(".wav"):
        os.remove(os.path.join("/tmp", file))