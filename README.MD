# G-code Calculator API

This API calculates the optimal layer to stop a 3D print to plan a filament cut, given a desired excess length.

## Local Development

1. **Set up a virtual environment:**
   ```bash
   python3.9 -m venv .venv
   source .venv/bin/activate
   ```
    
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app:**
   ```bash
   python main.py
   ```

## API Endpoints

**POST /**

*   Uploads a G-code file and calculates the optimal layer to stop for a given cut length.

**Request body:**

*   `file`: G-code file (multipart/form-data)
*   `cutLength`: Desired excess length in meters (number)

**Response body:**

*   `result`: Object containing calculation results (if successful)
*   `error`: Error message (if an error occurred)

## Deployment to Google Cloud Functions

1. **Install gcloud CLI:**
   [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

2. **Initialize gcloud CLI:**
   ```bash
   gcloud init
   ```

3. **Deploy the function:**
   ```bash
   gcloud functions deploy process_gcode \
     --runtime python39 \
     --trigger-http \
     --allow-unauthenticated \
     --source . \
     --entry-point process_gcode \
     --project your-project-id  # Replace with your actual project ID
   ```

## Requirements

*   Python 3.9
*   Flask
*   flask_cors

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```

**Explanation**

*   Local development: Provides instructions on setting up a virtual environment and running the Flask app locally.
*   API endpoints: Describes the API endpoint, including request and response formats.
*   Deployment: Outlines the steps to deploy the API to Google Cloud Functions.
*   Requirements: Lists the necessary dependencies.
*   Contributing: Encourages contributions and provides guidelines.
*   License: Specifies the license under which the code is distributed.

Remember to replace placeholders like `your-project-id` with your actual values.