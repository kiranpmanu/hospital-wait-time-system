# 🏥 Hospital Wait Time Prediction System using Machine Learning
## 📌 Overview

Long and unpredictable waiting times are a common problem in hospitals, affecting patient satisfaction and hospital efficiency. This project presents a Hospital Wait Time Prediction System that uses machine learning to estimate patient waiting time and provide decision support for hospital management.

The system predicts expected waiting time based on real-world hospital parameters such as patient urgency, queue size, peak hours, and doctor availability. It is implemented as an interactive web application with role-based access for patients and hospital administrators.

## 🔗 Live Application

**🚀 Streamlit App:**
**URL :** https://hospital-wait-time-system.streamlit.app/

## 🎯 Objectives

Predict patient waiting time using machine learning techniques

Analyze the impact of queue size, urgency level, and staffing on waiting time

Provide transparency to patients regarding expected waiting duration

Assist hospital administrators in decision-making during peak congestion

Improve hospital resource utilization and patient experience

## 🧠 Why Two Algorithms?

Linear Regression

Used as a baseline model

Simple and interpretable

Random Forest Regressor

Captures complex, non-linear relationships

Achieves higher accuracy and lower prediction error

Comparing both models ensures reliable model selection and validates the effectiveness of the final solution.

## 📊 Dataset Description

Synthetic hospital dataset simulating real-world scenarios

Dataset size: 100,000+ records

Key features:

Patient age

Urgency level (Normal / Urgent / Emergency)

Visit type

Arrival time slot

Number of patients in queue

Doctor availability

Peak hour indicator

## ⚙️ Feature Engineering

Priority Score

Derived from urgency level and patient condition

Doctor Utilization

Ratio of patients in queue to available doctors

These features improve prediction accuracy and better represent hospital dynamics.

## 🖥️ Application Features
**👤 User (Patient) Mode** 

Simple login interface

Input patient and queue details

View:

Expected waiting time

Minimum and maximum waiting range

Interactive visualizations for better understanding

**🛠️ Admin (Hospital Management) Mode**

Secure admin login

Monitor hospital load

Simulate adding doctors during peak congestion

Receive recommendations for staffing decisions

## 📈 Visualizations

Interactive graphs using Plotly

Displays:

Waiting time range (min / expected / max)

Patients vs doctors comparison

Enhances interpretability for non-technical users

## 🛠️ Technology Stack

Programming Language: Python

Machine Learning: Scikit-learn

Data Processing: Pandas, NumPy

Visualization: Plotly

Web Framework: Streamlit

Model Storage: Joblib


## 👤 Author
Kiran P
Data science profession
