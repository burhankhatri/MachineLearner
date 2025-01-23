# Machine Learner

An AI-powered machine learning platform that learns and fixes itself.

## Features

- Self-learning capabilities
- Automated model training and optimization
- Real-time monitoring and metrics
- Interactive web interface
- Support for multiple ML frameworks (TensorFlow, PyTorch, scikit-learn)

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- E2B API Key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd machine-learner
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Create a `.env` file in the root directory and add your E2B API key:
```
E2B_API_KEY=your_api_key_here
```

## Directory Structure

```
machine-learner/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Core functionality
│   ├── services/     # Service modules
│   └── frontend/     # Frontend components
├── static/
│   ├── css/          # Stylesheets
│   └── js/           # JavaScript files
├── templates/        # HTML templates
├── models/          # Saved models
├── data/           # Dataset storage
└── logs/           # Application logs
```

## Usage

1. Start the development server:
```bash
npm start
```

2. Build frontend assets:
```bash
npm run build
```

3. Access the web interface at `http://localhost:8000`

## API Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

1. The application uses FastAPI for the backend and React for the frontend
2. TailwindCSS is used for styling
3. ML operations are handled in isolated sandboxes using E2B

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 