import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

const initialState = {
  tasks: [],
  currentTask: null,
  myTasks: [],
  createdTasks: [],
  loading: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
  },
  filters: {
    status: '',
    priority: '',
    search: '',
    ordering: '-created_at',
  },
};

export const fetchTasks = createAsyncThunk(
  'tasks/fetchTasks',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await api.get('/tasks/', { params });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch tasks');
    }
  }
);

export const fetchTaskById = createAsyncThunk(
  'tasks/fetchTaskById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await api.get(`/tasks/${id}/`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch task');
    }
  }
);

export const createTask = createAsyncThunk(
  'tasks/createTask',
  async (taskData, { rejectWithValue }) => {
    try {
      const response = await api.post('/tasks/', taskData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to create task');
    }
  }
);

export const updateTask = createAsyncThunk(
  'tasks/updateTask',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await api.patch(`/tasks/${id}/`, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to update task');
    }
  }
);

export const deleteTask = createAsyncThunk(
  'tasks/deleteTask',
  async (id, { rejectWithValue }) => {
    try {
      await api.delete(`/tasks/${id}/`);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to delete task');
    }
  }
);

export const fetchMyTasks = createAsyncThunk(
  'tasks/fetchMyTasks',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/tasks/my_tasks/');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch my tasks');
    }
  }
);

export const fetchCreatedTasks = createAsyncThunk(
  'tasks/fetchCreatedTasks',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/tasks/created_by_me/');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch created tasks');
    }
  }
);

export const markTaskCompleted = createAsyncThunk(
  'tasks/markTaskCompleted',
  async (id, { rejectWithValue }) => {
    try {
      const response = await api.patch(`/tasks/${id}/mark_completed/`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to mark task as completed');
    }
  }
);

const taskSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = {
        status: '',
        priority: '',
        search: '',
        ordering: '-created_at',
      };
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.loading = false;
        state.tasks = action.payload.results;
        state.pagination = {
          count: action.payload.count,
          next: action.payload.next,
          previous: action.payload.previous,
        };
      })
      .addCase(fetchTasks.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchTaskById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTaskById.fulfilled, (state, action) => {
        state.loading = false;
        state.currentTask = action.payload;
      })
      .addCase(fetchTaskById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createTask.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createTask.fulfilled, (state, action) => {
        state.loading = false;
        state.tasks.unshift(action.payload);
      })
      .addCase(createTask.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateTask.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateTask.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.tasks.findIndex(task => task.id === action.payload.id);
        if (index !== -1) {
          state.tasks[index] = action.payload;
        }
        if (state.currentTask?.id === action.payload.id) {
          state.currentTask = action.payload;
        }
      })
      .addCase(updateTask.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteTask.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteTask.fulfilled, (state, action) => {
        state.loading = false;
        state.tasks = state.tasks.filter(task => task.id !== action.payload);
      })
      .addCase(deleteTask.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchMyTasks.fulfilled, (state, action) => {
        state.myTasks = action.payload.results || action.payload;
      })
      .addCase(fetchCreatedTasks.fulfilled, (state, action) => {
        state.createdTasks = action.payload.results || action.payload;
      })
      .addCase(markTaskCompleted.fulfilled, (state, action) => {
        const index = state.tasks.findIndex(task => task.id === action.payload.id);
        if (index !== -1) {
          state.tasks[index] = action.payload;
        }
      });
  },
});

export const { setFilters, clearFilters, clearError } = taskSlice.actions;
export default taskSlice.reducer;
