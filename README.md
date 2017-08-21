# lctc-ceph-performance-workbench
####Ceph performance test workbench for LCTC

- LCTC test team need a workbench to test ceph performance via GUI, which may support auto-deployment, parameter-setting and etc.
- We will lauch a project: lctc-ceph-performance-workbench, which is a website.
- The architecture of website mainly consists of separated frontend(Reactor) and backend(Django), frontend is responsible for GUI, and backend is responsible for data. Frontend send HTTP request to backend to fetch JSON data.
