import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchEvents } from '../store/slices/eventSlice';
import { format } from 'date-fns';

const Events = () => {
  const dispatch = useDispatch();
  const { events, loading, pagination } = useSelector((state) => state.events);
  const [filters, setFilters] = useState({
    event_type: '',
    ordering: '-timestamp',
  });

  useEffect(() => {
    dispatch(fetchEvents(filters));
  }, [dispatch, filters]);

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const getEventTypeColor = (eventType) => {
    const colors = {
      TASK_CREATED: 'bg-green-100 text-green-800',
      TASK_UPDATED: 'bg-blue-100 text-blue-800',
      TASK_COMPLETED: 'bg-purple-100 text-purple-800',
      TASK_DELETED: 'bg-red-100 text-red-800',
    };
    return colors[eventType] || 'bg-gray-100 text-gray-800';
  };

  const getEventIcon = (eventType) => {
    switch (eventType) {
      case 'TASK_CREATED':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
        );
      case 'TASK_UPDATED':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        );
      case 'TASK_COMPLETED':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'TASK_DELETED':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Event Log</h1>
        <p className="text-gray-600 mt-2">Track all system events and activities</p>
      </div>

      {/* Filters */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Event Type</label>
            <select
              value={filters.event_type}
              onChange={(e) => handleFilterChange('event_type', e.target.value)}
              className="input-field"
            >
              <option value="">All Events</option>
              <option value="TASK_CREATED">Task Created</option>
              <option value="TASK_UPDATED">Task Updated</option>
              <option value="TASK_COMPLETED">Task Completed</option>
              <option value="TASK_DELETED">Task Deleted</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
            <select
              value={filters.ordering}
              onChange={(e) => handleFilterChange('ordering', e.target.value)}
              className="input-field"
            >
              <option value="-timestamp">Newest First</option>
              <option value="timestamp">Oldest First</option>
              <option value="event_type">Event Type</option>
            </select>
          </div>
        </div>
      </div>

      {/* Events List */}
      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
          </div>
        ) : events.length === 0 ? (
          <div className="text-center py-12">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-gray-500 text-lg">No events found</p>
          </div>
        ) : (
          <div className="space-y-4">
            {events.map((event) => (
              <div
                key={event.id}
                className="flex items-start gap-4 p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:shadow-md transition-all"
              >
                <div className={`p-3 rounded-lg ${getEventTypeColor(event.event_type)}`}>
                  {getEventIcon(event.event_type)}
                </div>

                <div className="flex-1">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        {event.event_type.replace('_', ' ')}
                      </h3>
                      <p className="text-sm text-gray-600 mt-1">
                        {event.user_email && (
                          <span>
                            by <span className="font-medium">{event.user_email}</span>
                          </span>
                        )}
                        {event.task_title && (
                          <span className="ml-2">
                            • Task: <span className="font-medium">{event.task_title}</span>
                          </span>
                        )}
                      </p>
                    </div>
                    <span className="text-sm text-gray-500">
                      {format(new Date(event.timestamp), 'MMM dd, yyyy HH:mm')}
                    </span>
                  </div>

                  {event.metadata && Object.keys(event.metadata).length > 0 && (
                    <div className="mt-3 bg-gray-50 rounded p-3">
                      <p className="text-xs font-medium text-gray-500 mb-2">Metadata:</p>
                      <pre className="text-xs text-gray-700 overflow-x-auto">
                        {JSON.stringify(event.metadata, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {pagination.count > 10 && (
          <div className="mt-6 flex items-center justify-between border-t pt-4">
            <div className="text-sm text-gray-700">
              Showing <span className="font-medium">{events.length}</span> of{' '}
              <span className="font-medium">{pagination.count}</span> results
            </div>
            <div className="flex gap-2">
              {pagination.previous && (
                <button className="btn-secondary">Previous</button>
              )}
              {pagination.next && (
                <button className="btn-secondary">Next</button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Events;
