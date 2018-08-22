import datetime
import reproducible

message ="""\
# Those are the full and exact requirements, as installed when the results were
# generated. Note that all present here not listed in the `requirements.txt` file
# are dependencies.
"""

reproducible.export_requirements('requirements_strict.txt', message)
