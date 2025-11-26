<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Navbar -->
    <nav class="bg-gradient-to-r from-primary to-secondary text-white shadow-lg">
      <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <h1 class="text-2xl font-bold">📚 Librería Pandora</h1>
          </div>
          <div class="flex space-x-6">
            <router-link to="/" class="hover:text-gray-200 transition">Inicio</router-link>
            <router-link to="/categorias" class="hover:text-gray-200 transition">Categorías</router-link>
            <router-link to="/productos" class="hover:text-gray-200 transition">Productos</router-link>
            <router-link to="/clientes" class="hover:text-gray-200 transition">Clientes</router-link>
            <router-link to="/ventas" class="hover:text-gray-200 transition">Ventas</router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <main class="container mx-auto px-6 py-8">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white text-center py-4 mt-12">
      <p>&copy; 2025 Librería Pandora - Sistema de Gestión</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>