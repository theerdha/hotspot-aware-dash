# This module randomly selects N trace files from the set of traces, for sample experiments.

import os
import sys
import shutil
import random

files = os.listdir("../cooked_traces_all")
selected = random.sample(files, 30)

for f in selected:
    src = os.path.join("../cooked_traces_all", f)
    dst = os.path.join("../cooked_traces", f)
    shutil.copyfile(src, dst)
