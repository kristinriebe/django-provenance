import subprocess
import logging

def last_revision_date(request):
    """Get datetime of the last commit, useful for checking version on webpage"""
    # if registered in settings.py, it will be applied to each and every context!!

    # works only for development server:
    cmd = "git show -s --format=%ci"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:  # should log this!
        print "An error occured in last_revision_date context processor: ", error

    logger = logging.getLogger(__name__)
    if error:
        logger.error("An error occured in last_revision_date context processor: "+error)

    # On server, write the data after collecting static files?
    return {'last_revision_date': output}
