import logging
import traceback
import yaml
import arrow
import numpy as np

from cognite.client.data_classes import (
    ExtractionPipelineRun,
    TimeSeries,
)

from cognite.logger import configure_logger

# Configure application logger (only done ONCE):
configure_logger(logger_name="func", log_json=False, log_level="INFO")

# The following line must be added to all python modules (after imports):
logger = logging.getLogger(f"func.{__name__}")
logger.info(
    "---------------------------------------START--------------------------------------------"
)

# static variables
functionName = "Sine Function"

# Global variables with default values
amplitude = 0.5
period = 1
ts_external_id = "cdf_hub_sine_1.num"
ts_name = "sine_1.num"
extractionPipelineExtId = "sine-function"


def handle(client, data):
    msg = ""
    logger.info(f"[STARTING] {functionName}")
    logger.info(f"[INFO] Cognite Client login status: {client.login.status()}")

    logger.info("[STARTING] Extracting input data")
    try:
        get_input_data(client, data)
        logger.info("[FINISHED] Extracting input parameters")
    except Exception as e:
        logger.error(f"[FAILED] Get state from last run. Error: {e}")
        raise e

    try:
        # Calculate new output / time series data points based on input data
        startDate, num_points = sine_calcutation(client)
        msg = f"Function: {functionName}: complete -  Number of data points : {num_points} created from : {startDate} for time series: {ts_external_id}"

        # Write status and message back to extraction pipeline
        client.extraction_pipeline_runs.create(
            ExtractionPipelineRun(
                status="success", message=msg, external_id=extractionPipelineExtId
            )
        )
    except Exception as e:
        tb = traceback.format_exc()
        msg = f"Function: {functionName}: failed - message: {repr(e)} - {tb}"
        logger.info(f"[FAILED] {msg}")
        # message sent to the extraction pipeline could only be 1000 char - so make sure it's not longer.
        if len(msg) > 1000:
            msg = msg[0:995] + "..."

        # Write error and message back to extraction pipeline
        client.extraction_pipeline_runs.create(
            ExtractionPipelineRun(
                status="failure", message=msg, external_id=extractionPipelineExtId
            )
        )
        return {"error": e.__str__(), "status": "failed"}

    logger.info(f"[FINISHED] {functionName} : {msg}")

    return {"status": "succeeded"}


#
# read input data from data block extracted from the Extraction Pipeline Configuration
#
def get_input_data(client, data):
    global amplitude, period, ts_external_id, ts_name, extractionPipelineExtId

    # Read ExtractionPipelineExtId from the function run time configuration. 
    # Need this value to find the function configuration provided as part of the Extraction pipelines
    if "ExtractionPipelineExtId" in data:
        extractionPipelineExtId = data["ExtractionPipelineExtId"]
    else:
        logger.info(
            f"[INFO] ExtractionPipelineExtId not found in input function configuration, using default value: {period}"
        )

    # Connect to the Extraction pipeline to read the function configuration
    try:
        pipeline_config_str = client.extraction_pipelines.config.retrieve(
            extractionPipelineExtId
        )
        if pipeline_config_str and pipeline_config_str != "":
            data = yaml.safe_load(pipeline_config_str.config)["data"]
        else:
            raise Exception("No configuration found in pipeline")
    except Exception as e:
        logger.error(
            f"[ERROR] Not able to load pipeline : {extractionPipelineExtId} configuration - {e}"
        )
        
    # Read the configuration provided as part of the Extraction pipeline configuration
    logger.info(
        f"[INFO] Config from pipeline: {extractionPipelineExtId} - data: {data}"
    )

    if "amplitude" in data:
        amplitude = data["amplitude"]
    else:
        logger.info(
            f"[INFO] amplitude not found in input configuration in pipeline {extractionPipelineExtId}, using default value: {amplitude}"
        )

    if "period" in data:
        period = data["period"]
    else:
        logger.info(
            f"[INFO] period not found in input configuration in pipeline {extractionPipelineExtId}, using default value: {period}"
        )

    if "ts_external_id" in data:
        ts_external_id = data["ts_external_id"]
    else:
        logger.info(
            f"[INFO] ts_external_id not found in input configuration in pipeline {extractionPipelineExtId}, using default value: {ts_external_id}"
        )

    if "ts_name" in data:
        ts_name = data["ts_name"]
    else:
        logger.info(
            f"[INFO] ts_name not found in input configuration in pipeline {extractionPipelineExtId}, using default value: {ts_name}"
        )



#
#  sine_calcutation - use input data to calculate and create (if not existing) time series with data points
#
def sine_calcutation(client):
    # In case TS exists, just make sure it's removed and recreated with the new data points
    if client.time_series.retrieve(external_id=ts_external_id):
        client.time_series.delete(external_id=ts_external_id)

    # Get the data set ID, used to connect the time series created
    ExtPipe = client.extraction_pipelines.retrieve(external_id=extractionPipelineExtId)
    
    # Get the time now and create data for the previous day
    startDate = arrow.utcnow()  # Now - data & time today
    start = startDate.format()  # Readable string date format
    startSine = startDate.int_timestamp * 1000  # Start time as Int timestamp in milliseconds

    logger.info(
        f"[START] Calculate Sine curve data points, for one day starting at: {start}"
    )

    logger.info(
        f"[INFO] For calculation use, amplitude: {amplitude} (cure hight) and periods: {period} (number of curves)"
    )

    # define array of 86400 time samples for input parameter periods
    time = np.linspace(0, period, 86400)
    # create sine cure for provided time array and adjusted to input parameter amplitude
    data = np.sin(2 * np.pi * time) * amplitude

    # Create the array of data points, and merge inn the time with the found start time 
    datapoints = []
    i = 0
    for t_, value in zip(time, data):
        t = startSine + t_ * 1000 * 60 * 60 * 24
        datapoints.append({"timestamp": t, "value": value})
        i += 1

    # Create time series
    # Note: we delete the time_series in this example just to keep it simple to view and test the function.
    client.time_series.create(
        TimeSeries(
            name=ts_name,
            external_id=ts_external_id,
            description="Function sine_wave generated time series",
            data_set_id=ExtPipe.data_set_id,
        )
    )

    # Add the data points (array) to the Time Series
    client.time_series.data.insert(datapoints, external_id=ts_external_id)

    logger.info(
        f"[FINISHED] Calculate Sine curve data points, num data points: {len(datapoints)}"
    )

    return startDate, len(datapoints)
