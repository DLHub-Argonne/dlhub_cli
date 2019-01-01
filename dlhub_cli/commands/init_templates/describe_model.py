"""
A template for creating a DLHub-compatible description of a model.

The places where you need to fill in information are marked with "TODO" comments
"""

# TODO: Import a metadata template appropriate for your type of model
from dlhub_sdk.models import BaseMetadataModel
from dlhub_sdk.utils.schemas import validate_against_dlhub_schema
import json

# Read in model from disk
# TODO: Fill in options specific to this type of model
model_info = BaseMetadataModel.create_model(None)

# TODO: Give the model a name and a title
model_info.set_title("A descriptive title of your model")
model_info.set_name("a_short_name")

# TODO: Provide authorship information
model_info.set_authors(["Scientist, B"], "Argonne National Laboratory")

# TODO: Describe the scientific purpose of the model
model_info.set_domains(["some", "pertinent", "fields"])
model_info.set_abstract("A longer description of the model")

# TODO: Add references for the model
# model_info.add_related_identifier("DOI", "10.", "IsDescribedBy")  # Example: Paper describing the model

# TODO: Describe the computational environment
# Basic route: Add a specific Python requirement
# model.add_requirement('numpy', 'detect')
# Advanced: Include repo2docker config files in submission
# model.parse_repo2docker_configuration()  # You can specify a different path for config files

# TODO: Describe the inputs and outputs of the model

# Check the schema against a DLHub Schema
validate_against_dlhub_schema(model_info.to_dict(), 'servable')

# Save the metadata
with open('dlhub.json') as fp:
    print(json.dumps(model_info.to_dict()))
    json.dump(model_info.to_dict(save_class_data=True), fp, indent=2)
