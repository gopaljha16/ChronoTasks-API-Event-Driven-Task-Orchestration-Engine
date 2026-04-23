import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTaskById, updateTask, deleteTask, markTaskCompleted } from '../store/slices/taskSlice';
import { format } from 'date-fns';
import { toast } from 'react-toastify';
import TaskModal from '../components/TaskModal';

const TaskDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { currentTask, loading } = useSelector((state) => state.tasks);
  const { user } = useSelector((state) => state.auth);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  useEffect(() => {
    dispatch(fetchTaskById(id));
  }, [dispatch, id]);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      const result = await dispatch(deleteTask(id));
      if (deleteTask.fulfilled.match(result)) {
        toast.success('Task deleted successfully');
        navigate('/tasks');
      }
    }
  };

  const handleMarkCompleted = async () => {
    const result = await dispatch(markTaskCompleted(id));
    if (markTaskCompleted.fulfilled.match(result)) {
      toast.success('Task marked as completed');
    }
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

  if (loading || !currentTask) {
    return (
      <div className="p-8">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      </div>
    );
  }

  const canEdit = user?.role === 'admin' || currentTask.created_by?.id === user?.id;

  return (
    <div className="p-8">
      <div className="mb-6">
        <button
          onClick={() => navigate('/tasks')}
          className="flex items-center text-gray-600 hover:text-gray-900"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Tasks
        </button>
      </div>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{currentTask.title}</h1>
            <div className="flex items-center gap-3">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(currentTask.status)}`}>
                {currentTask.status.replace('_', ' ')}
              </span>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(currentTask.priority)}`}>
                {currentTask.priority}
              </span>
            </div>
          </div>
          <div className="flex gap-2">
            {currentTask.status !== 'completed' && (
              <button onClick={handleMarkCompleted} className="btn-primary">
                Mark Completed
              </button>
            )}
            {canEdit && (
              <>
                <button onClick={() => setIsEditModalOpen(true)} className="btn-secondary">
                  Edit
                </button>
                <button onClick={handleDelete} className="btn-danger">
                  Delete
                </button>
              </>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-2">Assigned To</h3>
            {currentTask.assigned_to ? (
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center text-white font-bold">
                  {currentTask.assigned_to.first_name?.[0] || currentTask.assigned_to.email[0].toUpperCase()}
                </div>
                <div>
                  <p className="font-medium text-gray-900">
                    {currentTask.assigned_to.first_name} {currentTask.assigned_to.last_name}
                  </p>
                  <p className="text-sm text-gray-500">{currentTask.assigned_to.email}</p>
                </div>
              </div>
            ) : (
              <p className="text-gray-500">Unassigned</p>
            )}
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-2">Created By</h3>
            {currentTask.created_by && (
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center text-white font-bold">
                  {currentTask.created_by.first_name?.[0] || currentTask.created_by.email[0].toUpperCase()}
                </div>
                <div>
                  <p className="font-medium text-gray-900">
                    {currentTask.created_by.first_name} {currentTask.created_by.last_name}
                  </p>
                  <p className="text-sm text-gray-500">{currentTask.created_by.email}</p>
                </div>
              </div>
            )}
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-2">Due Date</h3>
            <p className="text-gray-900">
              {currentTask.due_date ? format(new Date(currentTask.due_date), 'MMMM dd, yyyy HH:mm') : 'No due date'}
            </p>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-2">Created At</h3>
            <p className="text-gray-900">
              {format(new Date(currentTask.created_at), 'MMMM dd, yyyy HH:mm')}
            </p>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-2">Last Updated</h3>
            <p className="text-gray-900">
              {format(new Date(currentTask.updated_at), 'MMMM dd, yyyy HH:mm')}
            </p>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-medium text-gray-500 mb-2">Description</h3>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-gray-900 whitespace-pre-wrap">
              {currentTask.description || 'No description provided'}
            </p>
          </div>
        </div>
      </div>

      {isEditModalOpen && (
        <TaskModal
          isOpen={isEditModalOpen}
          onClose={() => setIsEditModalOpen(false)}
          task={currentTask}
        />
      )}
    </div>
  );
};

export default TaskDetail;
