# Template Invoker

This Python script automates the generation and building of Docker images based on predefined templates and combinations specified in CSV files. It reads the template and combination data, generates image properties, and invokes Docker commands to build and push the images to a Docker registry.

## Requirements

- Python 3.x
- Docker
- `csv` module

## Setup

1. **CSV Files**: Prepare two CSV files:

   - `version - Sheet1.csv`: Contains template versions.
   - `combination - Sheet1.csv`: Specifies combinations of templates.

2. **Configure Variables**: Customize the following variables in the script according to your environment:

   - `versions_path`: Path to the CSV file containing template versions.
   - `combinations_path`: Path to the CSV file specifying combinations.
   - `nexus_url`: URL of the Docker registry.
   - `base_directory`: Base directory for storing Docker images.

3. **Dockerfile Templates**: Ensure that Dockerfile templates are available for each template specified in the combinations.

## Usage

1. **Run the Script**: Execute the script `template_invoker.py` in your Python environment.

   ```
   python template_invoker.py
   ```

2. **Review Output**: The script will display the Docker build and push commands as it processes the combinations and builds Docker images.

## Dockerfile Examples

The script assumes the presence of Dockerfile templates in folders corresponding to each template. Here are some examples:

### Alpine Folder Dockerfile

```Dockerfile
ARG alpine

FROM alpine:$alpine

# Add your Alpine specific configurations here
```

### Ubuntu Folder Dockerfile

```Dockerfile
ARG ubuntu

FROM ubuntu:$ubuntu

# Add your Ubuntu specific configurations here
```

### Node Folder Dockerfile

```Dockerfile
ARG node

FROM node:$node

# Add your Node.js specific configurations here
```

## Additional Notes

- Ensure that Docker is properly configured and running on the host machine.
- Customize the Dockerfile templates according to your application requirements.
- Regularly update the CSV files with new template versions and combinations as needed.

