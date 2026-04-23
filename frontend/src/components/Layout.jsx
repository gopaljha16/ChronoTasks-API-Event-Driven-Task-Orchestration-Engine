import React, { useState } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../store/slices/authSlice';

const Layout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside
        className={`${
          isSidebarOpen ? 'w-64' : 'w-20'
        } bg-white shadow-lg transition-all duration-300 ease-in-out`}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between p-4 border-b">
            <h1 className={`text-2xl font-bold text-primary-600 ${!isSidebarOpen && 'hidden'}`}>
              ChronoTasks
            </h1>
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d={isSidebarOpen ? 'M11 19l-7-7 7-7m8 14l-7-7 7-7' : 'M13 5l7 7-7 7M5 5l7 7-7 7'}
                />
              </svg>
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            <Link
              to="/"
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive('/') ? 'bg-primary-50 text-primary-600' : 'hover:bg-gray-100'
              }`}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                />
              </svg>
              {isSidebarOpen && <span className="font-medium">Dashboard</span>}
            </Link>

            <Link
              to="/tasks"
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive('/tasks') ? 'bg-primary-50 text-primary-600' : 'hover:bg-gray-100'
              }`}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
              {isSidebarOpen && <span className="font-medium">Tasks</span>}
            </Link>

            {user?.role === 'admin' && (
              <Link
                to="/events"
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive('/events') ? 'bg-primary-50 text-primary-600' : 'hover:bg-gray-100'
                }`}
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                {isSidebarOpen && <span className="font-medium">Events</span>}
              </Link>
            )}
          </nav>

          {/* User Profile */}
          <div className="p-4 border-t">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center text-white font-bold">
                {user?.first_name?.[0] || user?.email?.[0]?.toUpperCase()}
              </div>
              {isSidebarOpen && (
                <div className="flex-1">
                  <p className="font-medium text-sm">
                    {user?.first_name} {user?.last_name}
                  </p>
                  <p className="text-xs text-gray-500">{user?.email}</p>
                </div>
              )}
            </div>
            {isSidebarOpen && (
              <button
                onClick={handleLogout}
                className="w-full mt-3 px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors font-medium"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
