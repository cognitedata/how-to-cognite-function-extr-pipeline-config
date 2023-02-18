# Introduction

Cognite Functions provide a run-time environment for hosting and running Python code, similar to Azure Functions, Google Cloud Functions, or Amazon Lambda. 
The benefit of utilizing the built in Functions capability of CDF is that it is tightly coupled with CDF and gives you as a developer an implicit Cognite 
client allowing you to seamlessly interact with your CDF data and data pipeline. 

CDF extraction pipelines allow you to monitor the data flow and gain visibility into the run history and receive notifications from data integration 
events that need to be paid attention to, all of which is an important part of the resulting data quality. CDF extraction pipelines offer a great 
feature for storing extractor configuration settings, allowing you to remotely configure the extractor.

# Setting up the Cognite Function

In this example we’ll create a Cognite Function that emits a simple Sine curve into a time series in CDF.
As the function runs, we’d like to adjust the amplitude and frequency of the curve. Our function should also take the time series external_id 
and name as input from the configuration.

The function will write time series data 


# Deployment of the function

The function is uploaded to the Files API as a zip file with the Python file called handler.py. Handler.py contains a function named handle with 
any of the following arguments: data, client, secrets, or 'function_call_info', which are passed into the function. The latest version of Cognite 
SDK's are available, and additional python packages and version specifications can be defined in a requirements.txt in the root of the zip.


The created zip file is then uploaded to the Cognite Data Fusion UI 