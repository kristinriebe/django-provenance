from django.test import TestCase

# Tests for VOTableRenderer:
# no data => empty string
# provide fields (incomplete), still get correct names for all fields etc.
#  (need to use some example data for this!)
# provide tabledescription => votable contains description-element