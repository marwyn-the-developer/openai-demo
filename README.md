# open-ai-demo

This simple demo project uploads an image to a Webserver (run by the Flask framework) and generates variations of the image by calling the OpenAI Rest-API (https://api.openai.com/v1). It sends a POST request to the images/variations endpoint to generate the image variations. The images uploaded must strictly be in the PNG format and the upload limit is set to 4MB.

How to run the app:
docker: docker run -e FLASK_APP=run.py -e OPENAI_API_KEY=<Your OpenAI Key> -p 5000:5000  marwynthedev/openai-demo:latest

Azure-link: https://openaidemo.azurewebsites.net

Docker-Hub: https://hub.docker.com/repository/docker/marwynthedev/openai-demo