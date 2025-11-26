# Crear frontend/src/views/Clientes.vue
cat > frontend/src/views/Clientes.vue << 'EOF'
<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Gestión de Clientes</h1>
      <button @click="openModal()" class="btn-primary">
        + Nuevo Cliente
      </button>
    </div>

    <!-- Tabla -->
    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="table-header">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombres</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Apellidos</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Teléfono</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Consumidor</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="cliente in clientes" :key="cliente.id" class="table-row">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ cliente.id }}</td>
              <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ cliente.nombres }}</td>
              <td class="px-6 py-4 text-sm text-gray-900">{{ cliente.apellidos || '-' }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ cliente.email || '-' }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ cliente.telefono || '-' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span :class="cliente.es_consumidor ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" 
                      class="px-2 py-1 rounded-full text-xs font-semibold">
                  {{ cliente.es_consumidor ? 'Sí' : 'No' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button @click="openModal(cliente)" class="text-blue-600 hover:text-blue-900">Editar</button>
                <button @click="deleteCliente(cliente.id)" class="text-red-600 hover:text-red-900">Eliminar</button>
              </td>
            </tr>
            <tr v-if="clientes.length === 0">
              <td colspan="7" class="px-6 py-4 text-center text-gray-500">No hay clientes registrados</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-8 max-w-2xl w-full mx-4">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">
          {{ editMode ? 'Editar Cliente' : 'Nuevo Cliente' }}
        </h2>
        
        <form @submit.prevent="saveCliente" class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Nombres *</label>
            <input v-model="form.nombres" type="text" required class="input-field">
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Apellidos</label>
            <input v-model="form.apellidos" type="text" class="input-field">
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Email</label>
            <input v-model="form.email" type="email" class="input-field">
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Teléfono</label>
            <input v-model="form.telefono" type="text" class="input-field">
          </div>

          <div class="col-span-2">
            <label class="block text-gray-700 text-sm font-bold mb-2">Dirección</label>
            <input v-model="form.direccion" type="text" class="input-field">
          </div>

          <div class="col-span-2">
            <label class="flex items-center space-x-2">
              <input v-model="form.es_consumidor" type="checkbox" class="w-4 h-4 text-primary">
              <span class="text-gray-700 text-sm font-bold">¿Es consumidor final?</span>
            </label>
          </div>
          
          <div class="col-span-2 flex justify-end space-x-3 mt-4">
            <button type="button" @click="closeModal()" class="btn-secondary">Cancelar</button>
            <button type="submit" class="btn-primary">{{ editMode ? 'Actualizar' : 'Crear' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Clientes',
  data() {
    return {
      clientes: [],
      showModal: false,
      editMode: false,
      form: {
        id: null,
        nombres: '',
        apellidos: '',
        email: '',
        telefono: '',
        direccion: '',
        es_consumidor: false
      }
    }
  },
  mounted() {
    this.loadClientes()
  },
  methods: {
    async loadClientes() {
      try {
        const response = await api.clientes.getAll()
        this.clientes = response.data
      } catch (error) {
        alert('Error al cargar clientes')
      }
    },
    openModal(cliente = null) {
      if (cliente) {
        this.editMode = true
        this.form = { ...cliente }
      } else {
        this.editMode = false
        this.form = {
          id: null,
          nombres: '',
          apellidos: '',
          email: '',
          telefono: '',
          direccion: '',
          es_consumidor: false
        }
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
    },
    async saveCliente() {
      try {
        if (this.editMode) {
          await api.clientes.update(this.form.id, this.form)
          alert('Cliente actualizado exitosamente')
        } else {
          await api.clientes.create(this.form)
          alert('Cliente creado exitosamente')
        }
        this.closeModal()
        this.loadClientes()
      } catch (error) {
        alert('Error: ' + (error.response?.data?.error || error.message))
      }
    },
    async deleteCliente(id) {
      if (!confirm('¿Eliminar este cliente?')) return
      try {
        await api.clientes.delete(id)
        alert('Cliente eliminado')
        this.loadClientes()
      } catch (error) {
        alert('Error: ' + (error.response?.data?.error || error.message))
      }
    }
  }
}
</script>
EOF