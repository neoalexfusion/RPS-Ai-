# Rock-Paper-Scissors Game with AI and Hand Tracking

Welcome to the documentation for the Rock-Paper-Scissors game built with AI and real-time hand gesture recognition. This guide will walk you through the project’s features, setup instructions, and the underlying code.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [Code Walkthrough](#code-walkthrough)
   - [Importing Libraries](#importing-libraries)
   - [Setting Up the Camera](#setting-up-the-camera)
   - [Hand Tracking with MediaPipe](#hand-tracking-with-mediapipe)
   - [Classifying Hand Gestures](#classifying-hand-gestures)
   - [AI Move and Decision Logic](#ai-move-and-decision-logic)
   - [AI Voice Feedback](#ai-voice-feedback)
   - [The Main Game Loop](#the-main-game-loop)
6. [Conclusion](#conclusion)

## Introduction
This project is a fun and interactive Rock-Paper-Scissors game where you can challenge an AI opponent. The AI uses your webcam to recognize your hand gestures in real-time, decides its move, and announces the result through voice feedback. It's a great demonstration of how computer vision and AI can be integrated into a simple yet engaging game.

## Features
- **Real-time Hand Tracking:** Recognizes gestures like rock, paper, and scissors using your webcam.
- **AI Opponent:** The AI randomly selects its move and competes against you.
- **Voice Feedback:** The AI announces the game results using Google Text-to-Speech.
- **Optimized Performance:** Designed to run smoothly with built-in performance enhancements.

## Technologies Used
- **Python**
- **OpenCV:** For video capture and frame processing.
- **MediaPipe:** For hand tracking and gesture recognition.
- **Google Text-to-Speech (gTTS):** For converting text to spoken words.

## Setup Instructions

### Clone the Repository:
```bash
git clone https://github.com/neoalexfusion/RPS-Ai-.git
