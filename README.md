This repository contains the following:
- data
- detection - notebooks and model for training slate/non slate detector
- localization - notebooks and model for generating bounding boxes for slate components
- via-app - via v2 packaged in a flask app with linked database for annotation of bounding boxes in slate frames
- slate_loader.py - module to extract slate frames as annotated in the provided annotations csv in the data directory
- utils.py - helper functions