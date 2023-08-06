DevOps. Jenkins-job-builder plug-in for creating dashboards in Jenkins Job Builder.

This is for Jenkins dashboard plug-in https://plugins.jenkins.io/dashboard-view/

Example of code in Job Builder YAML file.

```
- view:
    name: product/tests/Frontend_dashboard
    view-type: dashboard
    description: "Frontend Dashboard View"
    filter-executors: true
    filter-queue: true
    job-name:
      - qa_tests/test1
      - qa_tests/test2
      - qa_tests/test3
      - qa_tests/test4
      - qa_tests/test5
      
- view:
    name: product/tests/Backend_dashboard
    view-type: dashboard
    description: "Backend Dashboard View"
    filter-executors: true
    filter-queue: true
    job-name:
      - qa_tests/test1
      - qa_tests/test2
```
