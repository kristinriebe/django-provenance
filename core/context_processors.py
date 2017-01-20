import subprocess
import logging
from datetime import datetime

def last_revision_date(request):
    """Get datetime of the last commit, useful for checking version on webpage"""
    # if registered in settings.py, it will be applied to each and every context!!

    # works only for development server, produces error in 'real' server environment
    cmd = "git show -s --format=%ci"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    logger = logging.getLogger(__name__)

    if error:
        logger.error(str(datetime.now()) + ": An error occured in last_revision_date context processor: " + error)

    return {'last_revision_date': output}
