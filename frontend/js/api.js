const API_BASE = 'https://todo-app-f5tw.onrender.com/api/v1';

const api = {
  getToken: () => localStorage.getItem('token'),
  setToken: (token) => localStorage.setItem('token', token),
  removeToken: () => localStorage.removeItem('token'),
  isLoggedIn: () => !!localStorage.getItem('token'),

  headers: (auth = false) => {
    const h = { 'Content-Type': 'application/json' };
    if (auth) h['Authorization'] = `Bearer ${api.getToken()}`;
    return h;
  },

  async request(method, endpoint, body = null, auth = false) {
    const options = { method, headers: api.headers(auth) };
    if (body) options.body = JSON.stringify(body);
    const res = await fetch(`${API_BASE}${endpoint}`, options);
    const data = await res.json();
    if (!res.ok) throw { status: res.status, detail: data.detail };
    return data;
  },

  // Auth
  register: (body) => api.request('POST', '/auth/register', body),
  login: (body) => api.request('POST', '/auth/login', body),

  // Todos (protected)
  getTodos: () => api.request('GET', '/todos', null, true),
  createTodo: (body) => api.request('POST', '/todos', body, true),
  updateTodo: (id, body) => api.request('PUT', `/todos/${id}`, body, true),
  deleteTodo: (id) => api.request('DELETE', `/todos/${id}`, null, true),

  // Guest todos (public)
  getGuestTodos: () => api.request('GET', '/guest/todos'),
  createGuestTodo: (body) => api.request('POST', '/guest/todos', body),
};
