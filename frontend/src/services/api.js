import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para adicionar token nas requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const systemService = {
  getRoot: () => api.get('/'),
  health: () => api.get('/health'),
  about: () => api.get('/about'),
}

export const authService = {
  register: (data) => api.post('/api/v1/auth/register', data),
  login: (email, password) => api.post('/api/v1/auth/login', { email, password }),
}

export const booksService = {
  listBooks: () => api.get('/api/v1/books'),
  getBook: (id) => api.get(`/api/v1/books/${id}`),
  createBook: (data) => api.post('/api/v1/books', data),
  updateBook: (id, data) => api.put(`/api/v1/books/${id}`, data),
  deleteBook: (id) => api.delete(`/api/v1/books/${id}`),
}

export default api