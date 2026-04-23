import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

const initialState = {
  events: [],
  currentEvent: null,
  loading: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
  },
};

export const fetchEvents = createAsyncThunk(
  'events/fetchEvents',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await api.get('/events/', { params });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch events');
    }
  }
);

export const fetchEventById = createAsyncThunk(
  'events/fetchEventById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await api.get(`/events/${id}/`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch event');
    }
  }
);

const eventSlice = createSlice({
  name: 'events',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchEvents.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchEvents.fulfilled, (state, action) => {
        state.loading = false;
        state.events = action.payload.results;
        state.pagination = {
          count: action.payload.count,
          next: action.payload.next,
          previous: action.payload.previous,
        };
      })
      .addCase(fetchEvents.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchEventById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchEventById.fulfilled, (state, action) => {
        state.loading = false;
        state.currentEvent = action.payload;
      })
      .addCase(fetchEventById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError } = eventSlice.actions;
export default eventSlice.reducer;
