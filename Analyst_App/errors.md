PS C:\Users\DELL\Analyst> cd Analyst_App
PS C:\Users\DELL\Analyst\Analyst_App> docker-compose up --build
[+] Building 148.3s (17/17)
 => => resolve docker.io/library/python:3.10-slim-bullseye@sha256:f1fb49e4d5501ac93d0ca519fb7ee6250842245aba8612926a4  0.1s 
 => [internal] load build context                                                                                      0.2s 
 => => transferring context: 3.01kB                                                                                    0.1s 
 => CACHED [2/6] WORKDIR /app                                                                                          0.0s 
 => CACHED [3/6] RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libpq-dev    0.0s 
 => [4/6] COPY requirements.txt .                                                                                      0.2s 
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt                                                         112.0s 
 => [6/6] COPY . .                                                                                                     0.3s 
 => exporting to image                                                                                                28.6s 
 => => exporting layers                                                                                               15.3s 
 => => exporting manifest sha256:80f51243a556d925156fff33082dd054eb092b51bc26346dda37ebded9ee407e                      0.1s 
 => => exporting config sha256:dcd6cae5f2413d8f74125dcb63eda3444bc3b00acd488923d8c88cf5e5b1e621                        0.0s 
 => => exporting attestation manifest sha256:8c71c0b969c9866b5dda36d1cf7ff6d4898ff7f7a9463ea1081f10539759ebf7          0.1s 
 => => exporting manifest list sha256:5ecd767547169bc5c3f647baab08a146f6d62e25d3c5d06f7929d24e57440d6a                 0.0s 
 => => naming to docker.io/library/analyst_app-server:latest                                                           0.0s 
 => => unpacking to docker.io/library/analyst_app-server:latest                                                       12.8s 
 => resolving provenance for metadata file                                                                             1.2s 
failed to execute bake: read |0: file already closed
PS C:\Users\DELL\Analyst\Analyst_App> 