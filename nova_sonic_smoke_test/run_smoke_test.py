#!/usr/bin/env python3
import os
import json
import uuid
import logging
import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

# Setup logging
log = logging.getLogger("nova-smoke")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

def load_config():
    """Load configuration from settings.json file."""
    config_path = os.path.join("config", "settings.json")
    if not os.path.exists(config_path):
        log.warning(f"Config file {config_path} not found, using default settings")
        return {
            "model_id": os.getenv("MODEL_ID", "amazon.nova-sonic-v1:0"),
            "region": os.getenv("AWS_REGION", "us-east-1"),
            "system_prompt": "You are a helpful assistant."
        }
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            log.info(f"Loaded configuration from {config_path}")
            return config
    except Exception as e:
        log.error(f"Error loading config from {config_path}: {e}")
        raise

def run_smoke_test():
    """Run a simplified smoke test for Nova Sonic accessibility."""
    # Load configuration
    config = load_config()
    MODEL_ID = config["model_id"]
    REGION_NAME = config["region"]
    
    log.info(f"Starting Nova Sonic accessibility test with model {MODEL_ID}")
    
    # Create the bedrock client (not bedrock-runtime)
    log.info(f"Initializing Bedrock client in region {REGION_NAME}")
    try:
        bedrock = boto3.client(
            "bedrock",  # Use bedrock for model inspection instead of bidirectional streaming
            region_name=REGION_NAME,
            config=Config(retries={"max_attempts": 3})
        )
        
        # Step 1: Try to get the model using ListFoundationModels operation
        log.info("Querying available foundation models...")
        response = bedrock.list_foundation_models()
        
        # Check if our target model is in the list
        found_model = False
        available_models = []
        for model in response.get("modelSummaries", []):
            model_id = model.get("modelId")
            available_models.append(model_id)
            if model_id == MODEL_ID:
                found_model = True
                log.info(f"✅ Found Nova Sonic model: {model_id}")
                log.info(f"Provider: {model.get('providerName')}")
                log.info(f"Output modalities: {model.get('outputModalities')}")
                log.info(f"Input modalities: {model.get('inputModalities')}")
        
        if not found_model:
            log.error(f"❌ The specified model '{MODEL_ID}' was not found in the available models.")
            log.info("Available models:")
            for model_id in available_models:
                if "nova" in model_id.lower():
                    log.info(f"   - {model_id} (potential Nova model)")
                elif "anthropic" in model_id.lower() or "claude" in model_id.lower():
                    log.info(f"   - {model_id} (Anthropic model)")
            return False
            
        # Step 2: Check if you have provisioned throughput for this model (optional)
        try:
            throughput_response = bedrock.get_foundation_model_throughput(
                modelId=MODEL_ID
            )
            log.info(f"Provisioned throughput: {throughput_response.get('provisionedThroughput')}")
        except Exception as e:
            log.warning(f"Could not check provisioned throughput: {e}")
        
        # Step 3: Verify access permissions
        log.info("Verifying IAM permissions for the Nova Sonic model...")
        try:
            # Use get_foundation_model instead of invoke 
            model_details = bedrock.get_foundation_model(modelIdentifier=MODEL_ID)
            log.info(f"✅ You have permission to access model details.")
            
            # Get customization info
            customizations = bedrock.list_custom_models()
            log.info(f"Found {len(customizations.get('modelSummaries', []))} custom models.")
            
            # Success
            log.info("\n✅ SMOKE TEST PASSED: The Nova Sonic model is accessible from your environment.")
            log.info("NOTE: This simplified test only verifies model access, not bidirectional streaming.")
            log.info("For a full smoke test, you'll need to implement aws_sdk_bedrock_runtime support.")
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            log.error(f"❌ Permission error: {error_code}: {error_msg}")
            return False
            
    except (BotoCoreError, ClientError) as e:
        log.error(f"Failed to access Bedrock service: {e}")
        return False
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        return False

def main():
    try:
        success = run_smoke_test()
        return 0 if success else 1
    except KeyboardInterrupt:
        log.info("Test interrupted by user")
        return 1
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 