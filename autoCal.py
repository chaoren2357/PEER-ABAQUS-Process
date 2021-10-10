
from autoUtils import *
from utils import *
import glob
import time


logger = Logger()

all_file = list(glob.glob('*.inp'))

for idx,inpfile_path in enumerate(all_file):
    name = os.path.splitext(os.path.basename(inpfile_path))[0]
    logger.debug("Start calculate {} >>".format(name))
    calculate(inpfile_path,logger)
    logger.debug("End calculate {} <<".format(name))
    if idx % 5 == 4:
        time.sleep(60*30)
logger.debug("Finish all calculate")