# GCP-Quizz-App
# 

This repository contains the files necessary to run and manage a GCP quiz application. Below is a brief overview of each file and its purpose:

## Files Description

- `quizz_v4.py`: The main Python script for the quiz application. It uses Tkinter to provide a graphical user interface for users to take quizzes. It includes functionality to load questions from a JSON file, present them to the user, and evaluate answers.

- `strip.py`: A utility Python script designed to parse a structured text file containing questions, answers, options, and explanations. It outputs this data in JSON format, making it easy to update or add new questions to the quiz application.

- `questions_answers.json`: A JSON file that stores the CDL quiz questions, multiple-choice options, correct answers, and explanations. This file is loaded by `quizz_v4.py` to present questions to the user.

- `questions_answers_ACE.json`: Another JSON file with the ACE set of quiz questions, options, answers, and explanations. This provides an additional or alternative question set for the quiz application.

## Application Overview

The Quiz Application is designed to offer an interactive learning experience. Users can take quizzes on various topics, with questions loaded from JSON files. The application supports multiple-choice questions and provides immediate feedback on user selections. It's an excellent tool for education, training, or self-assessment.

## Features

- **Integration with ChatGPT and Gemini**: The application includes "Check with ChatGPT" and "Check with Gemini" buttons. When clicked, these buttons copy the current question to the clipboard and open the respective service in a browser, allowing users to verify the answer if unsure.
- **Quiz Modes**: Users can choose between two quiz modes:
  - **Timed Mode**: The user has a fixed amount of time to complete the quiz, enhancing the challenge by testing not only knowledge but also speed.
  - **Practice Mode**: Allows users to take the quiz without the pressure of time, focusing on learning and accuracy.


## Additional Information

- The repository also includes a ZIP file containing all necessary files compiled as a standalone Windows application. This allows users to run the quiz application on Windows without installing Python or any dependencies.

 GGCP quizz app
