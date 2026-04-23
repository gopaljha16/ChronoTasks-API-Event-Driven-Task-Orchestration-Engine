import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { createTask, updateTask } from '../store/slices/taskSlice';
import { toast } from 'react-toastify';
import api from '../services/api';

const TaskModal = ({ isOpen, onClose, task = null }) => {
  const dispatch = useDispatch();
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'pending',
    priority: 'medium',
    assigned_to_id: '',
    due_date: '',
  });

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description,
        status: task.status,
        priority: task.priority,
        assigned_to_id: task.assigned_to?.id || '',
        due_date: task.due_date ? task.due_date.slice(0, 16) : '',
      });
    }
  }, [task]);

  useEffect(() => {
    // Fetch users for assignment - this would need a users endpoint
    // For now, we'll use a placeholder
    const fetchUsers = async () => {
      try {
        // This endpoint doesn't exist in the backend, so we'll handle gracefully
        const response = await api.get('/auth/users/');
        setUsers(response.data);
      } catch (error) {
        // Silently fail - users can still create tasks without assignment
        console.log('Users endpoint not available');
      }
    };
    fetchUsers();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const taskData = {
      ...formData,
      assigned_to_id: formData.assigned_to_id || null,
      due_date: formData.due_date || null,
    };

    try {
      if (task) {
        const result = await dispatch(updateTask({ id: task.id, data: taskData }));
        if (updateTask.fulfilled.match(result)) {
          toast.success('Task updated successfully');
          onClose();
        }
      } else {
        const result = await dispatch(createTask(taskData));
        if (createTask.fulfilled.match(result)) {
          toast.success('Task created successfully');
          onClose();
        }
      }
    } catch (error) {
      toast.error('An error occurred');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              {task ? 'Edit Task' : 'Create New Task'}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                className="input-field"
                placeholder="Enter task title"
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows={4}
                className="input-field"
                placeholder="Enter task description"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
                  Status *
                </label>
                <select
                  id="status"
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  required
                  className="input-field"
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>

              <div>
                <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-2">
                  Priority *
                </label>
                <select
                  id="priority"
                  name="priority"
                  value={formData.priority}
                  onChange={handleChange}
                  required
                  className="input-field"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="assigned_to_id" className="block text-sm font-medium text-gray-700 mb-2">
                  Assign To
                </label>
                <select
                  id="assigned_to_id"
                  name="assigned_to_id"
                  value={formData.assigned_to_id}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="">Unassigned</option>
                  {users.map((user) => (
                    <option key={user.id} value={user.id}>
                      {user.first_name} {user.last_name} ({user.email})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 mb-2">
                  Due Date
                </label>
                <input
                  type="datetime-local"
                  id="due_date"
                  name="due_date"
                  value={formData.due_date}
                  onChange={handleChange}
                  className="input-field"
                />
              </div>
            </div>

            <div className="flex gap-3 pt-4">
              <button type="submit" className="btn-primary flex-1">
                {task ? 'Update Task' : 'Create Task'}
              </button>
              <button type="button" onClick={onClose} className="btn-secondary flex-1">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TaskModal;
