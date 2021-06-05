[![melanoma web application](https://github.com/prudhvirajboddu/deployment_pipeline/actions/workflows/docker-image.yml/badge.svg?branch=master)](https://github.com/prudhvirajboddu/deployment_pipeline/actions/workflows/docker-image.yml)

# Melanoma Detection

### About

Project Aim is to build a web application for Detection of Melanoma

### Dataset

Dataset is available on Kaggle .You can find it [here](https://www.kaggle.com/c/siim-isic-melanoma-classification/data)

### Training
Experimental training  on both GPUs and TPUs   [training code](https://github.com/prudhvirajboddu/training)

Converted to Tflite file for optimization and ran inference

## Deployment

To Run this locally using docker

```bash
  docker run melanoma:latest
```
### Hosted on Azure container instances 

check this [out](http://melanoma.centralindia.azurecontainer.io:5000/)
  
