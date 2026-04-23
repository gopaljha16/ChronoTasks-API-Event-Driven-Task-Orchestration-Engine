# ChronoTasks Frontend

A professional React-based frontend application for the ChronoTasks task management system.

## Features

- **Authentication**: Login and registration with JWT tokens
- **Task Management**: Create, read, update, and delete tasks
- **Advanced Filtering**: Filter tasks by status, priority, search terms
- **Real-time Updates**: Redux state management for seamless data flow
- **Event Logging**: Admin-only event tracking and monitoring
- **Responsive Design**: Mobile-friendly UI with Tailwind CSS
- **Professional UI**: Clean, modern interface with smooth animations

## Tech Stack

- **React 18**: Modern React with hooks
- **Redux Toolkit**: State management with RTK Query
- **React Router v6**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client with interceptors
- **date-fns**: Date formatting and manipulation
- **React Toastify**: Toast notifications

## Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Update `.env` with your API URL (default is `http://localhost:8000/api`):
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Running the Application

Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

## Building for Production

Create an optimized production build:
```bash
npm run build
```

The build files will be in the `build/` directory.

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Layout.jsx          # Main layout with sidebar
│   │   └── TaskModal.jsx       # Task create/edit modal
│   ├── pages/
│   │   ├── Dashboard.jsx       # Dashboard with stats
│   │   ├── Events.jsx          # Event log (admin only)
│   │   ├── Login.jsx           # Login page
│   │   ├── Register.jsx        # Registration page
│   │   ├── TaskDetail.jsx      # Task detail view
│   │   └── Tasks.jsx           # Task list with filters
│   ├── services/
│   │   └── api.js              # Axios instance with interceptors
│   ├── store/
│   │   ├── slices/
│   │   │   ├── authSlice.js    # Authentication state
│   │   │   ├── eventSlice.js   # Events state
│   │   │   └── taskSlice.js    # Tasks state
│   │   └── store.js            # Redux store configuration
│   ├── App.js                  # Main app component
│   ├── index.css               # Global styles with Tailwind
│   └── index.js                # App entry point
├── .env.example
├── package.json
├── postcss.config.js
├── tailwind.config.js
└── README.md
```

## Features Overview

### Authentication
- User registration with email validation
- Secure login with JWT tokens
- Automatic token refresh
- Protected routes

### Dashboard
- Overview statistics (total tasks, my tasks, pending, completed)
- Recent tasks list
- My assigned tasks
- Quick navigation

### Task Management
- Create new tasks with title, description, status, priority, assignment, and due date
- View all tasks in a table format
- Filter by status, priority, and search terms
- Sort by various fields
- Edit and delete tasks (with permissions)
- Mark tasks as completed
- Detailed task view with full information

### Event Log (Admin Only)
- View all system events
- Filter by event type
- Sort by timestamp or event type
- Detailed metadata for each event

### UI/UX Features
- Responsive design for all screen sizes
- Collapsible sidebar navigation
- Toast notifications for user feedback
- Loading states and error handling
- Color-coded status and priority badges
- Smooth transitions and animations

## API Integration

The frontend integrates with the following backend endpoints:

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh access token

### Tasks
- `GET /api/tasks/` - List all tasks (with filters)
- `GET /api/tasks/:id/` - Get task details
- `POST /api/tasks/` - Create new task
- `PATCH /api/tasks/:id/` - Update task
- `DELETE /api/tasks/:id/` - Delete task
- `GET /api/tasks/my_tasks/` - Get my assigned tasks
- `GET /api/tasks/created_by_me/` - Get tasks I created
- `PATCH /api/tasks/:id/mark_completed/` - Mark task as completed

### Events (Admin Only)
- `GET /api/events/` - List all events (with filters)
- `GET /api/events/:id/` - Get event details

## State Management

The application uses Redux Toolkit for state management with three main slices:

1. **authSlice**: Manages authentication state, user data, and tokens
2. **taskSlice**: Manages tasks, filters, and pagination
3. **eventSlice**: Manages events and event filters

## Styling

The application uses Tailwind CSS with custom utility classes:

- `.btn-primary` - Primary action buttons
- `.btn-secondary` - Secondary action buttons
- `.btn-danger` - Destructive action buttons
- `.input-field` - Form input fields
- `.card` - Card containers

## Environment Variables

- `REACT_APP_API_URL` - Backend API base URL (default: `http://localhost:8000/api`)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Tips

1. **Hot Reload**: Changes are automatically reflected in the browser
2. **Redux DevTools**: Install Redux DevTools extension for debugging
3. **React DevTools**: Install React DevTools extension for component inspection
4. **API Proxy**: The `proxy` field in `package.json` handles CORS during development

## Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure the backend has proper CORS configuration for `http://localhost:3000`

### Token Expiration
The app automatically refreshes tokens. If you're logged out unexpectedly, check the backend token expiration settings.

### API Connection
Verify the backend is running on `http://localhost:8000` and the `REACT_APP_API_URL` is correctly set.

## License

This project is part of the ChronoTasks system.
