# capstone-project-2024-t3-3900h11adigitalhaven

## AI Model Installation and Testing Guide

To install the dependencies for the ai go into the ml/ directory and run

```bash
pip install -r requirements.txt
```

To run tests for AI models, follow the instructions below:

### Classification Model Tests

To verify the performance and accuracy of the classification model, navigate to the `ml` directory and execute the following command:

```bash
cd mlpytest test/classification_test.py
```

### Object detection model tests

To ensure the functionality and accuracy of the detection model, use the following command after navigating to the ml directory:

```bash
cd mlpytest test/detection_test.py
```

## Front-end Installation, Operation and Testing guide

To run the front-end of this system without using docker, please following the instruction below

### Installation and Operation

To install and use this product frontend, navigate to the `frontend` directory and execute the following command:

```bash
npm install
npm start
```

### Front-end end-to-end Testing

To test the frontend operations and components, use the following command after navigating to the ml directory and installing cypress:

```bash
npx cypress open
```
