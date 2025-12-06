import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      if (window.location.pathname !== '/login') {
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default {
  // AUTENTICACIÓN
  auth: {
    login: (credentials) => api.post('/auth/login', credentials),
    logout: () => api.post('/auth/logout'),
    me: () => api.get('/auth/me'),
    check: () => api.get('/auth/check')
  },

  // CATEGORÍAS
  categorias: {
    getAll: () => api.get('/categorias'),
    getById: (id) => api.get(`/categorias/${id}`),
    create: (data) => api.post('/categorias', data),
    update: (id, data) => api.put(`/categorias/${id}`, data),
    delete: (id) => api.delete(`/categorias/${id}`)
  },
  
  // PRODUCTOS
  productos: {
    getAll: () => api.get('/productos'),
    getById: (id) => api.get(`/productos/${id}`),
    create: (data) => api.post('/productos', data),
    update: (id, data) => api.put(`/productos/${id}`, data),
    delete: (id) => api.delete(`/productos/${id}`)
  },
  
  // CLIENTES
  clientes: {
    getAll: () => api.get('/clientes'),
    getById: (id) => api.get(`/clientes/${id}`),
    create: (data) => api.post('/clientes', data),
    update: (id, data) => api.put(`/clientes/${id}`, data),
    delete: (id) => api.delete(`/clientes/${id}`)
  },
  
  // VENTAS
  ventas: {
    getAll: () => api.get('/ventas'),
    getById: (id) => api.get(`/ventas/${id}`),
    create: (data) => api.post('/ventas', data),
    update: (id, data) => api.put(`/ventas/${id}`, data),
    delete: (id) => api.delete(`/ventas/${id}`)
  },
  
  // EMPLEADOS
  empleados: {
    getAll: () => api.get('/empleados'),
    getById: (id) => api.get(`/empleados/${id}`),
    create: (data) => api.post('/empleados', data),
    update: (id, data) => api.put(`/empleados/${id}`, data),
    delete: (id) => api.delete(`/empleados/${id}`)
  },

  // PAGOS
  pagos: {
    getAll: () => api.get('/pagos'),
    getById: (id) => api.get(`/pagos/${id}`),
    create: (data) => api.post('/pagos', data),
    update: (id, data) => api.put(`/pagos/${id}`, data),
    delete: (id) => api.delete(`/pagos/${id}`),
    porVenta: (ventaId) => api.get(`/pagos/venta/${ventaId}`)
  },

  // STOCK
  stock: {
    getAll: () => api.get('/stock_adjustments'),
    getById: (id) => api.get(`/stock_adjustments/${id}`),
    create: (data) => api.post('/stock_adjustments', data),
    porProducto: (productoId) => api.get(`/stock_adjustments/producto/${productoId}`)
  },

  // REPORTES
  reportes: {
    resumen: () => api.get('/reportes/resumen'),
    ventas: () => api.get('/reportes/ventas'),
    productos: () => api.get('/reportes/productos'),
    clientes: () => api.get('/reportes/clientes'),
    bajoStock: () => api.get('/reportes/productos-bajo-stock')
  }
}