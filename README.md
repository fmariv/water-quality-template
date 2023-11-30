Example forest monitoring

1. Local workflow (load aoi, images -> compute -> save local)
2. Hybrid workflow (load aoi, images from cloud -> compute local -> save cloud)
3. Cloud workflow (load aoi, images from cloud -> compute cloud -> save cloud)
    - use cli to send script to cloud
    - provision infrastructure
    - run script on cloud 
    - delete infrastructure (if not persistent)

If use want an api, create the api.py file with the endpoints. We manage the deployment

Create agents in different files
- download new images
- retreive analytics and send email alerts / pdf reports / call other apis ...

Use config file to setup spai