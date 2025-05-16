# Nova Sonic Smoke Test

## Purpose
The primary goal of this smoke test is to verify basic accessibility of the Amazon Nova Sonic speech-to-speech model. This includes ensuring that the system can successfully:
- Establish a connection with the Amazon Bedrock service.
- Verify the Nova Sonic model is available in your account.
- Confirm you have the necessary permissions to access the model.
- Check provisioned throughput (if any).

## Implementation Details
The smoke test is implemented in `run_smoke_test.py` and follows this approach:

1. **Configuration Management**
   - Configuration is loaded from `config/settings.json`
   - Includes model ID and region settings
   - Fallbacks to environment variables if config file not found

2. **Model Accessibility Verification**
   - Lists available foundation models to check if Nova Sonic is available
   - Verifies IAM permissions by attempting to access model details
   - Checks for provisioned throughput (optional)
   - Reports all accessible models if Nova Sonic isn't found

3. **Reporting**
   - Provides detailed logging of each verification step
   - Reports success/failure with clear indications
   - Lists alternative models if the target model isn't found

## Note on Bidirectional Streaming
This simplified smoke test focuses on verifying model accessibility rather than actual speech-to-speech interaction. The original implementation attempting to use `invoke_model_with_response_stream` was not compatible with Nova Sonic, as it requires a bidirectional streaming API rather than response streaming.

For a full interaction test with audio input/output, you would need to:
1. Use the AWS SDK for Bedrock Runtime with bidirectional streaming support
2. Implement the appropriate event sequence as shown in the AWS samples

## Prerequisites
- AWS CLI configured with valid credentials and default region.
- Python 3.x installed.
- Boto3 (AWS SDK for Python) installed: `pip install boto3`
- Necessary IAM permissions to access Amazon Bedrock and list/describe the Nova Sonic model. Nova Sonic is available in `us-east-1` (N. Virginia).

## How to Run the Test
1. Navigate to the `nova_sonic_smoke_test` directory:
   ```bash
   cd nova_sonic_smoke_test
   ```
2. Ensure any required configuration (e.g., in the `config/` directory or via environment variables) is set up if not using defaults.
3. Execute the test script:
   ```bash
   ./run_smoke_test.py
   ```
   or
   ```bash
   python run_smoke_test.py
   ```

## Expected Behavior and How to Interpret Results
- **Successful Execution**:
    - The script will log information about the Nova Sonic model
    - No errors or exceptions will be printed.
    - You will see: "u2705 SMOKE TEST PASSED: The Nova Sonic model is accessible from your environment."

- **Failure Scenarios**:
    - Model not found: The script will list available models to help identify the correct model ID
    - Permission errors: Indicates IAM issues that need to be resolved
    - Connection failures: Could indicate network problems or AWS service issues

## Customization
The test can be customized by:
1. Editing the `config/settings.json` file to modify parameters
2. Adding environment variables to override settings (MODEL_ID, AWS_REGION) 