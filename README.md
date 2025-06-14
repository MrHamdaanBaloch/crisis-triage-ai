# 🚀 CrisisTriage AI: An AI-Powered Crisis Response Platform

An intelligent, real-time platform designed to revolutionize humanitarian aid by leveraging Large Language Models to instantly analyze, prioritize, and manage emergency reports from multiple channels.

---

## 📜 Project Description

In the first critical moments of a disaster, response teams are inundated with a chaotic flood of information—panicked calls, fragmented texts, and social media posts. Traditional systems are slow, manual, and unable to provide a clear, real-time operational picture. This delay can be measured in lives lost.

**CrisisTriage AI** is a proof-of-concept platform built to solve this problem. It acts as an intelligent digital first responder, using the power of modern LLMs (like Llama 3 via Groq and Novita.ai) to instantly understand natural language reports from any source. The system automatically extracts critical data, assesses the severity and urgency, assigns a priority score, and plots incidents on a live map, providing emergency dispatchers with the actionable intelligence they need to act decisively and save lives.

This project moves beyond static forms and simple data logging, creating a dynamic, end-to-end ecosystem for modern crisis management.

---

## ✨ Core Features

*   **AI-Powered Triage Engine:** Instantly parses unstructured text from any source to extract:
    *   **Location:** Geo-coordinates for mapping.
    *   **Severity:** Classifies injuries as None, Minor, Serious, or Critical.
    *   **Vulnerability:** Identifies reports involving children, the elderly, or disabled persons.
    *   **Resource Needs:** Detects requests for ambulances, firefighters, boats, etc.
*   **Dynamic Priority Scoring:** A sophisticated, multi-stage algorithm that thinks like an emergency dispatcher, heavily weighting immediate threats to life to intelligently rank all incoming incidents.
*   **Professional SaaS Dashboard:** A clean, multi-page command center built with **React** and **Material-UI**, featuring:
    *   A live, color-coded triage queue of all incidents.
    *   Detailed incident views with full AI analysis and scoring reasoning.
    *   Interactive controls to Acknowledge and Simulate Dispatch for response teams.
*   **Multi-Channel Reporting:**
    *   A clean, public-facing web form for citizen reporting.
    *   Real-time integration with **Telegram**, allowing reports to be submitted via a simple mobile message.
*   **Real-Time Notifications & Mapping:**
    *   Automatically sends high-priority alerts to a dedicated **Slack channel**.
    *   Plots all geo-tagged incidents on a live **Crisis Map** with an auto-refresh mode.
*   **AI-Powered Administrative Tools:** Includes a one-click "Fundraising Appeal Generator" that uses the context of real incidents to create compelling social media content.
*   **Cloud-Native & Scalable:** A robust architecture with a **FastAPI** backend and a **Supabase (PostgreSQL)** cloud database, ready for real-world deployment.

---

## 🛠️ Technology Stack

| Category             | Technology                                      |
| -------------------- | ----------------------------------------------- |
| **Frontend**         | React, Vite, Material-UI (MUI), Axios, React-Leaflet |
| **Backend**          | Python 3.11, FastAPI, SQLAlchemy                |
| **Database**         | Supabase (PostgreSQL)                           |
| **AI / LLMs**        | Groq (Llama 3), Novita.ai                       |
| **Notifications**    | Slack Webhooks                                  |
| **Messaging Channel**| Telegram Bot API                                |

---

## 👥 The Team

This project was developed as part of a hackathon, showcasing a powerful vision for the future of humanitarian technology.

*   **Hamdaan Baloch** - *Lead Backend Developer & System Architect*
    *   [GitHub](https://github.com/mrHamdaanbaloch)
    *   [LinkedIn](https://pk.linkedin.com/in/hamdaan-baloch-3ba3b51ab)
*   **Asif Ullah Saad** - *Presenter & Frontend Contributor*
    *   [GitHub](https://github.com/asif-ullah-saad)
    *   [LinkedIn](https://www.linkedin.com/in/asif-ullah-saad-724103154)

---

## 🚀 Deployment

This application is fully deployed on the cloud using a modern, free-tier stack:
*   **Backend:** Deployed on **Render**.
*   **Frontend:** Deployed on **Netlify**.
