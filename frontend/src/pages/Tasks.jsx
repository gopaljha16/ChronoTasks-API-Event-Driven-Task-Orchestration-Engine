import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { fetchTasks, setFilters, clearFilters } from '../store/slices/taskSlice';
import { format } from 'date-fns';
import TaskModal from '../components/TaskModal';

const Tasks = () => {
  const dispatch = useDispatch();
  const { tasks, loading, filters, pagination } = useSelector((state) => state.tasks);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    dispatch(fetchTasks(filters));
  }, [dispatch, filters]);

  const handleFilterChange = (key, value) => {
    dispatch(setFilters({ [key]: value }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    dispatch(setFilters({ search: searchTerm }));
  };

  const handleClearFilters = () => {
    setSearchTerm('');
    dispatch(clearFilters());
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      in_progress: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      low: 'bg-gray-100 text-gray-800',
      medium: 'bg-blue-100 text-blue-800',
      high: 'bg-orange-100 text-orange-800',
      urgent: 'bg-red-100 text-red-800',
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
          <p className="text-gray-600 mt-2">Manage and track all your tasks</p>
        </div>
        <button onClick={() => setIsModalOpen(true)} className="btn-primary">
          <svg className="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Create Task
        </button>
      </div>

      {/* Filters */}
      <div className="card mb-6">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search tasks..."
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
              <select
                value={filters.status}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="input-field"
              >
                <option value="">All Status</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
              <select
                value={filters.priority}
                onChange={(e) => handleFilterChange('priority', e.target.value)}
                className="input-field"
              >
                <option value="">All Priorities</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
              <select
                value={filters.ordering}
                onChange={(e) => handleFilterChange('ordering', e.target.value)}
                className="input-field"
              >
                <option value="-created_at">Newest First</option>
                <option value="created_at">Oldest First</option>
                <option value="-updated_at">Recently Updated</option>
                <option value="due_date">Due Date</option>
                <option value="priority">Priority</option>
              </select>
            </div>
          </div>

          <div className="flex gap-2">
            <button type="submit" className="btn-primary">
              Apply Filters
            </button>
            <button type="button" onClick={handleClearFilters} className="btn-secondary">
              Clear Filters
            </button>
          </div>
        </form>
      </div>

      {/* Tasks List */}
      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-12">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <p className="text-gray-500 text-lg">No tasks found</p>
            <button onClick={() => setIsModalOpen(true)} className="btn-primary mt-4">
              Create Your First Task
            </button>
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Task
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Priority
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Assigned To
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Due Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {tasks.map((task) => (
                    <tr key={task.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div>
                          <div className="font-medium text-gray-900">{task.title}</div>
                          <div className="text-sm text-gray-500 line-clamp-1">{task.description}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}>
                          {task.status.replace('_', ' ')}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {task.assigned_to ? (
                          <div>
                            <div>{task.assigned_to.first_name} {task.assigned_to.last_name}</div>
                            <div className="text-gray-500">{task.assigned_to.email}</div>
                          </div>
                        ) : (
                          <span className="text-gray-400">Unassigned</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {task.due_date ? format(new Date(task.due_date), 'MMM dd, yyyy') : '-'}
                      </td>
                      <td className="px-6 py-4">
                        <Link
                          to={`/tasks/${task.id}`}
                          className="text-primary-600 hover:text-primary-900 font-medium"
                        >
                          View Details
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {pagination.count > 10 && (
              <div className="mt-6 flex items-center justify-between border-t pt-4">
                <div className="text-sm text-gray-700">
                  Showing <span className="font-medium">{tasks.length}</span> of{' '}
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
          </>
        )}
      </div>

      {/* Task Modal */}
      {isModalOpen && (
        <TaskModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
      )}
    </div>
  );
};

export default Tasks;
