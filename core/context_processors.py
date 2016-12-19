import subprocess

def last_revision_date(request):
    """Get datetime of the last commit, useful for checking version on webpage"""
    # if registered in settings.py, it will be applied to each and every context!!

    cmd = "git show -s --format=%ci"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    # print "output: ", output
    # print "error: ", error
    if error:
        print "An error occured in last_revision_date context processor: ", error

    return {'last_revision_date': output}
