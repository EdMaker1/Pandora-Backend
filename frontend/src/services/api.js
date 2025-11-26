/*'''import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para manejar errores
api.interceptors.response.use(
  response => response,
  error => {
    console.error('Error en la petición:', error)
    return Promise.reject(error)
  }
)

export default {
  // Categorías
  categorias: {
    getAll: () => api.get('/categorias'),
    getById: (id) => api.get(`/categorias/${id}`),
    create: (data) => api.post('/categorias', data),
    update: (id, data) => api.put(`/categorias/${id}`, data),
    delete: (id) => api.delete(`/categorias/${id}`)
  },
  
  // Productos
  productos: {
    getAll: () => api.get('/productos'),
    getById: (id) => api.get(`/productos/${id}`),
    create: (data) => api.post('/productos', data),
    update: (id, data) => api.put(`/productos/${id}`, data),
    delete: (id) => api.delete(`/productos/${id}`)
  },
  
  // Clientes
  clientes: {
    getAll: () => api.get('/clientes'),
    getById: (id) => api.get(`/clientes/${id}`),
    create: (data) => api.post('/clientes', data),
    update: (id, data) => api.put(`/clientes/${id}`, data),
    delete: (id) => api.delete(`/clientes/${id}`)
  },
  
  // Ventas
  ventas: {
    getAll: () => api.get('/ventas'),
    getById: (id) => api.get(`/ventas/${id}`),
    create: (data) => api.post('/ventas', data),
    update: (id, data) => api.put(`/ventas/${id}`, data),
    delete: (id) => api.delete(`/ventas/${id}`)
  },
  
  // Empleados
  empleados: {
    getAll: () => api.get('/empleados')
  }
}
'''*/
import axios from 'axios'

const api = axios.create({
  // CORRECCIÓN: Usar una URL relativa /api. 
  // Esto permite que el proxy de Vite (en dev) se encargue de reenviar a localhost:5000, 
  // y en producción, la llamada se hace al propio dominio (ej. miweb.com/api).
  baseURL: '/api', 
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para manejar errores
api.interceptors.response.use(
  response => response,
  error => {
    // Aquí puedes añadir lógica de manejo de errores HTTP (ej. mostrar notificación)
    console.error('Error en la petición:', error)
    return Promise.reject(error)
  }
)

export default {
  // Categorías
  categorias: {
    getAll: () => api.get('/categorias'),
    getById: (id) => api.get(`/categorias/${id}`),
    create: (data) => api.post('/categorias', data),
    update: (id, data) => api.put(`/categorias/${id}`, data),
    delete: (id) => api.delete(`/categorias/${id}`)
  },
  
  // Productos
  productos: {
    getAll: () => api.get('/productos'),
    getById: (id) => api.get(`/productos/${id}`),
    create: (data) => api.post('/productos', data),
    update: (id, data) => api.put(`/productos/${id}`, data),
    delete: (id) => api.delete(`/productos/${id}`)
  },
  
  // Clientes
  clientes: {
    getAll: () => api.get('/clientes'),
    getById: (id) => api.get(`/clientes/${id}`),
    create: (data) => api.post('/clientes', data),
    update: (id, data) => api.put(`/clientes/${id}`, data),
    delete: (id) => api.delete(`/clientes/${id}`)
  },
  
  // Ventas
  ventas: {
    getAll: () => api.get('/ventas'),
    getById: (id) => api.get(`/ventas/${id}`),
    create: (data) => api.post('/ventas', data),
    update: (id, data) => api.put(`/ventas/${id}`, data),
    delete: (id) => api.delete(`/ventas/${id}`)
  },
  
  // Empleados
  empleados: {
    getAll: () => api.get('/empleados')
  }
}