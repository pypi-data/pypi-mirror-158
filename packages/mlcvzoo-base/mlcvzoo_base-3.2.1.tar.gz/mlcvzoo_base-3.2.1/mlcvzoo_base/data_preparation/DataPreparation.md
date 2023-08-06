# Copyright 2021 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

# Data Preparation

To prepare our training data we mainly use a self hosted instance of [CVAT)](https://github.com/openvinotoolkit/cvat). 
To be able to read the annotated data the main entry is 

```
src/mlcvzoo/data_preparation/AnnotationHandler.py
```

This class is used to read image and annotation information in various formats:

- Read/Write CSV files
- Read from xml files in "PASCAL VOC 1.1" Format
- Read json in "CVAT for Images 1.1" Format
- Read xml a single xml file in "COCO 1.0" Format

NOTE: These Formats are specified by CVAT. They can be specified when 
downloading annotation data from specific tasks.

#
The main configuration for the AnnotationHandler can be found at:
```
src/mlcvzoo/configuration/AnnotationHandlerConfig.py
```

