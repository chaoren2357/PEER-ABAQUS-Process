
from autoUtils import *
from utils import *
import glob
import time

logger = Logger()

all_file = list(glob.glob('*.inp'))

for idx,inpfile_path in enumerate(all_file):
    name = os.path.splitext(os.path.basename(inpfile_path))[0]
    logger.debug("Start datacheck {} >>".format(name))
    datacheck(inpfile_path,logger)
    logger.debug("End datacheck {} <<".format(name))
    if idx % 5 == 0:
        time.sleep(60*1)
    
logger.debug("Finish all datacheck")
