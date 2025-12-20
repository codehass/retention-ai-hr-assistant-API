<a name="readme-top"></a>

<div align="center">
  <img src="public/logo-dark.png" alt="logo" width="140" height="auto" />
  <br/>
</div>

# 📗 Table of Contents

- [📖 About the Project](#about-project)
  - [🛠 Built With](#built-with)
    - [Tech Stack](#tech-stack)
    - [Key Features](#key-features)
  - [🚀 Live Demo](#live-demo)
- [💻 Getting Started](#getting-started)
  - [Setup](#setup)
  - [Install](#install)
  - [Usage](#usage)
  - [Login](#login)
- [👥 Authors](#authors)
- [🔭 Future Features](#future-features)
- [🤝 Contributing](#contributing)
- [⭐️ Show your support](#support)
- [📝 License](#license)

# 📖 RetentionAI – Backend API <a name="about-project"></a>

RetentionAI Backend is a secure and industrialized FastAPI application that predicts employee attrition using supervised machine learning and generates personalized retention plans using generative AI.

The API is secured with JWT authentication, persists data in PostgreSQL, and is fully containerized with Docker.

## 🛠 Built With <a name="built-with"></a>

### Tech Stack <a name="tech-stack"></a>

<ul>
  <li><a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
  <li>Python</li>
  <li>Scikit-learn</li>
  <li>PostgreSQL</li>
  <li>JWT Authentication</li>
  <li>Docker & Docker Compose</li>
</ul>

### Key Features <a name="key-features"></a>

- **Supervised ML model for attrition prediction**
- **JWT-secured authentication (register / login)**
- **Prediction endpoint returning churn probability**
- **AI-powered retention plan generation**
- **Prediction history tracking in PostgreSQL**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🚀 Live Demo <a name="live-demo"></a>

- API deployment coming soon

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 💻 Getting Started <a name="getting-started"></a>

To get a local copy up and running, follow these steps.

### Setup

Clone this repository:

```sh
git clone https://github.com/codehass/retention-ai-hr-assistant-API.git

```

### Install

Install this project with:

```sh
  cd retention-ai-hr-assistant-API
  pip install -r requirements.txt
```

create `.env` file and add your environment variables. You can copy `.env.example` as a template.

```sh
  cp .env.example .env
```

Update the .env file with your database credentials, JWT secret, and external AI API keys.

### Usage

To run the project locally, follow these steps:

1. Create the PostgreSQL database
2. Make sure PostgreSQL is running and create the database defined in your .env file.

Start the backend server

```sh
   fastapi dev app/main.py
```

To run with `docker compose` check the frontend repo [RetentionAI Frontend](https://github.com/codehass/retention-ai-hr-assistant-frontend)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 👥 Author <a name="authors"></a>

👤 **Hassan El Ouardy**

- GitHub: [@codehass](https://github.com/codehass)
- Twitter: [@hassanelourdy](https://twitter.com/hassanelourdy)
- LinkedIn: [@hassanelourdy](https://www.linkedin.com/in/hassanelouardy/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🔭 Future Features <a name="future-features"></a>

- **MLflow experiment tracking**
- **Advanced model**
- **CI/CD with GitHub Actions**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🤝 Contributing <a name="contributing"></a>

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/codehass/the-wild-oasis/issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ⭐️ Show your support <a name="support"></a>

Join us in supporting our project to improve cabin management in hotels! Your help makes a big difference in making stays smoother and guests happier. Let's work together to bring positive change to the hospitality industry!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📝 License <a name="license"></a>

This project is [MIT](./MIT.md) licensed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
